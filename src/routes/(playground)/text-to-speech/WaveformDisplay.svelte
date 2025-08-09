<script>
	import { onMount, onDestroy } from 'svelte';

	export let audioUrl;
	export let onReady;
	export let onPlay;
	export let onPause;
	export let onAudioProcess;
	export let onSeek;
	export let onFinish;
	export let onError;

	let container;
	let wavesurfer;

	// Initialize WaveSurfer
	async function initializeWaveSurfer() {
		if (!container || !audioUrl) return;

		try {
			// Dynamically import WaveSurfer
			const { default: WaveSurfer } = await import('wavesurfer.js');

			// Destroy existing instance
			if (wavesurfer) {
				wavesurfer.destroy();
			}

			// Create WaveSurfer instance
			wavesurfer = WaveSurfer.create({
				container: container,
				height: 120,
				waveColor: '#1F222D',
				progressColor: '#23f784',
				cursorColor: '#23f784',
				cursorWidth: 4,
				barWidth: 4,
				barGap: 4,
				barRadius: 3,
				interact: true,
				dragToSeek: true,
				responsive: true,
				normalize: true,
				autoplay: false,
				preload: true
			});

			// Event listeners
			wavesurfer.on('ready', onReady);
			wavesurfer.on('audioprocess', onAudioProcess);
			wavesurfer.on('seek', onSeek);
			wavesurfer.on('play', onPlay);
			wavesurfer.on('pause', onPause);
			wavesurfer.on('finish', onFinish);
			wavesurfer.on('error', onError);

			// Load the audio URL
			await wavesurfer.load(audioUrl);
		} catch (error) {
			console.error('Error initializing WaveSurfer:', error);
			onError(error);
		}
	}

	// Expose wavesurfer instance to parent
	export function getWaveSurfer() {
		return wavesurfer;
	}

	// Cleanup function
	function cleanup() {
		if (wavesurfer) {
			wavesurfer.destroy();
			wavesurfer = null;
		}
		if (container) {
			container.innerHTML = '';
		}
	}

	// Lifecycle
	onMount(() => {
		if (audioUrl) {
			setTimeout(() => {
				initializeWaveSurfer();
			}, 100);
		}
	});

	onDestroy(() => {
		cleanup();
	});

	// Reactive updates when audioUrl changes
	$: if (audioUrl && container) {
		cleanup();
		setTimeout(() => {
			initializeWaveSurfer();
		}, 200);
	}
</script>

<div class="waveform h-[120px] w-full" bind:this={container}></div>

<style>
	/* WaveSurfer container styling */
	:global(.waveform) {
		width: 100%;
		border-radius: 8px;
		overflow: hidden;
	}

	/* Custom scrollbar if needed */
	:global(.waveform > div) {
		border-radius: 8px;
	}
</style>
