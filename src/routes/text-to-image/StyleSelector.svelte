<script>
	import { fly } from 'svelte/transition';

	export let modelOptions;
	export let selectedModel;
	export let isLoading;
	export let onModelChange;
</script>

<div
	class="mb-6"
	in:fly={{ delay: 450, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
>
	<h4 class="text-[#ECF2FF] text-xl pb-4">Style</h4>
	<select
		class="select select-sm text-[#D9E4FF] bg-[#0C0D12] border border-[#444A61] w-full rounded-full focus:border-utama focus:outline-none transition-colors duration-200"
		bind:value={selectedModel}
		on:change={onModelChange}
		disabled={isLoading}
	>
		<option value="" disabled hidden>Select a Style</option>
		{#each modelOptions as { label, modelName }}
			<option value={modelName}>{label}</option>
		{/each}
	</select>
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
