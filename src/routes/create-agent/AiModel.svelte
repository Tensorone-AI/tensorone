<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	// All props from parent (centralized in +page.svelte)
	export let aiModels;
	export let selectedModelCost = 0;
	export let selectedRadioValue = null;
	export let isLoading = false;
	export let canProceed = false;
	export let computeUnitsStore = { current: 0, total: 0, available: 0 };
	export let newAgentCost = 0;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Event dispatcher for parent communication
	const dispatch = createEventDispatcher();

	// Handle radio value changes and dispatch to parent
	function handleRadioChange(event) {
		const newValue = event.target.value;
		dispatch('radioValueChange', { radioValue: newValue });
	}

	// Simplified event handlers - just dispatch to parent
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
		class="mb-4 border-b-2 border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Select Model</h3>
			<p class="text-base text-[#D9E4FF]">
				Select your agent's language model for content analysis and text output.
			</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{selectedModelCost} cu</span>
			</p>
		</div>
	</div>

	<!-- AI Model Grid -->
	<div class="flex-1 min-h-0 flex flex-col">
		<div class="flex flex-col sm:flex-row gap-4 flex-1 items-stretch">
			{#each aiModels as provider, index (provider.id)}
				<div
					class="flex flex-col bg-[#06070A] border border-[#444A61] rounded-md flex-1 min-h-full relative overflow-hidden"
					data-provider-id={provider.id}
					data-testid="provider-card-{provider.id}"
					in:fly|global={{
						delay: 300 + index * 100,
						duration: 500,
						x: -100,
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
				>
					<div class="flex flex-col relative z-10 h-full">
						<!-- AI Model Header -->
						<div
							class="flex items-center gap-4 mb-4 px-4 py-5 bg-[#0C0D12] border-b border-[#444A61]"
						>
							<img src={provider.logo} alt={provider.name} />
							{#if provider.name !== 'Google' && provider.name !== 'Anthropic'}
								<h2 class="text-xl text-[#D9E4FF] font-semibold">{provider.name}</h2>
							{/if}
						</div>

						<!-- Model Radio Options -->
						<div class="px-4 pb-4 space-y-4 text-base text-[#ECF2FF] flex-1">
							{#each provider.models as model (model.id)}
								{@const radioValue = `${provider.id}-${model.id}`}
								{@const isSelected = selectedRadioValue === radioValue}
								<label
									class="flex items-center gap-2 bg-[#0C0D12] border border-[#1F222D] rounded-md p-2 cursor-pointer hover:border-utama transition-colors"
									class:ring-1={isSelected}
									class:ring-utama={isSelected}
									class:bg-kedua={isSelected}
									data-model-id={model.id}
									data-testid="model-option-{provider.id}-{model.id}"
								>
									<input
										id="model-{provider.id}-{model.id}"
										type="radio"
										name="aiModel"
										value={radioValue}
										checked={selectedRadioValue === radioValue}
										class="radio radio-sm radio-primary border-[#444A61]"
										data-testid="model-radio-{provider.id}-{model.id}"
										on:change={handleRadioChange}
									/>
									<span class="flex-grow">{model.name}</span>
								</label>
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
		currentComputeUnits={computeUnitsStore?.current || 0}
		totalComputeUnits={computeUnitsStore?.total || 0}
		{newAgentCost}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>
