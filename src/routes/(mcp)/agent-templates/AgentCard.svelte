<script>
	// ========================================
	// PROPS
	// ========================================
	export let agent;
	export let availableComputeUnits = 0;
	export let onCardClick;

	// ========================================
	// COMPUTED VALUES
	// ========================================
	$: hasInsufficientFunds = availableComputeUnits < agent.estimatedCost;
	$: remainingCU = agent.estimatedCost - availableComputeUnits;

	// ========================================
	// EVENT HANDLERS
	// ========================================
	function handleCardClick() {
		if (hasInsufficientFunds) {
			// Prevent action if insufficient funds
			return;
		}
		onCardClick(agent);
	}
</script>

<div
	class="card card-compact bg-black border-2 border-[#1F222D] rounded-[18px] w-full relative overflow-hidden flex flex-col transition-all duration-200 group {hasInsufficientFunds
		? 'cursor-default opacity-60'
		: 'cursor-pointer hover:border-utama'}"
	on:click={handleCardClick}
	on:keydown={(e) => e.key === 'Enter' && handleCardClick()}
	tabindex="0"
	role="button"
	aria-label="Select {agent.name || 'Unnamed Agent'} template"
	title={hasInsufficientFunds
		? `Insufficient Compute Units. You need ${remainingCU} more CU to use this template.`
		: `Click to use ${agent.name} template`}
>
	<div class="card-body flex flex-col items relative z-10 flex-1">
		<div
			class="flex justify-between items-center space-x-2 bg-[#0C0D12] px-3 py-2 rounded-md transition-colors duration-200"
		>
			<h2 class="card-title text-xl text-[#ECF2FF] font-normal">
				{agent.name || 'Unnamed Agent'}
			</h2>
			<div class="flex flex-col items-end">
				<h3 class="text-utama text-sm font-normal">
					{agent.estimatedCost === 0 ? 'FREE' : `${agent.estimatedCost} CU`}
				</h3>
			</div>
		</div>
		<div class="flex-1 flex items-center justify-center py-2 px-3">
			<p class="text-[#ECF2FF] text-sm leading-relaxed line-clamp-3 transition-colors duration-200">
				{agent.description || 'No Description'}
			</p>
		</div>
		<div class="card-actions mt-auto px-3">
			<div
				class="bg-kedua border border-utama text-utama rounded-full px-4 py-1 transition-colors duration-200"
			>
				{agent.category || 'General'}
			</div>
			<div
				class="bg-kedua border border-utama text-utama rounded-full px-4 py-1 transition-colors duration-200"
			>
				{agent.complexity || 'Fast Agent'}
			</div>
		</div>
	</div>

	<!-- Insufficient Funds Overlay -->
	{#if hasInsufficientFunds}
		<div
			class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20 rounded-[18px] opacity-0 group-hover:opacity-100 transition-opacity duration-200"
		>
			<div class="text-center text-white p-4">
				<div class="text-red-400 text-sm font-medium mb-1">Insufficient Compute Units</div>
				<div class="text-xs text-gray-300">You need {remainingCU} more CU</div>
			</div>
		</div>
	{/if}
</div>
