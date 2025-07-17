<script>
	// ================================
	// IMPORTS AND COMPONENTS
	// ================================
	import { onMount, afterUpdate } from 'svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { wallet } from '$lib/stores/wallet';
	import { supabase } from '$lib/db/supabaseClient.js';

	// Components
	import Header from '../../Header.svelte';
	import PageTitle from '../../PageTitle.svelte';
	import ChatContainer from './ChatContainer.svelte';
	import AgentNotFound from './AgentNotFound.svelte';

	// Props
	export let data = {};

	// ================================
	// CATEGORY 1: FETCHING FROM DATABASE
	// ================================

	// Agent/Template fetching and validation
	$: agentSlug = $page.params.slug;
	$: currentItem = null; // Will be populated from Supabase
	
	// Fetch agent/template data from Supabase based on slug
	async function fetchAgentBySlug(slug) {
		isFetchingAgent = true;
		hasTriedFetch = false;
		agentNotFound = false; // Reset state
		
		try {
			// Check if slug starts with 'prebuilt-'
			if (slug.startsWith('prebuilt-')) {
				console.log('Fetching prebuilt agent with slug:', slug);
				
				const { data, error } = await supabase
					.from('prebuilt-mcp')
					.select('config, agent_name')
					.eq('slug', slug)
					.single();
				
				if (error) {
					console.error('Error fetching prebuilt agent:', error);
					throw error;
				}
				
				if (data && data.config) {
					console.log('Prebuilt agent config:', data.config);
					currentItem = {
						...data.config,
						agent_name: data.agent_name,
						type: 'template',
						slug: slug
					};
				} else {
					console.error('No config found for prebuilt agent');
					// Don't set agentNotFound here, let reactive statement handle it
				}
			} else {
				// Handle regular agents from mcp table
				console.log('Fetching regular agent with slug:', slug);
				
				const { data, error } = await supabase
					.from('mcp')
					.select('*')
					.eq('slug', slug)
					.single();
				
				if (error) {
					console.error('Error fetching agent:', error);
					throw error;
				}
				
				if (data) {
					// Check if the agent belongs to the current user
					if (data.address !== address) {
						console.error('Agent not found or access denied for user:', address);
						// Don't set agentNotFound here, let reactive statement handle it
					} else {
						console.log('Agent found and belongs to user:', data);
						currentItem = {
							...data,
							type: 'agent',
							slug: slug
						};
					}
				} else {
					console.error('No agent found with slug:', slug);
					// Don't set agentNotFound here, let reactive statement handle it
				}
			}
		} catch (error) {
			console.error('Error fetching agent:', error);
			// Don't set agentNotFound here, let reactive statement handle it
		} finally {
			isFetchingAgent = false;
			hasTriedFetch = true;
		}
	}



	// ================================
	// CATEGORY 2: REACTIVITY ONLY
	// ================================

	// Reactive address binding
	$: address = data?.address || $wallet?.address || '';

	// Check if current slug is prebuilt (for enabling/disabling call mode)
	$: isPrebuilt = agentSlug?.startsWith('prebuilt-') || false;

	// Check if call feature should be enabled based on 'call' column
	$: hasCallFeature = isPrebuilt || (currentItem && currentItem.call !== null);

	// Stable template detection - only set once and don't change
	let isTemplate = false;
	let sourceType = '';

	// Set the source type once when we find the item
	$: if (agentSlug && currentItem && !sourceType) {
		// TODO: Determine source type from Supabase data
		isTemplate = currentItem.type === 'template';
		sourceType = currentItem.type || 'agent';
		console.log('Source type determined:', sourceType, 'isTemplate:', isTemplate);
	}

	// Agent/Template existence check - only set agentNotFound after we've tried fetching
	$: {
		if (agentSlug && !currentItem && hasTriedFetch && !isFetchingAgent) {
			agentNotFound = true;
			console.error('Agent/Template not found for slug:', agentSlug);
		} else if (currentItem) {
			agentNotFound = false;
			console.log('Item found:', currentItem);
			console.log('Source type:', sourceType);
		}
	}

	// Initialize chat title with agent/template name
	$: if (currentItem && currentItem.agent_name) {
		chatTitle = currentItem.agent_name;
	}

	// Talk mode status text
	$: statusText = isListening
		? 'Listening...'
		: isProcessing
			? 'Processing...'
			: isAgentSpeaking
				? 'AI is speaking...'
				: 'Ready to talk';

	// ================================
	// STATE VARIABLES
	// ================================

	// UI State
	let isLoading = false;
	let prompt = '';
	let conversation = [];
	let chatTitle = 'New Chat';
	let messagesContainer;
	let shouldAutoScroll = true;
	let agentNotFound = false;
	let mounted = false;
	let isFetchingAgent = false;
	let hasTriedFetch = false;

	// Talk mode state variables
	let isTalkMode = false;

	// Voice recognition and audio state
	let recognition = null;
	let audioContext = null;
	let analyser = null;
	let microphone = null;
	let microphoneStream = null;
	let dataArray = null;
	let animationFrame = null;

	// AI speech simulation state
	let speechAnimationFrame = null;
	let isSpeechAnimating = false;

	// Voice state
	let voiceLevel = 0;
	let smoothedLevel = 0;
	let isMonitoring = false;
	let isListening = false;
	let isProcessing = false;
	let isAgentSpeaking = false;

	// Call mode state
	let mediaRecorder = null;
	let audioChunks = [];
	let currentAudio = null;

	// Voice activity detection state
	let silenceThreshold = 2; // Voice level below this is considered silence
	let silenceDuration = 1000; // 1 second of silence before stopping
	let lastVoiceTime = 0;
	let silenceCheckInterval = null;
	let isVoiceDetected = false;

	// User message copy state
	let copyStates = {};

	// ================================
	// SPEECH RECOGNITION INITIALIZATION
	// ================================

	// Initialize speech recognition
	if (typeof window !== 'undefined') {
		if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
			const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
			recognition = new SpeechRecognition();
			recognition.continuous = true;
			recognition.interimResults = true;
			recognition.lang = 'en-US';
		}
	}

	// ================================
	// UI INTERACTION FUNCTIONS
	// ================================

	// Navigation and UI controls
	function handleGoBack() {
		// Go back to templates if it's a template, otherwise go to agents
		if (isTemplate) {
			goto('/agent-templates');
		} else {
			goto('/my-agents');
		}
	}

	function handleTalkModeToggle() {
		isTalkMode = !isTalkMode;
		console.log('Talk mode toggled:', isTalkMode);
	}

	function handleBackToChat() {
		if (window.speechSynthesis) {
			window.speechSynthesis.cancel();
		}
		
		// Stop call mode recording if active
		if (hasCallFeature && mediaRecorder && mediaRecorder.state !== 'inactive') {
			mediaRecorder.stop();
		}
		
		// Stop current audio playback
		stopCurrentAudio();
		
		isListening = false;
		isProcessing = false;
		isAgentSpeaking = false;

		stopAudioMonitoring();
		stopSilenceDetection();
		stopSpeechAnimation();
		handleTalkModeToggle();
	}

	// Scroll management
	function scrollToBottom() {
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	}

	function handleScroll() {
		if (messagesContainer) {
			const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
			shouldAutoScroll = scrollTop + clientHeight >= scrollHeight - 100;
		}
	}

	// Auto-scroll after updates
	afterUpdate(() => {
		if (shouldAutoScroll && messagesContainer) {
			scrollToBottom();
		}
	});

	// ================================
	// INPUT HANDLING FUNCTIONS
	// ================================

	// Text input handlers
	function updatePrompt(event) {
		prompt = event.target.value;
	}

	function handleKeydown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	// User message copy functionality
	async function handleCopy(message) {
		try {
			await navigator.clipboard.writeText(message);
			copyStates[message] = 'success';
			console.log('Message copied to clipboard');

			// Reset to default after 2 seconds
			setTimeout(() => {
				copyStates[message] = 'default';
			}, 2000);
		} catch (err) {
			copyStates[message] = 'error';
			console.error('Failed to copy message:', err);

			// Reset to default after 2 seconds
			setTimeout(() => {
				copyStates[message] = 'default';
			}, 2000);
		}
	}

	// ================================
	// VOICE RECOGNITION FUNCTIONS
	// ================================

	// Voice listening controls
	async function startListening() {
		if (!recognition) {
			alert('Speech recognition is not supported in your browser');
			return;
		}

		try {
			await startAudioMonitoring();
		} catch (error) {
			console.error('Error starting audio monitoring:', error);
			return;
		}

		isListening = true;
		isProcessing = false;
		isAgentSpeaking = false;
		
		// Reset voice detection state
		isVoiceDetected = false;
		lastVoiceTime = Date.now();
		
		// Start silence detection
		startSilenceDetection();

		recognition.onresult = async (event) => {
			// Only process final results
			if (event.results[event.results.length - 1].isFinal) {
				const transcript = event.results[event.results.length - 1][0].transcript.trim();
				if (transcript) {
					isListening = false;
					isProcessing = true;
					stopAudioMonitoring();
					stopSilenceDetection();
					await processVoiceInput(transcript);
				}
			}
		};

		recognition.onerror = (event) => {
			console.error('Speech recognition error:', event.error);
			isListening = false;
			isProcessing = false;
			stopAudioMonitoring();
			stopSilenceDetection();
		};

		recognition.onend = () => {
			if (isListening) {
				stopAudioMonitoring();
				stopSilenceDetection();
				isListening = false;
			}
		};

		recognition.start();
	}

	function stopListening() {
		if (recognition) {
			recognition.stop();
		}
		stopAudioMonitoring();
		stopSilenceDetection();
		isListening = false;
		isVoiceDetected = false;
	}

	// Audio monitoring functions
	async function startAudioMonitoring() {
		const stream = await navigator.mediaDevices.getUserMedia({
			audio: {
				echoCancellation: false,
				noiseSuppression: false,
				autoGainControl: false,
				channelCount: 1
			}
		});

		microphoneStream = stream;
		audioContext = new (window.AudioContext || window.webkitAudioContext)();

		if (audioContext.state === 'suspended') {
			await audioContext.resume();
		}

		analyser = audioContext.createAnalyser();
		analyser.fftSize = 512;
		analyser.smoothingTimeConstant = 0.3;

		microphone = audioContext.createMediaStreamSource(stream);
		microphone.connect(analyser);
		dataArray = new Uint8Array(analyser.fftSize);

		isMonitoring = true;
		monitorAudio();
	}

	function monitorAudio() {
		if (!isMonitoring || !analyser || !dataArray) return;

		analyser.getByteTimeDomainData(dataArray);

		let sum = 0;
		for (let i = 0; i < dataArray.length; i++) {
			const value = Math.abs(dataArray[i] - 128);
			sum += value * value;
		}

		const rms = Math.sqrt(sum / dataArray.length);
		const normalizedLevel = rms / 128;
		let targetLevel = Math.floor(normalizedLevel * 100);
		targetLevel = Math.min(24, targetLevel);

		// Smooth the level changes - faster response but still smooth
		const smoothingFactor = 0.3; // Higher = more responsive, lower = smoother
		smoothedLevel += (targetLevel - smoothedLevel) * smoothingFactor;
		voiceLevel = Math.round(smoothedLevel);

		// Voice activity detection
		if (isListening) {
			const currentTime = Date.now();
			if (voiceLevel > silenceThreshold) {
				lastVoiceTime = currentTime;
				isVoiceDetected = true;
			}
		}

		animationFrame = requestAnimationFrame(monitorAudio);
	}

	// Voice activity detection functions
	function startSilenceDetection() {
		silenceCheckInterval = setInterval(() => {
			if (isListening && isVoiceDetected) {
				const currentTime = Date.now();
				const timeSinceLastVoice = currentTime - lastVoiceTime;
				
				// If we've detected silence for the required duration, stop listening
				if (timeSinceLastVoice >= silenceDuration) {
					console.log('Stopping listening due to silence detection');
					
					// Use appropriate stop function based on mode
					if (isTalkMode && hasCallFeature) {
						stopCallModeRecording();
					} else {
						stopListening();
					}
				}
			}
		}, 100); // Check every 100ms
	}

	function stopSilenceDetection() {
		if (silenceCheckInterval) {
			clearInterval(silenceCheckInterval);
			silenceCheckInterval = null;
		}
	}

	function stopAudioMonitoring() {
		isMonitoring = false;

		if (animationFrame) {
			cancelAnimationFrame(animationFrame);
			animationFrame = null;
		}

		if (microphoneStream) {
			microphoneStream.getTracks().forEach((track) => track.stop());
			microphoneStream = null;
		}

		if (microphone) {
			microphone.disconnect();
			microphone = null;
		}

		if (audioContext && audioContext.state !== 'closed') {
			audioContext.close();
			audioContext = null;
		}

		analyser = null;
		dataArray = null;

		// Only reset if not animating speech, otherwise let it fade naturally
		if (!isSpeechAnimating) {
			// Smooth fade out instead of instant reset
			const fadeOut = () => {
				if (smoothedLevel > 0.1) {
					smoothedLevel *= 0.9;
					voiceLevel = Math.round(smoothedLevel);
					requestAnimationFrame(fadeOut);
				} else {
					voiceLevel = 0;
					smoothedLevel = 0;
				}
			};
			fadeOut();
		}
	}

	// ================================
	// SPEECH ANIMATION FUNCTIONS
	// ================================

	function animateSpeechLevel() {
		if (!isSpeechAnimating) return;

		// Create smoother, more realistic speech patterns
		const time = Date.now() / 150; // Slower time progression for smoother animation
		const baseLevel = 6 + Math.sin(time * 0.4) * 2; // Gentler base oscillation between 4-8
		const speechPattern = Math.sin(time * 0.9) * Math.sin(time * 0.6) * 3; // Smoother speech modulation
		const randomVariation = (Math.random() - 0.5) * 1.5; // Reduced randomness

		let targetLevel = Math.floor(baseLevel + speechPattern + randomVariation);
		targetLevel = Math.max(3, Math.min(18, targetLevel)); // Slightly tighter range 3-18

		// Apply same smoothing to AI speech
		const smoothingFactor = 0.25; // Slightly smoother for AI speech
		smoothedLevel += (targetLevel - smoothedLevel) * smoothingFactor;
		voiceLevel = Math.round(smoothedLevel);

		speechAnimationFrame = requestAnimationFrame(animateSpeechLevel);
	}

	function startSpeechAnimation() {
		isSpeechAnimating = true;
		// Reset smoothed level to current level for smooth transition
		smoothedLevel = voiceLevel;
		animateSpeechLevel();
	}

	function stopSpeechAnimation() {
		isSpeechAnimating = false;
		if (speechAnimationFrame) {
			cancelAnimationFrame(speechAnimationFrame);
			speechAnimationFrame = null;
		}
		// Smooth transition back to 0
		const fadeOut = () => {
			if (smoothedLevel > 0.1) {
				smoothedLevel *= 0.85; // Gradual fade out
				voiceLevel = Math.round(smoothedLevel);
				requestAnimationFrame(fadeOut);
			} else {
				voiceLevel = 0;
				smoothedLevel = 0;
			}
		};
		fadeOut();
	}

	// ================================
	// SPEECH SYNTHESIS FUNCTIONS
	// ================================

	async function speakText(text) {
		return new Promise((resolve) => {
			if ('speechSynthesis' in window) {
				window.speechSynthesis.cancel();

				// Start speech animation when AI starts speaking
				startSpeechAnimation();

				const utterance = new SpeechSynthesisUtterance(text);
				utterance.rate = 1;
				utterance.pitch = 1;
				utterance.volume = 1;

				utterance.onend = () => {
					// Stop speech animation when AI finishes speaking
					stopSpeechAnimation();
					resolve();
				};

				utterance.onerror = () => {
					stopSpeechAnimation();
					resolve();
				};

				window.speechSynthesis.speak(utterance);
			} else {
				resolve();
			}
		});
	}

	// ================================
	// VOICE INPUT PROCESSING
	// ================================

	async function processVoiceInput(transcript) {
		try {
			isProcessing = false;
			isAgentSpeaking = true;

			await speakText("Voice input received: " + transcript);

			isAgentSpeaking = false;
			stopAudioMonitoring();
		} catch (error) {
			console.error('Error processing voice input:', error);
			isProcessing = false;
			isAgentSpeaking = false;
			stopAudioMonitoring();
		}
	}

	// ================================
	// CALL MODE PROCESSING
	// ================================

	async function startCallModeRecording() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			microphoneStream = stream;
			
			// Reset audio chunks
			audioChunks = [];
			
			// Create MediaRecorder
			mediaRecorder = new MediaRecorder(stream);
			
			mediaRecorder.ondataavailable = (event) => {
				if (event.data.size > 0) {
					audioChunks.push(event.data);
				}
			};
			
			mediaRecorder.onstop = async () => {
				const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
				await sendAudioToBackend(audioBlob);
			};
			
			// Start recording
			mediaRecorder.start();
			isListening = true;
			
			// Start audio monitoring for visualization
			await startAudioMonitoring();
			
			// Start silence detection
			startSilenceDetection();
			
		} catch (error) {
			console.error('Error starting call mode recording:', error);
			isListening = false;
		}
	}

	function stopCallModeRecording() {
		if (mediaRecorder && mediaRecorder.state !== 'inactive') {
			mediaRecorder.stop();
		}
		
		isListening = false;
		stopAudioMonitoring();
		stopSilenceDetection();
		
		// Clean up stream
		if (microphoneStream) {
			microphoneStream.getTracks().forEach(track => track.stop());
			microphoneStream = null;
		}
	}

	async function sendAudioToBackend(audioBlob) {
		try {
			// Disable talk button during processing
			isProcessing = true;
			
			// Create form data
			const formData = new FormData();
			formData.append('audio', audioBlob, 'audio.wav');
			formData.append('slug', agentSlug);
			
			// Send to our API endpoint
			const response = await fetch('/api/mcp/agentic-call', {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				throw new Error('Failed to process audio');
			}
			
			// Get audio response
			const audioData = await response.arrayBuffer();
			const audioContext = new (window.AudioContext || window.webkitAudioContext)();
			const audioBuffer = await audioContext.decodeAudioData(audioData);
			
			// Play response with Three.js visualizer
			await playAudioResponse(audioBuffer, audioContext);
			
		} catch (error) {
			console.error('Error sending audio to backend:', error);
		} finally {
			isProcessing = false;
		}
	}

	async function playAudioResponse(audioBuffer, audioContext) {
		try {
			// Stop any currently playing audio
			if (currentAudio) {
				currentAudio.stop();
			}
			
			// Create audio source
			const source = audioContext.createBufferSource();
			source.buffer = audioBuffer;
			
			// Connect to destination for playback
			source.connect(audioContext.destination);
			
			// Start speech animation
			isAgentSpeaking = true;
			startSpeechAnimation();
			
			// Play audio
			source.start();
			currentAudio = source;
			
			// Handle audio end
			source.onended = () => {
				isAgentSpeaking = false;
				stopSpeechAnimation();
				currentAudio = null;
			};
			
		} catch (error) {
			console.error('Error playing audio response:', error);
			isAgentSpeaking = false;
			stopSpeechAnimation();
		}
	}

	function stopCurrentAudio() {
		if (currentAudio) {
			currentAudio.stop();
			currentAudio = null;
		}
		isAgentSpeaking = false;
		stopSpeechAnimation();
	}

	// ================================
	// CATEGORY 3: DATA INPUT TO DATABASE
	// ================================

	// Main message sending function
	async function sendMessage() {
		if (!prompt.trim() || isLoading) return;

		const userMessage = prompt.trim();
		prompt = '';

		// Step 1: Add user message first
		conversation = [...conversation, { type: 'user', message: userMessage }];
		shouldAutoScroll = true;

		// Step 2: Wait a tiny bit for the user message to render, then show loading
		await new Promise((resolve) => setTimeout(resolve, 100));
		isLoading = true;

		try {
			const response = await fetch('/api/mcp/agentic-chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					prompt: userMessage,
					conversation: conversation,
					agent: currentItem, // Send either agent or template
					agentSlug: agentSlug,
					isTemplate: isTemplate // Let backend know if this is a template
				})
			});

			if (!response.ok) {
				throw new Error('Chat request failed');
			}

			const data = await response.json();

			// Step 3: Hide loading and add AI response
			isLoading = false;
			if (data.assistantMessage) {
				conversation = [...conversation, { type: 'assistant', message: data.assistantMessage }];
			}

		} catch (err) {
			console.error('Chat error:', err);
			isLoading = false;
			conversation = [
				...conversation,
				{
					type: 'assistant',
					message: 'Sorry, I encountered an error. Please try again.'
				}
			];
		}
	}

	// ================================
	// LIFECYCLE FUNCTIONS
	// ================================

	onMount(() => {
		console.log('Chat page mounted with slug:', agentSlug);
		console.log('Current item:', currentItem);

		// Reset source type when slug changes (new navigation)
		sourceType = '';

		// Fetch agent data when slug is available
		if (agentSlug) {
			fetchAgentBySlug(agentSlug);
		}

		setTimeout(() => {
			mounted = true;
		}, 50);

		// Cleanup on unmount
		return () => {
			if (window.speechSynthesis) {
				window.speechSynthesis.cancel();
			}
			
			// Stop call mode recording if active
			if (mediaRecorder && mediaRecorder.state !== 'inactive') {
				mediaRecorder.stop();
			}
			
			// Stop current audio playback
			stopCurrentAudio();
			
			stopAudioMonitoring();
			stopSilenceDetection();
			stopSpeechAnimation();
		};
	});
