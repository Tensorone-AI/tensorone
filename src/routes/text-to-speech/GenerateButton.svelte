<script>
	import { fly } from 'svelte/transition';

	export let canGenerate;
	export let isLoading;
	export let onGenerate;
</script>

<button
	type="button"
	on:click={onGenerate}
	disabled={!canGenerate}
	in:fly={{ delay: 500, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
	class="btn btn-primary rounded-full mt-6 w-full text-kedua hover:opacity-70 disabled:text-[#BBD0FF] disabled:bg-[#1F222D] disabled:border-[#1F222D] disabled:opacity-70 disabled:cursor-not-allowed"
>
	{#if isLoading}
		<span class="text-base font-normal generating-text">Generating</span>
	{:else}
		<span class="text-base font-normal">Generate</span>
		<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M11.3529 1L12.8782 5.12184L17 6.64706L12.8782 8.17228L11.3529 12.2941L9.82772 8.17228L5.70588 6.64706L9.82772 5.12184L11.3529 1Z"
				stroke="black"
				stroke-linejoin="round"
			/>
			<path
				d="M4.29412 10.4118L5.62647 12.3735L7.58824 13.7059L5.62647 15.0382L4.29412 17L2.96176 15.0382L1 13.7059L2.96176 12.3735L4.29412 10.4118Z"
				stroke="black"
				stroke-linejoin="round"
			/>
		</svg>
	{/if}
</button>

<style>
	/* Generate button loading animation */
	.generating-text::after {
		content: '';
		animation: generating-dots 1.5s infinite;
	}

	@keyframes generating-dots {
		0%,
		20% {
			content: '.';
		}
		40% {
			content: '..';
		}
		60%,
		100% {
			content: '...';
		}
	}
</style>
