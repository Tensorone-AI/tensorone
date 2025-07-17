<script>
	// ===================================
	// IMPORTS & COMPONENT SETUP
	// ===================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import { fade } from 'svelte/transition';
	import { wallet } from '$lib/stores/wallet';
	import { onMount } from 'svelte';

	// Import new components
	import ErrorMessage from './ErrorMessage.svelte';
	import PromptInput from './PromptInput.svelte';
	import GenerateButton from './GenerateButton.svelte';
	import VideoPlayer from './VideoPlayer.svelte';
	import EmptyState from './EmptyState.svelte';
	import LoadingState from './LoadingState.svelte';

	// Props
	export let data = {};

	// ===================================
	// 1. VIDEO GENERATION STATUS CHECK
	// ===================================

	let pollingInterval;
	let isPolling = false;

	// ===================================
	// 2. REACTIVITY ONLY
	// ===================================

	// Reactive state derived from props and stores
	$: address = data?.address || $wallet?.address || '';
	$: progressPercentage = duration > 0 ? (currentTime / duration) * 100 : 0;

	// Component state variables
	let prompt = '';
	let isGenerating = false;
	let generatedVideo = null;
	let error = null;

	// Video player state
	let videoElement;
	let isPlaying = false;
	let currentTime = 0;
	let duration = 0;
	let isDragging = false;

	// ===================================
	// 3. DATA INPUT TO DATABASE
	// ===================================

	// Check video generation status
	async function checkVideoStatus() {
		if (!address) return;

		try {
			const response = await fetch('/api/playground/video/check_generate', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ address })
			});

			if (!response.ok) {
				throw new Error('Failed to check video status');
			}

			const result = await response.json();
			
			if (result.status === 'complete' && result.result_video_path) {
				generatedVideo = {
					id: `video_${Date.now()}`,
					url: result.result_video_path,
					prompt: 'Generated video',
					createdAt: new Date().toISOString()
				};
				isGenerating = false;
				stopPolling();
			} else if (result.status === 'waiting') {
				isGenerating = true;
				startPolling();
			} else if (result.status === 'nothing') {
				isGenerating = false;
				stopPolling();
			}
		} catch (err) {
			console.error('Error checking video status:', err);
			error = 'Failed to check video status';
		}
	}

	// Start polling for video status
	function startPolling() {
		if (isPolling) return;
		
		isPolling = true;
		pollingInterval = setInterval(checkVideoStatus, 6000);
	}

	// Stop polling
	function stopPolling() {
		if (pollingInterval) {
			clearInterval(pollingInterval);
			pollingInterval = null;
		}
		isPolling = false;
	}

	// Generate video function
	async function generateVideo() {
		if (!prompt.trim()) {
			error = 'Please enter a prompt to generate a video';
			return;
		}

		if (prompt.trim().length < 3) {
			error = 'Prompt must be at least 3 characters long';
			return;
		}

		isGenerating = true;
		error = null;
		generatedVideo = null;

		try {
			const requestId = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
			
			const response = await fetch('/api/playground/video/generate-video', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					address,
					request_id: requestId,
					prompt: prompt.trim()
				})
			});

			if (!response.ok) {
				throw new Error('Failed to generate video');
			}

			const result = await response.json();
			
			if (result.request_id) {
				startPolling();
			} else {
				throw new Error('Invalid response from server');
			}
		} catch (err) {
			error = err.message || 'An error occurred while generating the video';
			console.error('Video generation error:', err);
			isGenerating = false;
		}
	}

	// Mount function
	onMount(() => {
		checkVideoStatus();
		
		return () => {
			stopPolling();
		};
	});

	// ===================================
	// UI INTERACTION HANDLERS
	// ===================================

	// Input handling
	function handleKeydown(event) {
		if (event.key === 'Enter') {
			event.preventDefault(); // Prevent new line
			generateVideo();
		}
	}

	// Error handling
	function clearError() {
		error = null;
	}

	// Video player functions
	function togglePlay() {
		if (!videoElement) return;

		if (isPlaying) {
			videoElement.pause();
		} else {
			videoElement.play();
		}
	}

	function skipBackward() {
		if (!videoElement) return;
		videoElement.currentTime = Math.max(0, videoElement.currentTime - 10);
	}

	function skipForward() {
		if (!videoElement) return;
		videoElement.currentTime = Math.min(duration, videoElement.currentTime + 10);
	}

	function onTimeUpdate() {
		if (!isDragging && videoElement) {
			currentTime = videoElement.currentTime;
		}
	}

	function onLoadedMetadata() {
		if (videoElement) {
			duration = videoElement.duration;
		}
	}

	function onPlay() {
		isPlaying = true;
	}

	function onPause() {
		isPlaying = false;
	}

	function onProgressClick(event) {
		if (!videoElement || !duration) return;

		const rect = event.currentTarget.getBoundingClientRect();
		const pos = (event.clientX - rect.left) / rect.width;
		const newTime = pos * duration;

		videoElement.currentTime = newTime;
		currentTime = newTime;
	}

	function onProgressMouseDown(event) {
		isDragging = true;
		onProgressClick(event);

		function onMouseMove(e) {
			if (isDragging) {
				onProgressClick(e);
			}
		}

		function onMouseUp() {
			isDragging = false;
			document.removeEventListener('mousemove', onMouseMove);
			document.removeEventListener('mouseup', onMouseUp);
		}

		document.addEventListener('mousemove', onMouseMove);
		document.addEventListener('mouseup', onMouseUp);
	}

	// Video actions
	function toggleFullscreen() {
		if (!videoElement) return;

		if (document.fullscreenElement) {
			document.exitFullscreen();
		} else {
			videoElement.requestFullscreen();
		}
	}

	async function downloadVideo() {
		if (!generatedVideo?.url) return;

		try {
			// TODO: Update download statistics in database
			// await updateVideoStats(generatedVideo.id, 'download');

			// Create a temporary link element for download
			const link = document.createElement('a');
			link.href = generatedVideo.url;
			link.download = `generated-video-${Date.now()}.mp4`;
			link.target = '_blank';
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		} catch (error) {
			console.error('Download failed:', error);
		}
	}
