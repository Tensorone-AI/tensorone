<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let prompt;
	export let isLoading;
	export let onInput;
	export let onKeydown;
	export let onSubmit;
</script>

<div
	class="p-4 lg:px-7 lg:py-3 w-full bottom-0 z-100 absolute font-inter"
	in:fly={{
		delay: 700,
		duration: 600,
		y: 50,
		opacity: 0,
		easing: quintOut
	}}
	out:fade={{ duration: 200 }}
>
	<div class="col-span-12 relative mx-44">
		<textarea
			class="textarea w-full h-16 text-[#ECF2FF] text-base placeholder:text-[#444A61] pl-8 pr-20 pt-[18px] bg-[#0C0D12] border border-[#444A61] rounded-full disabled:opacity-50 disabled:bg-[#0C0D12] resize-none overflow-y-auto transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
			placeholder="Ask Anything"
			bind:value={prompt}
			on:input={onInput}
			on:keydown={onKeydown}
			disabled={isLoading}
			style="resize: none; overflow-y: auto;"
		/>
		<button
			class="absolute bottom-[20px] right-5 disabled:opacity-50"
			on:click={onSubmit}
			disabled={isLoading || !prompt}
		>
			<svg
				width="36"
				height="36"
				viewBox="0 0 32 32"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M0 16C0 7.16344 7.16344 0 16 0C24.8366 0 32 7.16344 32 16C32 24.8366 24.8366 32 16 32C7.16344 32 0 24.8366 0 16Z"
					fill="#23F784"
					style="fill:#23F784;fill:color(display-p3 0.1373 0.9686 0.5176);fill-opacity:1;"
				/>
				<path
					d="M16 23V9"
					stroke="black"
					style="stroke:black;stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M9 16L16 9L23 16"
					stroke="black"
					style="stroke:black;stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
	</div>
</div>

<style>
	/* Hide scrollbar while keeping scroll functionality */
	textarea::-webkit-scrollbar {
		display: none;
	}

	textarea {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	/* Smooth transitions */
	textarea {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
