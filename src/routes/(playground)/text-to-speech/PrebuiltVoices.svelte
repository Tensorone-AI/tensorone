<script>
	import { fly } from 'svelte/transition';

	export let prebuiltVoices;
	export let selectedVoiceType;
	export let selectedPrebuiltVoice;
	export let currentPlayingVoice;
	export let onSelectVoice;
	export let onPlaySample;
</script>

<div
	class="mb-6"
	in:fly={{ delay: 450, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
>
	<h4 class="text-[#ECF2FF] text-xl pb-4">Prebuilt Voice</h4>
	<div class="grid grid-cols-3 gap-3">
		{#each prebuiltVoices as voice}
			<div
				class="border transition-colors rounded-md p-3 flex items-center justify-between cursor-pointer hover:border-utama"
				class:bg-kedua={selectedVoiceType === 'prebuilt' && selectedPrebuiltVoice === voice.id}
				class:border-utama={selectedVoiceType === 'prebuilt' && selectedPrebuiltVoice === voice.id}
				class:bg-[#0C0D12]={!(
					selectedVoiceType === 'prebuilt' && selectedPrebuiltVoice === voice.id
				)}
				class:border-[#444A61]={!(
					selectedVoiceType === 'prebuilt' && selectedPrebuiltVoice === voice.id
				)}
				on:click={() => onSelectVoice(voice.id)}
				role="button"
				tabindex="0"
				on:keydown={(e) => e.key === 'Enter' && onSelectVoice(voice.id)}
			>
				<div class="flex items-center gap-2">
					<input
						type="radio"
						name="voice"
						value={voice.id}
						checked={selectedVoiceType === 'prebuilt' && selectedPrebuiltVoice === voice.id}
						on:change={() => onSelectVoice(voice.id)}
						class="radio radio-sm radio-primary border-[#444A61] pointer-events-none"
					/>
					<span class="text-[#ECF2FF]">{voice.name}</span>
				</div>
				<button
					type="button"
					on:click|stopPropagation={() => onPlaySample(voice.id)}
					class="transition-opacity hover:opacity-70 relative"
					class:opacity-60={currentPlayingVoice === voice.id}
				>
					{#if currentPlayingVoice === voice.id}
						<!-- Playing indicator -->
						<svg
							width="16"
							height="20"
							viewBox="0 0 16 20"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
							class="animate-pulse"
						>
							<path
								d="M1 1L15 10L1 19V1Z"
								stroke="#23f784"
								fill="#23f784"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
					{:else}
						<!-- Default play icon -->
						<svg
							width="16"
							height="20"
							viewBox="0 0 16 20"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M1 1L15 10L1 19V1Z"
								stroke="#D9E4FF"
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
