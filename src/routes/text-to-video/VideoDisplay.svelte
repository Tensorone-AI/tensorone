<script>
	import { fly } from 'svelte/transition';

	export let video;
	export let videoElement;
	export let onTimeUpdate;
	export let onLoadedMetadata;
	export let onPlay;
	export let onPause;
</script>

<div class="flex-1 relative rounded-2xl overflow-hidden bg-black">
	<video
		bind:this={videoElement}
		src={video.url}
		class="w-full h-full object-contain"
		preload="metadata"
		in:fly={{ delay: 100, duration: 400, y: 20 }}
		on:timeupdate={onTimeUpdate}
		on:loadedmetadata={onLoadedMetadata}
		on:play={onPlay}
		on:pause={onPause}
		on:loadstart={() => console.log('Video loading started')}
		on:loadeddata={() => console.log('Video loaded')}
		on:error={(e) => console.error('Video error:', e)}
	>
		<track kind="captions" />
	</video>
</div>
