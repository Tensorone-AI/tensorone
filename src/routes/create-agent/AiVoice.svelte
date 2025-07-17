<script>
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	// All props from parent (centralized in +page.svelte)
	export let voices;
	export let tempoOptions;
	export let styleOptions;
	export let isVoiceEnabled;
	export let selectedTempo;
	export let selectedStyle;
	export let totalVoiceCost;
	export let isLoading = false;
	export let canProceed = false;
	export let computeUnitsStore = { current: 0, total: 0 };
	export let newAgentCost = 0;
	export let isVoiceSelected = () => {};
	export let handlePlayVoice = () => {};
	export let currentPlayingVoice = null;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Event dispatcher for parent communication
	const dispatch = createEventDispatcher();

	// Simplified event handlers - just dispatch to parent
	function handleVoiceToggle(enabled) {
		dispatch('voiceToggle', { enabled });
	}

	function handleVoiceSelect(voiceId) {
		if (isVoiceEnabled) {
			dispatch('voiceIdSelect', { voiceId });
		}
	}

	function handleTempoChange(event) {
		if (isVoiceEnabled) {
			dispatch('tempoChange', { tempo: event.target.value });
		}
	}

	function handleStyleChange(event) {
		if (isVoiceEnabled) {
			dispatch('styleChange', { style: event.target.value });
		}
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
	<div
		class="mb-4 border-b border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Select Voice</h3>
			<p class="text-base text-[#D9E4FF]">Select your agent's speaking voice.</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{totalVoiceCost} cu</span>
			</p>
		</div>
	</div>

	<div class="flex-1 min-h-0 flex flex-col">
		<!-- Voice Enable Toggle -->
		<div class="flex items-center gap-4 mb-4 pb-4 border-b border-[#1F222D]">
			<input
				type="checkbox"
				class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
				checked={isVoiceEnabled}
				data-testid="voice-enable-toggle"
				on:change={(e) => handleVoiceToggle(e.target.checked)}
			/>
			<span class="text-[#ECF2FF]">Enable Voice</span>
		</div>

		<!-- Voice Selection -->
		<div
			class="space-y-4 mb-6 pb-6 border-b border-[#1F222D] transition-opacity duration-300"
			class:opacity-40={!isVoiceEnabled}
		>
			{#each voices as category (category.category)}
				<div class="flex items-center gap-4">
					<span class="text-[#ECF2FF] min-w-[73px] capitalize">{category.category}</span>
					<div class="grid grid-cols-3 gap-4 w-full">
						{#each category.voices as voice (voice.id)}
							{@const isSelected = isVoiceSelected(voice.id)}
							{@const isCurrentlyPlaying = currentPlayingVoice === voice.id}
							<div
								class="bg-[#0C0D12] border border-[#444A61] rounded-md p-3 flex items-center justify-between transition-colors"
								class:cursor-pointer={isVoiceEnabled}
								class:cursor-not-allowed={!isVoiceEnabled}
								class:hover:border-utama={isVoiceEnabled}
								class:border-utama={isSelected}
								class:ring-1={isSelected}
								class:ring-utama={isSelected}
								class:bg-kedua={isSelected}
								data-voice-id={voice.id}
								data-testid="voice-option-{voice.id}"
								on:click={() => handleVoiceSelect(voice.id)}
								on:keydown={(e) => {
									if (isVoiceEnabled && (e.key === 'Enter' || e.key === ' ')) {
										e.preventDefault();
										handleVoiceSelect(voice.id);
									}
								}}
								role="button"
								tabindex={isVoiceEnabled ? '0' : '-1'}
							>
								<div class="flex items-center gap-2">
									<input
										type="radio"
										name="voice"
										value={voice.id}
										class="radio radio-sm radio-primary border-[#444A61]"
										checked={isSelected}
										disabled={!isVoiceEnabled}
										data-testid="voice-radio-{voice.id}"
										on:change={() => handleVoiceSelect(voice.id)}
									/>
									<span class="text-[#ECF2FF]">{voice.name}</span>
								</div>
								<button
									class="transition-opacity relative"
									class:hover:opacity-70={isVoiceEnabled}
									class:cursor-not-allowed={!isVoiceEnabled}
									class:opacity-60={isCurrentlyPlaying}
									disabled={!isVoiceEnabled}
									data-testid="play-voice-{voice.id}"
									on:click|stopPropagation={() => handlePlayVoice(voice.id)}
								>
									{#if isCurrentlyPlaying}
										<!-- Playing indicator with pulse animation -->
										<svg
											width="17"
											height="20"
											viewBox="0 0 17 20"
											fill="none"
											xmlns="http://www.w3.org/2000/svg"
											class="animate-pulse"
										>
											<path
												d="M1.66602 1L15.666 10L1.66602 19V1Z"
												stroke="#23f784"
												fill="#23f784"
												style="stroke:#23f784;stroke:color(display-p3 0.1386 0.9686 0.5176);stroke-opacity:1;"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
										</svg>
									{:else}
										<!-- Default play icon -->
										<svg
											width="17"
											height="20"
											viewBox="0 0 17 20"
											fill="none"
											xmlns="http://www.w3.org/2000/svg"
										>
											<path
												d="M1.66602 1L15.666 10L1.66602 19V1Z"
												stroke="#D9E4FF"
												style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
										</svg>
									{/if}
								</button>
							</div>
						{/each}
					</div>
				</div>
			{/each}
		</div>

		<!-- Tempo and Style Selection -->
		<div
			class="grid grid-cols-2 gap-8 w-full transition-opacity duration-300"
			class:opacity-40={!isVoiceEnabled}
		>
			<div class="space-y-4">
				<label for="tempo-select" class="text-[#ECF2FF] text-xl">Tempo</label>
				<select
					id="tempo-select"
					class="select select-sm text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full w-full focus:border-utama focus:outline-none transition-colors duration-200"
					class:text-[#D9E4FF]={selectedTempo && selectedTempo !== ''}
					class:text-[#98A7C8]={!selectedTempo || selectedTempo === ''}
					class:cursor-not-allowed={!isVoiceEnabled}
					aria-label="Select tempo type"
					value={selectedTempo}
					disabled={!isVoiceEnabled}
					data-testid="tempo-select"
					on:change={handleTempoChange}
				>
					<option value="" disabled hidden>Choose Tempo</option>
					{#each tempoOptions as tempo (tempo.id)}
						<option value={tempo.id}>{tempo.name}</option>
					{/each}
				</select>
			</div>
			<div class="space-y-4">
				<label for="style-select" class="text-[#ECF2FF] text-xl">Style</label>
				<select
					id="style-select"
					class="select select-sm text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full w-full focus:border-utama focus:outline-none transition-colors duration-200"
					class:text-[#D9E4FF]={selectedStyle && selectedStyle !== ''}
					class:text-[#98A7C8]={!selectedStyle || selectedStyle === ''}
					class:cursor-not-allowed={!isVoiceEnabled}
					aria-label="Select style type"
					value={selectedStyle}
					disabled={!isVoiceEnabled}
					data-testid="style-select"
					on:change={handleStyleChange}
				>
					<option value="" disabled hidden>Choose Style</option>
					{#each styleOptions as style (style.id)}
						<option value={style.id}>{style.name}</option>
					{/each}
				</select>
			</div>
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

<style>
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
