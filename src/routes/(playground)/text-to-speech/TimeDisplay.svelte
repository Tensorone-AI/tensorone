<script>
	export let currentTime;
	export let duration;
	export let formatTime;
</script>

<div class="flex items-center justify-center gap-2 mb-6 text-[#D9E4FF] text-sm">
	<span>{formatTime(currentTime)}</span>
	<span class="text-[#98A7C8]">/</span>
	<span>{formatTime(duration)}</span>
</div>
