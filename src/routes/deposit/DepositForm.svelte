<script>
	import { fly, fade } from 'svelte/transition';

	export let depositAmount;
	export let isSubmitting;
	export let playgroundCredits;
	export let handleInput;
	export let handleKeydown;
	export let handleDeposit;
</script>

<!-- Deposit Form Section -->
<div class="mb-8 border-b-2 border-[#1F222D] pb-8">
	<h3 class="text-[#ECF2FF] text-3xl font-medium mb-6">Deposit</h3>

	<div class="flex flex-col xl:flex-row xl:items-center gap-4">
		<!-- Deposit Input -->
		<div
			class="relative flex-1"
			in:fly|global={{ delay: 300, x: -100, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<input
				bind:value={depositAmount}
				type="text"
				inputmode="decimal"
				placeholder="Enter an amount to deposit"
				disabled={isSubmitting}
				class="input input-md bg-[#0C0D12] border border-[#444A61] text-[#ECF2FF] text-base placeholder:text-[#BBD0FF] rounded-full transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20 pl-6 pr-20 w-full disabled:opacity-50 [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none [-moz-appearance:textfield]"
				on:input={handleInput}
				on:keydown={handleKeydown}
			/>
			<button
				on:click={handleDeposit}
				disabled={!depositAmount || isSubmitting}
				class="btn btn-primary rounded-full absolute right-0 top-0 px-6 disabled:opacity-50 disabled:cursor-not-allowed"
			>
				<span class="text-base text-kedua font-normal">
					{isSubmitting ? 'Processing...' : 'Submit'}
				</span>
				{#if !isSubmitting}
					<svg
						width="18"
						height="18"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M5 12L19 12"
							stroke="#00200F"
							style="stroke:#00200F;stroke:color(display-p3 0.0000 0.1250 0.0586);stroke-opacity:1;"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M12 5L19 12L12 19"
							stroke="#00200F"
							style="stroke:#00200F;stroke:color(display-p3 0.0000 0.1250 0.0586);stroke-opacity:1;"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{/if}
			</button>
		</div>

		<!-- Playground Credits Display -->
		<div
			class="bg-kedua text-utama rounded-full py-3 px-5 flex-shrink-0 whitespace-nowrap space-x-4"
			in:fly|global={{ delay: 450, x: -100, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<span>Playground Credits</span>
			<span class="border border-utama rounded-full py-1 px-4">
				{playgroundCredits}
			</span>
		</div>
	</div>
</div>

<style>
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
