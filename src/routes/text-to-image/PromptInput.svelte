<script>
	import { fly } from 'svelte/transition';

	export let prompt;
	export let isLoading;
	export let onInput;
	export let onKeydown;
</script>

<textarea
	class="mb-6 textarea bg-[#0C0D12] border border-[#444A61] w-full h-44 text-[#ECF2FF] placeholder:text-[#98A7C8] px-7 py-4 rounded-3xl resize-none overflow-y-auto transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
	in:fly={{ delay: 300, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
	placeholder="Describe your image..."
	bind:value={prompt}
	on:input={onInput}
	on:keydown={onKeydown}
	disabled={isLoading}
/>

<style>
	textarea::-webkit-scrollbar {
		width: 8px;
	}

	textarea::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 4px;
	}

	textarea::-webkit-scrollbar-thumb {
		background: #23f784;
		border-radius: 4px;
	}

	textarea::-webkit-scrollbar-thumb:hover {
		background: #1ed670;
	}

	textarea {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