</script>

<svelte:head>
	<title>{currentItem ? `Chat with ${currentItem.name}` : 'AI Agent Chat'}</title>
	<meta name="description" content="Chat with AI Agent" />
</svelte:head>

<Header />

{#if agentNotFound}
	<AgentNotFound {handleGoBack} />
{:else if isFetchingAgent}
	<div class="min-h-screen w-full overflow-hidden px-10 flex items-center justify-center">
		<div class="loading loading-spinner loading-lg text-utama"></div>
	</div>
{:else if mounted && (currentItem || hasTriedFetch)}
	<div class="min-h-screen w-full overflow-hidden px-10" key={agentSlug}>
		<div
			in:fly={{
				delay: 100,
				duration: 800,
				y: 50,
				opacity: 0,
				easing: quintOut
			}}
			out:fade={{ duration: 200 }}
		>
			<div class="flex">
				<div class="relative w-full">
					<div class="gap-y-1 p-4 lg:gap-x-12 lg:px-6 h-screen">
						<section
							class="col-span-12 w-full shadow-sm relative lg:pt-5"
							in:fly={{
								delay: 200,
								duration: 600,
								y: -30,
								opacity: 0,
								easing: quintOut
							}}
							out:fade={{ duration: 200 }}
						>
							<div in:fade={{ delay: 300, duration: 400 }} out:fade={{ duration: 200 }}>
								<PageTitle
									subtitle={isTemplate ? 'Templates' : 'My Agents'}
									title="Chat with {chatTitle}"
									{address}
									showBackButton={true}
									backTo={isTemplate ? '/agent-templates' : '/my-agents'}
								/>

								<ChatContainer
									bind:conversation
									bind:isLoading
									bind:messagesContainer
									bind:prompt
									bind:isTalkMode
									{chatTitle}
									{handleScroll}
									{updatePrompt}
									{handleKeydown}
									{sendMessage}
									{handleTalkModeToggle}
									{handleBackToChat}
									{voiceLevel}
									{statusText}
									{isListening}
									{isProcessing}
									{isAgentSpeaking}
									{startListening}
									{stopListening}
									{startCallModeRecording}
									{stopCallModeRecording}
									{stopCurrentAudio}
									{copyStates}
									{handleCopy}
									{hasCallFeature}
									{microphoneStream}
								/>
							</div>
						</section>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
