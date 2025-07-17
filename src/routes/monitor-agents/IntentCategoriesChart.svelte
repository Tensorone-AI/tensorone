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
	<h3 class="text-[#ECF2FF] mb-4">Intent Categories</h3>
	<div class="space-y-3">
		{#if agent}
			{#each data as category}
				<div>
					<div class="flex justify-between text-xs mb-1">
						<span class="text-[#ECF2FF]">{category.name}</span>
						<span class="text-utama">{category.percentage}%</span>
					</div>
					<div class="w-full bg-[#1F222D] rounded-full h-3">
						<div class="bg-utama h-3 rounded-full" style="width: {category.percentage}%"></div>
					</div>
				</div>
			{/each}
		{:else}
			<div class="flex items-center justify-center h-32">
				<span class="text-[#98A7C8] text-sm">No data available</span>
			</div>
		{/if}
	</div>
</div>
