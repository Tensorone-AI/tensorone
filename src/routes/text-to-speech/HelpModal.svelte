<script>
	import { fade, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	export let isOpenHelp;
	export let onToggleModal;
</script>

{#if isOpenHelp}
	<div
		class="fixed inset-0 z-[200] flex items-center justify-center px-2"
		transition:fade={{ duration: 200 }}
	>
		<button
			class="absolute inset-0 bg-black bg-opacity-60 backdrop-blur-sm"
			on:click={onToggleModal}
			transition:fade={{ duration: 200 }}
		>
			<div
				class="w-full h-full backdrop-blur-sm transition-all duration-300 ease-in-out"
				style="backdrop-filter: blur(4px);"
			></div>
		</button>
		<div
			class="relative z-10 bg-black rounded-xl shadow-2xl max-w-lg w-full mx-4 border border-[#444A61]"
			transition:scale={{ duration: 200, easing: cubicOut, start: 0.95 }}
		>
			<div
				class="flex items-center justify-between mb-4 bg-[#0C0D12] border-b border-[#444A61] px-4 py-3 rounded-tl-xl rounded-tr-xl"
			>
				<h2 class="text-[#ECF2FF] text-xl font-bold">Voice Clone Help</h2>
				<button class="btn btn-circle btn-ghost btn-sm text-[#ECF2FF]" on:click={onToggleModal}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						class="w-5 h-5"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<div class="px-4">
				<ul class="mt-4 mb-8 text-[#D9E4FF] marker:text-primary list-disc pl-4 space-y-6">
					<li>Audio must be between 60 seconds and 10 minutes in length.</li>
					<li>Audio must contain only human voice throughout its duration.</li>
					<li>Audio must be in .mp3 format.</li>
					<li>
						Audio must be clear, without any background noise, and should not be too loud or too
						quiet.
					</li>
					<li>
						Each user can clone only one voice. <u
							>Cloning a new voice will replace the previously cloned one.</u
						>
					</li>
				</ul>
			</div>
		</div>
	</div>
{/if}
