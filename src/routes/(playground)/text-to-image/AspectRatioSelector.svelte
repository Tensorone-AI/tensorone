<script>
	import { fly } from 'svelte/transition';

	export let aspectRatios;
	export let activeRatio;
	export let isLoading;
	export let onRatioSelect;
</script>

<div
	class="mb-6"
	in:fly={{ delay: 350, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
>
	<h4 class="text-[#ECF2FF] text-xl pb-4">Aspect Ratio</h4>
	<div class="grid grid-cols-3 gap-1">
		{#each aspectRatios as ratio}
			<button
				class="bg-[#0C0D12] border text-center text-[#ECF2FF] px-6 py-1 rounded-full transition-all duration-200 disabled:opacity-50 {activeRatio ===
				ratio.name
					? 'border-utama bg-kedua text-utama'
					: 'border-[#444A61] hover:border-utama'}"
				on:click={() => onRatioSelect(ratio.name)}
				disabled={isLoading}
			>
				{ratio.name}
			</button>
		{/each}
	</div>
</div>
