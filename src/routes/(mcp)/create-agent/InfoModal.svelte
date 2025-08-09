<script>
	import { fade, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	export let isOpen = false;
	export let server = null;
	export let onClose;
</script>

{#if isOpen && server}
	<div
		class="fixed inset-0 z-[200] flex items-center justify-center px-2"
		transition:fade={{ duration: 200 }}
	>
		<button
			class="absolute inset-0 bg-black bg-opacity-60 backdrop-blur-sm"
			on:click={onClose}
			transition:fade={{ duration: 200 }}
		>
		</button>
		<div
			class="relative z-10 bg-black rounded-xl shadow-2xl max-w-lg w-full mx-4 border border-[#444A61]"
			transition:scale={{ duration: 200, easing: cubicOut, start: 0.95 }}
		>
			<!-- Header -->
			<div
				class="flex items-center justify-between mb-4 bg-[#0C0D12] border-b border-[#444A61] px-4 py-3 rounded-tl-xl rounded-tr-xl"
			>
				<h2 class="text-[#ECF2FF] text-xl font-bold">{server.name}</h2>
				<button class="btn btn-circle btn-ghost btn-sm text-[#ECF2FF]" on:click={onClose}>
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

			<!-- Server Details -->
			<div class="space-y-6 pt-4 pb-8 px-4">
				<!-- Description -->
				<div>
					<h3 class="text-lg font-medium text-[#ECF2FF] mb-3">Description</h3>
					<p class="text-[#D9E4FF] leading-relaxed">
						{server.description}
					</p>
				</div>

				<!-- Cost Information -->
				<div class="bg-[#070707] rounded-full p-4 border border-[#343434]">
					<div class="flex items-center justify-between">
						<span class="text-[#BBD0FF] font-medium">Compute Unit Cost</span>
						<span class="text-utama">{server.cost} cu</span>
					</div>
				</div>

				<!-- Server ID (for debugging/technical info) -->
				<div>
					<h3 class="text-sm font-medium text-gray-400 mb-2">Server ID</h3>
					<code
						class="text-xs text-gray-500 bg-[#FFFFFF08] px-2 py-1 rounded border border-[#FFFFFF10]"
					>
						{server.id}
					</code>
				</div>

				<!-- Additional Features/Capabilities -->
				<div>
					<h3 class="text-lg font-medium text-[#ECF2FF] mb-3">Key Features</h3>
					<div class="space-y-2">
						{#each server.features as feature}
							<div class="flex items-start gap-3 text-[#D9E4FF]">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0"
								>
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
								<span class="text-sm leading-relaxed">{feature}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
