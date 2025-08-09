<script>
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	// Props
	export let isLoading = false;
	export let canProceed = true;
	export let canGoBack = true;
	export let currentComputeUnits = 0;
	export let totalComputeUnits = 0;
	export let newAgentCost = 0;
	export let showComputeUnits = true;
	export let nextButtonText = 'Next';
	export let backButtonText = 'Back';
	export let hasInsufficientComputeUnits = false;
	export let nextButtonClass = 'btn-primary';

	// Event dispatcher
	const dispatch = createEventDispatcher();

	// Handle button clicks
	function handleNext() {
		if (!isLoading && (canProceed || hasInsufficientComputeUnits)) {
			dispatch('next');
		}
	}

	function handleBack() {
		if (!isLoading && canGoBack) {
			dispatch('back');
		}
	}

	// Computed values
	$: computeUnitsDisplay = `${currentComputeUnits + newAgentCost}/${totalComputeUnits}`;
	$: isComputeUnitsExceeded = currentComputeUnits + newAgentCost > totalComputeUnits;
	$: actualCanProceed = hasInsufficientComputeUnits || (canProceed && !isComputeUnitsExceeded);

	// Debug logging - remove this after fixing
	$: console.log('NextAndBackButtons Debug:', {
		canProceed,
		isComputeUnitsExceeded,
		actualCanProceed,
		currentComputeUnits,
		totalComputeUnits,
		newAgentCost,
		isLoading
	});
</script>

<div
	class="mt-8 flex items-center gap-4"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<div class="join flex-1">
		<button
			class="border border-utama join-item hover:bg-transparent hover:border-utama rounded-l-full flex-1 flex items-center justify-end gap-2 px-4 py-2.5 hover:opacity-70 transition-all duration-200"
			class:opacity-50={!canGoBack || isLoading}
			class:cursor-not-allowed={!canGoBack || isLoading}
			data-testid="back-button"
			disabled={!canGoBack || isLoading}
			on:click={handleBack}
		>
			{#if isLoading}
				<div class="loading loading-spinner loading-xs"></div>
			{:else}
				<svg
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M12 19L12 5"
						stroke="#ECF2FF"
						style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M5 12L12 5L19 12"
						stroke="#ECF2FF"
						style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			{/if}
			<span class="text-[#ECF2FF] text-base font-medium">{backButtonText}</span>
		</button>
		<button
			class="border border-utama join-item hover:border-utama rounded-r-full flex-1 flex items-center justify-start gap-2 px-4 py-2.5 hover:opacity-70 transition-all duration-200 disabled:hover:opacity-50"
			class:opacity-50={!actualCanProceed || isLoading}
			class:cursor-not-allowed={!actualCanProceed || isLoading}
			class:bg-kedua={!hasInsufficientComputeUnits}
			class:bg-utama={hasInsufficientComputeUnits}
			class:border-success={hasInsufficientComputeUnits}
			data-testid="next-button"
			disabled={!actualCanProceed || isLoading}
			on:click={handleNext}
		>
			<span
				class="text-base font-medium"
				class:text-black={hasInsufficientComputeUnits}
				class:text-[#ECF2FF]={!hasInsufficientComputeUnits}>{nextButtonText}</span
			>
			{#if isLoading}
				<div class="loading loading-spinner loading-xs"></div>
			{:else if !hasInsufficientComputeUnits}
				<svg
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M12 5L12 19"
						stroke="white"
						style="stroke:white;stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M19 12L12 19L5 12"
						stroke="white"
						style="stroke:white;stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			{/if}
		</button>
	</div>

	{#if showComputeUnits}
		<div
			class="text-[#98A7C8] font-medium bg-[#0C0D12] border border-[#1F222D] py-2.5 px-6 rounded-full"
			class:border-red-500={isComputeUnitsExceeded}
			class:text-red-400={isComputeUnitsExceeded}
			data-testid="compute-units-display"
		>
			Compute Unit: <span class="text-[#ECF2FF]" class:text-red-400={isComputeUnitsExceeded}>
				{computeUnitsDisplay}
			</span>
		</div>
	{/if}
</div>