</script>

<svelte:head>
	<title>Text to Video</title>
	<meta
		name="description"
		content="Generate AI videos from text prompts with customizable duration and high-quality output."
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-8 flex flex-col">
	<PageTitle subtitle="Playground" title="Text to Video" {address} />

	<!-- Error Message Component -->
	{#if error}
		<ErrorMessage {error} onClear={clearError} />
	{/if}

	<div class="flex flex-1 gap-8 min-h-0">
		<!-- Controls Panel -->
		<div class="xl:w-2/5">
			<div class="flex-1 overflow-y-auto pr-2">
				<PromptInput bind:value={prompt} onKeydown={handleKeydown} disabled={isGenerating} />
			</div>
			<GenerateButton
				onClick={generateVideo}
				disabled={isGenerating || !prompt.trim()}
				{isGenerating}
			/>
		</div>

		<!-- Result Section -->
		<div
			class="xl:w-3/5 min-h-0"
			in:fade|global={{ delay: 550, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<div
				class="rounded-3xl h-full flex items-center justify-center relative overflow-hidden transition-all duration-300 p-4 {isGenerating
					? 'bg-kedua border border-utama animate-pulse'
					: 'bg-black border border-[#444A61]'}"
			>
				{#if generatedVideo}
					<VideoPlayer
						video={generatedVideo}
						bind:videoElement
						{isPlaying}
						{currentTime}
						{duration}
						{progressPercentage}
						{onTimeUpdate}
						{onLoadedMetadata}
						{onPlay}
						{onPause}
						{onProgressClick}
						{onProgressMouseDown}
						{togglePlay}
						{skipBackward}
						{skipForward}
						{toggleFullscreen}
						{downloadVideo}
					/>
				{:else if isGenerating}
					<LoadingState />
				{:else}
					<EmptyState />
				{/if}
			</div>
		</div>
	</div>
</section>
