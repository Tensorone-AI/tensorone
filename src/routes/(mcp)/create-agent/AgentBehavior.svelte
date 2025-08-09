<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	const dispatch = createEventDispatcher();

	// Props from parent component (all logic moved to parent)
	export let behaviorSelections = {};
	export let behaviorCategories = [];
	export let isLoading = false;
	export let canProceed = true;
	export let computeUnitsStore = { current: 0, total: 0 };
	export let newAgentCost = 0;
	export let capitalize = () => {}; // Function passed from parent
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Function to handle option selection
	function selectOption(categoryId, optionKey, selectedValue) {
		dispatch('behaviorSelectionUpdate', { categoryId, optionKey, selectedValue });
	}

	// Event handlers for NextAndBackButtons
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
	<div
		class="mb-4 border-b border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Agent Behavior</h3>
			<p class="text-base text-[#D9E4FF]">
				Customize how your agent interacts with its environment and responds to input.
			</p>
		</div>
	</div>

	<!-- Behavior Grid -->
	<div class="flex-1 min-h-0 flex flex-col">
		<div class="grid gap-4 sm:grid-cols-3">
			{#each behaviorCategories as category, categoryIndex}
				<div
					class="card card-compact bg-[#06070A] border border-[#444A61] rounded-md w-full relative overflow-hidden min-h-48"
					in:fly|global={{
						delay: 300 + categoryIndex * 50,
						duration: 500,
						x: -100,
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
				>
					<div class="flex flex-col relative z-10">
						<!-- Behavior Header -->
						<div
							class="flex items-center gap-3 mb-4 px-4 py-5 bg-[#0C0D12] border-b border-[#444A61]"
						>
							<img src={category.icon} alt="Icon" />
							<h2 class="text-xl text-[#ECF2FF]">{category.name}</h2>
						</div>

						<div class="px-4 pb-2 space-y-4">
							{#each category.options as option}
								<div class="relative flex bg-black border border-[#444A61] rounded-full">
									<!-- Sliding background indicator -->
									<div
										class="absolute top-0 bottom-0 w-1/2 bg-kedua border border-utama rounded-full transition-transform duration-300 ease-out"
										style="transform: translateX({behaviorSelections[category.id]?.[option.key] ===
										option.options[0]
											? '0%'
											: '100%'})"
									></div>
									<!-- Buttons -->
									{#each option.options as optionValue, index}
										<button
											class="relative z-10 flex-1 py-2 px-4 text-[#ECF2FF] rounded-full font-medium transition-all duration-300 ease-out"
											class:opacity-75={behaviorSelections[category.id]?.[option.key] !==
												optionValue}
											on:click={() => selectOption(category.id, option.key, optionValue)}
										>
											{capitalize(optionValue.replace('-', ' '))}
										</button>
									{/each}
								</div>
							{/each}
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
		currentComputeUnits={computeUnitsStore.current}
		totalComputeUnits={computeUnitsStore.total}
		{newAgentCost}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>
