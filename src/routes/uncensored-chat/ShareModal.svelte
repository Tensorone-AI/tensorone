<script>
	import { fade, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	export let isOpen;
	export let shareableID;
	export let onClose;
	export let onCopyLink;

	let isCopied = false;

	function handleCopyLink() {
		onCopyLink();
		isCopied = true;
		setTimeout(() => {
			isCopied = false;
		}, 2000);
	}
</script>

{#if isOpen}
	<div
		class="fixed inset-0 z-[200] flex items-center justify-center px-2"
		transition:fade={{ duration: 200 }}
	>
		<button
			class="absolute inset-0 bg-black bg-opacity-60 backdrop-blur-sm"
			on:click={onClose}
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
				class="flex justify-between items-center mb-4 bg-[#0C0D12] border-b border-[#444A61] px-4 py-3 rounded-tl-xl rounded-tr-xl"
			>
				<div class="text-[#ECF2FF] font-bold">Copy link to chat</div>
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
			{#if shareableID && shareableID.length !== 0}
				<div class="pt-4 pb-8 px-4">
					<div class="relative">
						<div
							class="text-[#BBD0FF] font-medium border border-[#343434] rounded-full bg-[#070707] pl-3 sm:pr-40 pr-24 py-3 truncate"
						>
							https://shareable.tensorone.ai/{encodeURIComponent(shareableID)}
						</div>
						<button
							class="btn btn-primary btn-sm rounded-full font-normal absolute right-3 top-2 hover:opacity-70"
							on:click={handleCopyLink}
						>
							{isCopied ? 'Copied' : 'Copy Link'}
						</button>
					</div>
				</div>
			{:else}
				<div class="text-center text-[#ECF2FF] pt-4 pb-8">Nothing to share</div>
			{/if}
		</div>
	</div>
{/if}
