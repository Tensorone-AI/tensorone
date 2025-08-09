<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	// All props from parent (centralized in +page.svelte)
	export let frameworks;
	export let selectedFramework = null;
	export let selectedFrameworkCost = 0;
	export let isLoading = false;
	export let canProceed = false;
	export let computeUnitsStore = { current: 0, total: 0, available: 0 };
	export let newAgentCost = 0;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Event dispatcher for parent communication
	const dispatch = createEventDispatcher();

	// Simplified event handlers - just dispatch to parent
	function handleFrameworkSelect(framework) {
		dispatch('frameworkSelect', { framework });
	}

	function handleNext() {
		dispatch('next');
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div
	class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<!-- Framework Section Header -->
	<div
		class="mb-4 border-b-2 border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Select Framework</h3>
			<p class="text-base text-[#D9E4FF]">
				Your framework will determine what your AI is built to do. It influences how fast, scalable,
				or flexible your agent can be.
			</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{selectedFrameworkCost} cu</span>
			</p>
		</div>
	</div>

	<!-- Framework Grid -->
	<div class="flex-1 min-h-0 flex flex-col">
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 flex-1 auto-rows-max">
			{#each frameworks as framework, index (framework.id)}
				<div
					class="card card-compact bg-black border-2 border-[#444A61] rounded-md w-full relative overflow-hidden min-h-48 cursor-pointer hover:border-utama transition-colors"
					class:border-utama={selectedFramework?.id === framework.id}
					class:ring-1={selectedFramework?.id === framework.id}
					class:ring-utama={selectedFramework?.id === framework.id}
					data-framework-id={framework.id}
					data-testid="framework-card-{framework.id}"
					in:fly|global={{
						delay: 300 + index * 100,
						duration: 500,
						x: -100,
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
					on:click={() => handleFrameworkSelect(framework)}
					on:keydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							handleFrameworkSelect(framework);
						}
					}}
					role="button"
					tabindex="0"
				>
					<div class="flex flex-col relative z-10">
						<div
							class="flex items-center gap-4 mb-4 px-4 py-5 bg-[#0C0D12] border-b border-[#444A61]"
							class:border-b-utama={selectedFramework?.id === framework.id}
							class:bg-kedua={selectedFramework?.id === framework.id}
						>
							<input
								type="radio"
								name="framework"
								class="radio radio-sm radio-primary border-[#444A61]"
								checked={selectedFramework?.id === framework.id}
								data-testid="framework-radio-{framework.id}"
								on:change={() => handleFrameworkSelect(framework)}
							/>
							<img src={framework.logo} alt={framework.name} />
							{#if framework.name !== 'LangChain'}
								<h2 class="text-xl text-[#ECF2FF] font-bold">{framework.name}</h2>
							{/if}
						</div>
						<!-- Framework Description -->
						<div class="px-4 pb-4 space-y-4 text-base text-[#ECF2FF] flex-grow">
							<p>
								<span class="font-bold">Best for</span>: {framework.bestFor}
							</p>
							<p>
								<span class="font-bold">Downside</span>: {framework.downside}
							</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Next/Back Buttons -->
	<NextAndBackButtons
		{isLoading}
		{canProceed}
		canGoBack={true}
		currentComputeUnits={computeUnitsStore.current}
		totalComputeUnits={computeUnitsStore.total}
		{newAgentCost}
		showComputeUnits={true}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>
