<script>
	import { fade, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	export let isOpen;
	export let itemToDelete;
	export let onClose;
	export let onDelete;
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
				class="mb-4 bg-[#0C0D12] border-b border-[#444A61] px-4 py-3 rounded-tl-xl rounded-tr-xl text-[#ECF2FF] font-bold"
			>
				Delete Chat?
			</div>
			<div class="pt-2 pb-6 px-4 space-y-6">
				<div class="text-[#ECF2FF] font-medium">
					This will delete <span
						class="break-all truncate lg:max-w-[200px] max-w-[150px] inline-block align-bottom"
						title={itemToDelete.title}>"{itemToDelete.title}"</span
					>
				</div>
				<div class="flex gap-2">
					<button
						class="btn btn-sm bg-[#1F222D] hover:bg-[#1F222D] border border-[#444A61] hover:border-[#444A61] rounded-full text-[#ECF2FF] font-normal hover:opacity-70"
						on:click={onClose}>Back</button
					>
					<button
						class="btn btn-sm btn-primary text-kedua rounded-full font-normal hover:opacity-70"
						on:click={onDelete}>Delete</button
					>
				</div>
			</div>
		</div>
	</div>
{/if}
