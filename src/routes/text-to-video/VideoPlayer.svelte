<script>
	// Import sub-components
	import VideoDisplay from './VideoDisplay.svelte';
	import VideoControls from './VideoControls.svelte';
	import ProgressBar from './ProgressBar.svelte';
	import ActionButtons from './ActionButtons.svelte';

	export let video;
	export let videoElement;
	export let isPlaying;
	export let currentTime;
	export let duration;
	export let progressPercentage;
	export let onTimeUpdate;
	export let onLoadedMetadata;
	export let onPlay;
	export let onPause;
	export let onProgressClick;
	export let onProgressMouseDown;
	export let togglePlay;
	export let skipBackward;
	export let skipForward;
	export let toggleFullscreen;
	export let downloadVideo;
</script>

<div class="relative w-full h-full flex flex-col" key={video.url}>
	<!-- Video Container -->
	<VideoDisplay {video} bind:videoElement {onTimeUpdate} {onLoadedMetadata} {onPlay} {onPause} />

	<!-- Custom Video Controls -->
	<div class="mt-4">
		<!-- Control Buttons -->
		<VideoControls {isPlaying} {togglePlay} {skipBackward} {skipForward} />

		<!-- Progress Bar -->
		<ProgressBar
			{currentTime}
			{duration}
			{progressPercentage}
			{onProgressClick}
			{onProgressMouseDown}
			{skipBackward}
			{skipForward}
		/>

		<!-- Action Buttons -->
		<ActionButtons {toggleFullscreen} {downloadVideo} />
	</div>
</div>
