<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let data = [];
	export let agent = null;
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6"
	in:fly|global={{ delay: 600, duration: 150, x: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Response Time Distribution</h3>
	{#if agent}
		<div class="flex items-end space-x-1 h-32 mb-2 mt-auto">
			{#each data as timeRange}
				<div
					class="flex-1 bg-[#1F222D] rounded flex items-end justify-center"
					style="height: {(timeRange.count / 100) * 100}%"
				>
					<div class="w-full h-full bg-utama rounded"></div>
				</div>
			{/each}
		</div>
		<div class="grid grid-cols-5 gap-1 text-xs text-[#ECF2FF]">
			{#each data as timeRange}
				<div class="text-center">{timeRange.range}</div>
			{/each}
		</div>
	{:else}
		<div class="flex items-center justify-center h-52">
			<span class="text-[#98A7C8] text-sm">No data available</span>
		</div>
	{/if}
</div>
