<script>
	import { fly } from 'svelte/transition';
	import WaveformDisplay from './WaveformDisplay.svelte';
	import TimeDisplay from './TimeDisplay.svelte';
	import AudioControls from './AudioControls.svelte';
	import DownloadButton from './DownloadButton.svelte';
	import EmptyState from './EmptyState.svelte';
	import LoadingState from './LoadingState.svelte';

	export let audioUrl;
	export let isLoading;
	export let onDownloadVoice;
	export let wavesurferComponent;
	export let duration;
	export let currentTime;
	export let isPlaying;
	export let isReady;
	export let formatTime;
	export let onTogglePlayPause;
	export let onSkipBackward;
	export let onSkipForward;
	export let onReady;
	export let onPlay;
	export let onPause;
	export let onAudioProcess;
	export let onSeek;
	export let onFinish;
	export let onError;
</script>

<div
	class="rounded-3xl h-full flex items-center justify-center relative overflow-hidden transition-all duration-300 p-4 {isLoading
		? 'bg-kedua border border-utama animate-pulse'
		: 'bg-black border border-[#444A61]'}"
>
	{#if audioUrl}
		<div class="relative w-full h-full flex items-center justify-center" key={audioUrl}>
			<div class="w-full max-w-2xl text-center" in:fly={{ delay: 100, duration: 400, y: 20 }}>
				<!-- Waveform -->
				<div class="mb-8">
					<WaveformDisplay
						bind:this={wavesurferComponent}
						{audioUrl}
						{onReady}
						{onPlay}
						{onPause}
						{onAudioProcess}
						{onSeek}
						{onFinish}
						{onError}
					/>
				</div>

				<!-- Time Display -->
				<TimeDisplay {currentTime} {duration} {formatTime} />

				<!-- Audio Controls -->
				<AudioControls {isPlaying} {isReady} {onTogglePlayPause} {onSkipBackward} {onSkipForward} />
			</div>

			<!-- Download Button -->
			<DownloadButton onDownload={onDownloadVoice} />
		</div>
	{:else if isLoading}
		<LoadingState />
	{:else}
		<EmptyState />
	{/if}
</div>
