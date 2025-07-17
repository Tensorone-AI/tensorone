<script>
	export let plan;
	export let index;
	export let fly;
	export let quintOut;
	export let CheckIconCard;
	export let XIconCard;

	$: delay = 300 + index * 150;
</script>

<div
	class="card card-compact bg-black border border-[#1F222D] w-full rounded-[32px] rounded-tr-[96px] relative overflow-hidden"
	in:fly|global={{ delay, duration: 500, x: -100, opacity: 0, easing: quintOut }}
	out:fly|global={{ duration: 300, x: -100, opacity: 0, easing: quintOut }}
>
	<div class="card-body flex flex-col relative z-10 space-y-4">
		<h2 class="card-title text-3xl text-[#ECF2FF] font-medium px-4 pt-4">{plan.name}</h2>

		<div class="px-4">
			{#if plan.priceDisplay}
				<p class="flex items-start mb-5">
					<span class="text-3xl md:text-4xl text-utama font-medium">
						{plan.priceDisplay}
					</span>
				</p>
			{:else}
				<p class="flex items-start">
					<span class="text-sm text-[#ECF2FF] font-satoshi font-medium">$</span>
					<span class="text-3xl md:text-4xl text-utama font-medium">
						{plan.price}/mo
					</span>
				</p>
				<p class="text-[#98A7C8] text-xs font-inter">USDT / Per Month</p>
			{/if}
		</div>

		<div class="px-4 pb-4">
			<ul class="text-sm space-y-3">
				{#each plan.features as feature}
					<li
						class="flex flex-row items-center gap-2 {feature.included
							? 'text-[#ECF2FF]'
							: 'text-[#98A7C8]'}"
					>
						<i>
							{#if feature.included}
								<svelte:component this={CheckIconCard} />
							{:else}
								<svelte:component this={XIconCard} />
							{/if}
						</i>
						{feature.name}
					</li>
				{/each}
			</ul>
		</div>

		<div class="card-actions justify-center mt-auto px-4">
			<button
				class="btn bg-kedua border border-primary rounded-full w-full text-primary font-normal hover:bg-kedua hover:border-primary hover:opacity-70 transition-all duration-200"
			>
				{plan.buttonText}
			</button>
		</div>
	</div>
</div>
