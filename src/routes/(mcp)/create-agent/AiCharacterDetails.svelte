<script>
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	const dispatch = createEventDispatcher();

	// Props from parent - now includes all data and calculations
	export let characterDetails = {};
	export let characterDetailsCost = 0;
	export let memoryFrequencies = [];
	export let agentTones = [];
	export let isCharacterDetailsFormValid = false;
	export let isLoading = false;
	export let canProceed = true;
	export let computeUnitsStore = { current: 0, total: 0 };
	export let newAgentCost = 0;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Local reactive reference to characterDetails for binding
	$: characterData = characterDetails;

	// Function to update character details
	function updateCharacterDetails() {
		dispatch('characterDetailsUpdate', characterData);
	}

	// Event handlers
	function handleNext() {
		if (isCharacterDetailsFormValid) {
			updateCharacterDetails();
			dispatch('next');
		}
	}

	function handleBack() {
		updateCharacterDetails();
		dispatch('back');
	}

	// Handle input changes
	function handleInputChange() {
		updateCharacterDetails();
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
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Character Details</h3>
			<p class="text-base text-[#D9E4FF]">Customize your agent's personality</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{characterDetailsCost} cu</span>
			</p>
		</div>
	</div>

	<div class="flex-1 min-h-0 flex flex-col">
		<div class="flex items-center gap-6 mb-4 pb-4 border-b border-[#1F222D] w-full flex-1">
			<div class="flex flex-col gap-4 w-1/4">
				<span class="text-[#ECF2FF] text-xl">Name</span>
				<input
					type="text"
					placeholder="Enter agent name..."
					bind:value={characterData.name}
					on:input={handleInputChange}
					class="input input-md bg-[#0C0D12] border border-[#444A61] text-[#ECF2FF] text-lg placeholder:text-[#98A7C8] rounded-full transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
				/>
			</div>
			<div class="flex flex-col gap-4 w-3/4">
				<span class="text-[#ECF2FF] text-xl">Description</span>
				<input
					type="text"
					placeholder="Describe your agent..."
					bind:value={characterData.description}
					on:input={handleInputChange}
					class="input input-md bg-[#0C0D12] border border-[#444A61] text-[#ECF2FF] text-lg placeholder:text-[#98A7C8] rounded-full transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
				/>
			</div>
		</div>

		<div class="mb-4 pb-4 border-b border-[#1F222D]">
			<h4 class="text-[#ECF2FF] text-xl mb-4">Memory</h4>
			<div class="grid grid-cols-2 gap-2 w-full">
				<div class="space-y-3">
					<div class="flex items-center gap-4">
						<input
							type="checkbox"
							bind:checked={characterData.memory.enableMemory}
							on:change={handleInputChange}
							class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
						/>
						<div class="text-[#ECF2FF]">
							<p>Enable Memory</p>
							<p class="text-sm text-[#98A7C8]">Allow agent to save and reference memories</p>
						</div>
					</div>
					<div
						class="flex items-center gap-4 transition-opacity duration-200"
						class:opacity-40={!characterData.memory.enableMemory}
						class:opacity-100={characterData.memory.enableMemory}
					>
						<input
							type="checkbox"
							bind:checked={characterData.memory.referenceSavedMemories}
							disabled={!characterData.memory.enableMemory}
							on:change={handleInputChange}
							class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
						/>
						<div class="text-[#ECF2FF]">
							<p>Reference Saved Memories</p>
							<p class="text-sm text-[#98A7C8]">Let agent save and use memories when responding</p>
						</div>
					</div>
					<div
						class="flex items-center gap-4 transition-opacity duration-200"
						class:opacity-40={!characterData.memory.enableMemory}
						class:opacity-100={characterData.memory.enableMemory}
					>
						<input
							type="checkbox"
							bind:checked={characterData.memory.referenceChatHistory}
							disabled={!characterData.memory.enableMemory}
							class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
						/>
						<div class="text-[#ECF2FF]">
							<p>Reference Chat History</p>
							<p class="text-sm text-[#98A7C8]">Let agent save and use memories when responding</p>
						</div>
					</div>
					<div
						class="flex items-center gap-4 transition-opacity duration-200"
						class:opacity-40={!characterData.memory.enableMemory}
						class:opacity-100={characterData.memory.enableMemory}
					>
						<input
							type="checkbox"
							bind:checked={characterData.memory.shareDataToUs}
							disabled={!characterData.memory.enableMemory}
							on:change={handleInputChange}
							class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
						/>
						<div class="text-[#ECF2FF]">
							<p>Share Data to Us</p>
							<p class="text-sm text-[#98A7C8]">Help us improve our AI Model</p>
						</div>
					</div>
				</div>
				<div
					class="transition-opacity duration-200"
					class:opacity-40={!characterData.memory.enableMemory}
					class:opacity-100={characterData.memory.enableMemory}
				>
					<div class="space-y-2">
						<label for="frequency-select" class="text-[#ECF2FF]">Frequency</label>
						<select
							id="frequency-select"
							bind:value={characterData.memory.frequency}
							disabled={!characterData.memory.enableMemory}
							on:change={handleInputChange}
							class="select select-sm text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full w-full focus:border-utama focus:outline-none transition-colors duration-200"
							class:text-[#98A7C8]={!characterData.memory.frequency}
							class:text-[#D9E4FF]={characterData.memory.frequency}
							aria-label="Select frequency type"
						>
							<option value="" disabled hidden>Choose Frequency</option>
							{#each memoryFrequencies as frequency}
								<option value={frequency.id}>{frequency.name}</option>
							{/each}
						</select>
					</div>
				</div>
			</div>
		</div>

		<div>
			<h4 class="text-[#ECF2FF] text-xl mb-4">Personalization</h4>
			<div class="grid grid-cols-2 gap-8 w-full">
				<div class="flex flex-col gap-4">
					<span class="text-[#ECF2FF]">Your Name</span>
					<input
						type="text"
						placeholder="What should the agent call you?"
						bind:value={characterData.personalization.userName}
						on:input={handleInputChange}
						class="input input-sm bg-[#0C0D12] border border-[#444A61] text-[#ECF2FF] text-sm py-4 placeholder:text-[#98A7C8] rounded-full transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
					/>
				</div>
				<div class="space-y-4">
					<label for="style-select" class="text-[#ECF2FF]">Agent Tone</label>
					<select
						id="style-select"
						bind:value={characterData.personalization.agentTone}
						on:change={handleInputChange}
						class="select select-sm text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full w-full focus:border-utama focus:outline-none transition-colors duration-200"
						class:text-[#98A7C8]={!characterData.personalization.agentTone}
						class:text-[#D9E4FF]={characterData.personalization.agentTone}
						aria-label="Select style type"
					>
						<option value="" disabled hidden>Choose Agent Tone</option>
						{#each agentTones as tone}
							<option value={tone.id}>{tone.name}</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</div>

	<!-- Next/Back Buttons -->
	<NextAndBackButtons
		{isLoading}
		canProceed={canProceed && isCharacterDetailsFormValid}
		canGoBack={true}
		currentComputeUnits={computeUnitsStore.current}
		totalComputeUnits={computeUnitsStore.total}
		{newAgentCost}
		showComputeUnits={true}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		backButtonText="Back"
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>

<style>
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
	.select {
		--select-option-bg: #000000;
	}

	select option {
		background-color: var(--select-option-bg);
		color: white;
		padding: 8px 12px;
	}

	select option:hover,
	select option:focus {
		background-color: #23f784;
		color: black;
	}

	select option:checked {
		background-color: #23f784;
		color: black;
	}

	/* Custom scrollbar for select dropdowns */
	select::-webkit-scrollbar {
		width: 8px;
	}

	select::-webkit-scrollbar-track {
		background: #1a1a1a;
	}

	select::-webkit-scrollbar-thumb {
		background: #23f784;
		border-radius: 4px;
	}
</style>
