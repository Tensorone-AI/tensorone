<script>
	export let plans;
	export let comparisonData;
	export let renderComparisonCell;
	export let CheckIcon;
	export let XIcon;
	export let fade;
</script>

<div class="w-full" in:fade={{ delay: 300, duration: 500 }} out:fade={{ duration: 300 }}>
	<h2 class="text-3xl lg:text-4xl text-[#ECF2FF] font-medium pb-12">Detailed Breakdown</h2>
	<div class="overflow-x-auto relative">
		<table class="table text-base bg-black border border-[#1F222D] rounded-[32px]">
			<thead class="text-xl">
				<tr class="text-center text-utama">
					<th class="h-16 w-52" />
					{#each plans as plan}
						<th class="h-16 w-52 font-normal">{plan.name}</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				<!-- Feature Comparison Rows -->
				{#each comparisonData as row}
					<tr>
						<td class="h-16 w-52 border border-[#1F222D] text-[#ECF2FF]">{row.feature}</td>
						{#each ['basic', 'business', 'advanced', 'enterprise'] as planType}
							{@const cellData = renderComparisonCell(row[planType])}
							<td class="text-center text-[#BBD0FF] h-16 w-52 border border-[#1F222D]">
								{#if cellData.type === 'boolean'}
									{#if cellData.value}
										<i class="inline-block align-middle">
											<svelte:component this={CheckIcon} />
										</i>
									{:else}
										<i class="inline-block align-middle">
											<svelte:component this={XIcon} />
										</i>
									{/if}
								{:else if cellData.value === true}
									<i class="inline-block align-middle">
										<svelte:component this={CheckIcon} />
									</i>
								{:else}
									{cellData.value}
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
