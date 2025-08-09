<script>
	import { onMount, onDestroy } from 'svelte';
	import * as THREE from 'three';
	import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
	import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';
	import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';
	import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass';

	export let microphoneStream = null;
	export let isListening = false;
	export let isProcessing = false;
	export let isAgentSpeaking = false;

	let container;
	let renderer;
	let scene;
	let camera;
	let mesh;
	let uniforms;
	let bloomComposer;
	let analyser;
	let sound;
	let listener;
	let animationId;
	let clock;
	let microphoneAnalyser = null;
	let mouseX = 0;
	let mouseY = 0;

	const vertexShader = `
		uniform float u_time;

		vec3 mod289(vec3 x) {
			return x - floor(x * (1.0 / 289.0)) * 289.0;
		}

		vec4 mod289(vec4 x) {
			return x - floor(x * (1.0 / 289.0)) * 289.0;
		}

		vec4 permute(vec4 x) {
			return mod289(((x*34.0)+10.0)*x);
		}

		vec4 taylorInvSqrt(vec4 r) {
			return 1.79284291400159 - 0.85373472095314 * r;
		}

		vec3 fade(vec3 t) {
			return t*t*t*(t*(t*6.0-15.0)+10.0);
		}

		float pnoise(vec3 P, vec3 rep) {
			vec3 Pi0 = mod(floor(P), rep);
			vec3 Pi1 = mod(Pi0 + vec3(1.0), rep);
			Pi0 = mod289(Pi0);
			Pi1 = mod289(Pi1);
			vec3 Pf0 = fract(P);
			vec3 Pf1 = Pf0 - vec3(1.0);
			vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
			vec4 iy = vec4(Pi0.yy, Pi1.yy);
			vec4 iz0 = Pi0.zzzz;
			vec4 iz1 = Pi1.zzzz;

			vec4 ixy = permute(permute(ix) + iy);
			vec4 ixy0 = permute(ixy + iz0);
			vec4 ixy1 = permute(ixy + iz1);

			vec4 gx0 = ixy0 * (1.0 / 7.0);
			vec4 gy0 = fract(floor(gx0) * (1.0 / 7.0)) - 0.5;
			gx0 = fract(gx0);
			vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
			vec4 sz0 = step(gz0, vec4(0.0));
			gx0 -= sz0 * (step(0.0, gx0) - 0.5);
			gy0 -= sz0 * (step(0.0, gy0) - 0.5);

			vec4 gx1 = ixy1 * (1.0 / 7.0);
			vec4 gy1 = fract(floor(gx1) * (1.0 / 7.0)) - 0.5;
			gx1 = fract(gx1);
			vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
			vec4 sz1 = step(gz1, vec4(0.0));
			gx1 -= sz1 * (step(0.0, gx1) - 0.5);
			gy1 -= sz1 * (step(0.0, gy1) - 0.5);

			vec3 g000 = vec3(gx0.x,gy0.x,gz0.x);
			vec3 g100 = vec3(gx0.y,gy0.y,gz0.y);
			vec3 g010 = vec3(gx0.z,gy0.z,gz0.z);
			vec3 g110 = vec3(gx0.w,gy0.w,gz0.w);
			vec3 g001 = vec3(gx1.x,gy1.x,gz1.x);
			vec3 g101 = vec3(gx1.y,gy1.y,gz1.y);
			vec3 g011 = vec3(gx1.z,gy1.z,gz1.z);
			vec3 g111 = vec3(gx1.w,gy1.w,gz1.w);

			vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
			g000 *= norm0.x;
			g010 *= norm0.y;
			g100 *= norm0.z;
			g110 *= norm0.w;
			vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
			g001 *= norm1.x;
			g011 *= norm1.y;
			g101 *= norm1.z;
			g111 *= norm1.w;

			float n000 = dot(g000, Pf0);
			float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
			float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
			float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
			float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
			float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
			float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
			float n111 = dot(g111, Pf1);

			vec3 fade_xyz = fade(Pf0);
			vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
			vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
			float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x);
			return 2.2 * n_xyz;
		}

		uniform float u_frequency;

		void main() {
			float noise = 3.0 * pnoise(position + u_time, vec3(10.0));
			float displacement = (u_frequency / 30.) * (noise / 10.);
			vec3 newPosition = position + normal * displacement;
			gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
		}
	`;

	const fragmentShader = `
		uniform float u_red;
		uniform float u_blue;
		uniform float u_green;
		void main() {
			gl_FragColor = vec4(vec3(u_red, u_green, u_blue), 1.);
		}
	`;

	function handleMouseMove(e) {
		if (!container) return;
		const rect = container.getBoundingClientRect();
		const windowHalfX = rect.width / 2;
		const windowHalfY = rect.height / 2;
		mouseX = (e.clientX - rect.left - windowHalfX) / 100;
		mouseY = (e.clientY - rect.top - windowHalfY) / 100;
	}

	function initThreeJS() {
		// Create renderer
		renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(container.clientWidth, container.clientHeight);
		renderer.outputColorSpace = THREE.SRGBColorSpace;
		renderer.setClearColor(0x000000, 0);
		container.appendChild(renderer.domElement);

		// Create scene and camera
		scene = new THREE.Scene();
		camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
		camera.position.set(0, -2, 14);
		camera.lookAt(0, 0, 0);

		// Create uniforms with specified colors
		uniforms = {
			u_time: { type: 'f', value: 0.0 },
			u_frequency: { type: 'f', value: 0.0 },
			u_red: { type: 'f', value: 0.0 },
			u_green: { type: 'f', value: 1.0 },
			u_blue: { type: 'f', value: 0.2 }
		};

		// Create material and mesh
		const material = new THREE.ShaderMaterial({
			uniforms,
			vertexShader,
			fragmentShader
		});

		const geometry = new THREE.IcosahedronGeometry(4, 30);
		mesh = new THREE.Mesh(geometry, material);
		mesh.material.wireframe = true;
		scene.add(mesh);

		// Setup post-processing
		const renderScene = new RenderPass(scene, camera);
		const bloomPass = new UnrealBloomPass(
			new THREE.Vector2(container.clientWidth, container.clientHeight)
		);
		bloomPass.threshold = 0.8;
		bloomPass.strength = 0.5;
		bloomPass.radius = 0.8;

		bloomComposer = new EffectComposer(renderer);
		bloomComposer.addPass(renderScene);
		bloomComposer.addPass(bloomPass);

		const outputPass = new OutputPass();
		bloomComposer.addPass(outputPass);

		// Setup audio
		listener = new THREE.AudioListener();
		camera.add(listener);
		sound = new THREE.Audio(listener);
		analyser = new THREE.AudioAnalyser(sound, 32);

		clock = new THREE.Clock();
	}

	function setupMicrophoneInput() {
		if (microphoneStream && listener) {
			try {
				const audioContext = listener.context;
				const source = audioContext.createMediaStreamSource(microphoneStream);
				
				// Create analyser for visualization only - DO NOT connect to output
				microphoneAnalyser = audioContext.createAnalyser();
				microphoneAnalyser.fftSize = 32;
				microphoneAnalyser.smoothingTimeConstant = 0.3;
				
				// Connect microphone source to analyser but NOT to destination
				source.connect(microphoneAnalyser);
				
				console.log('Microphone connected to Three.js visualizer (no echo)');
			} catch (error) {
				console.error('Error connecting microphone to visualizer:', error);
			}
		}
	}

	// Function to connect audio buffer source for response playback
	function connectAudioSource(audioSource) {
		if (audioSource && listener) {
			try {
				// Create a new audio object for the response
				const responseAudio = new THREE.Audio(listener);
				responseAudio.setNodeSource(audioSource);
				analyser = new THREE.AudioAnalyser(responseAudio, 32);
				console.log('Audio response connected to Three.js visualizer');
			} catch (error) {
				console.error('Error connecting audio response to visualizer:', error);
			}
		}
	}

	// Get frequency data from the appropriate analyser
	function getAudioFrequency() {
		if (isAgentSpeaking && analyser) {
			// Use Three.js analyser for AI speech
			return analyser.getAverageFrequency();
		} else if ((isListening || isProcessing) && microphoneAnalyser) {
			// Use Web Audio API analyser for microphone input
			const frequencyData = new Uint8Array(microphoneAnalyser.frequencyBinCount);
			microphoneAnalyser.getByteFrequencyData(frequencyData);
			
			// Calculate average frequency
			let sum = 0;
			for (let i = 0; i < frequencyData.length; i++) {
				sum += frequencyData[i];
			}
			return sum / frequencyData.length;
		}
		return 0;
	}

	function animate() {
		if (!renderer || !camera || !uniforms || !bloomComposer) return;

		camera.position.x += (mouseX - camera.position.x) * 0.05;
		camera.position.y += (-mouseY - camera.position.y) * 0.05;
		camera.lookAt(scene.position);

		uniforms.u_time.value = clock.getElapsedTime();
		
		// Always have subtle time-based animation regardless of listening state
		const time = clock.getElapsedTime();
		const subtleMovement = 3 + Math.sin(time * 0.5) * 2; // Oscillates between 1-5
		
		let finalFrequency = 5 + subtleMovement; // Always have base movement
		
		// Add audio frequency on top of base movement when listening or speaking
		if (isListening || isProcessing || isAgentSpeaking) {
			const audioFrequency = getAudioFrequency();
			finalFrequency = Math.max(finalFrequency, audioFrequency + subtleMovement);
		}
		
		uniforms.u_frequency.value = finalFrequency;

		bloomComposer.render();
		animationId = requestAnimationFrame(animate);
	}

	function handleResize() {
		if (!container || !renderer || !camera || !bloomComposer) return;

		const width = container.clientWidth;
		const height = container.clientHeight;

		camera.aspect = width / height;
		camera.updateProjectionMatrix();
		renderer.setSize(width, height);
		bloomComposer.setSize(width, height);
	}

	function cleanup() {
		if (animationId) {
			cancelAnimationFrame(animationId);
		}
		if (renderer) {
			renderer.dispose();
			if (container && renderer.domElement) {
				container.removeChild(renderer.domElement);
			}
		}
		if (sound) {
			sound.disconnect();
		}
		// Clean up microphone analyser
		microphoneAnalyser = null;
	}

	onMount(() => {
		initThreeJS();
		animate();
		window.addEventListener('resize', handleResize);
		container.addEventListener('mousemove', handleMouseMove);
	});

	onDestroy(() => {
		cleanup();
		window.removeEventListener('resize', handleResize);
		if (container) {
			container.removeEventListener('mousemove', handleMouseMove);
		}
	});

	// React to microphone stream changes
	$: if (microphoneStream) {
		setupMicrophoneInput();
	}
</script>

<div bind:this={container} class="w-full h-full relative">
</div>

<style>
	div {
		overflow: hidden;
	}
</style>