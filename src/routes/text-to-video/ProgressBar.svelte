<script>
	export let currentTime;
	export let duration;
	export let progressPercentage;
	export let onProgressClick;
	export let onProgressMouseDown;
	export let skipBackward;
	export let skipForward;
</script>

<div class="mb-6">
	<button
		class="w-full h-1 bg-[#444A61] rounded-full cursor-pointer relative block border-none p-0"
		on:click={onProgressClick}
		on:mousedown={onProgressMouseDown}
		on:keydown={(e) => {
			if (e.key === 'ArrowLeft') {
				skipBackward();
			} else if (e.key === 'ArrowRight') {
				skipForward();
			}
		}}
		aria-label="Video progress bar"
		aria-valuemin="0"
		aria-valuemax={duration || 100}
		aria-valuenow={currentTime || 0}
		role="slider"
	>
		<div
			class="h-full bg-utama rounded-full transition-all duration-150 ease-out pointer-events-none"
			style="width: {progressPercentage}%"
		></div>
		<div
			class="absolute top-1/2 w-4 h-4 bg-[#0C0D12] border-4 border-utama rounded-full transform -translate-y-1/2 pointer-events-none"
			style="left: calc({progressPercentage}% - 8px)"
		></div>
	</button>
</div>
