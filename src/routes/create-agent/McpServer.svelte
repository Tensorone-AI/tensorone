<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	// All props from parent (centralized in +page.svelte)
	export let mcpServers;
	export let selectedServers;
	export let totalSelectedCost = 0;
	export let isLoading = false;
	export let canProceed = false;
	export let computeUnitsStore = { current: 0, total: 0, available: 0 };
	export let newAgentCost = 0;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Event dispatcher for parent communication
	const dispatch = createEventDispatcher();

	// Event handlers - dispatch to parent
	function handleServerToggle(serverId, isEnabled) {
		dispatch('serverToggle', { serverId, isEnabled });
	}

	function handleShowServerInfo(server) {
		dispatch('showServerInfo', { server });
	}

	function handleNext() {
		dispatch('next');
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div
	class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<!-- MCP Server Section -->
	<div
		class="mb-4 border-b-2 border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade|global={{ delay: 300, duration: 500 }}
		out:fade|global={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Select MCP Server</h3>
			<p class="text-base text-[#D9E4FF]">
				Choose the MCP servers that will provide data and functionality to your AI agent.
			</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{totalSelectedCost} cu</span>
			</p>
		</div>
	</div>

	<!-- MCP Servers Grid -->
	<div class="flex-1 min-h-0 flex flex-col -m-1">
		<div class="grid gap-4 sm:grid-cols-3 flex-1 auto-rows-max overflow-y-auto p-1">
			{#each mcpServers as server, index (server.id)}
				<div
					class="card card-compact bg-black border-2 border-[#1F222D] rounded-[18px] w-full relative overflow-hidden min-h-48"
					class:ring-1={selectedServers.includes(server.id)}
					class:ring-utama={selectedServers.includes(server.id)}
					data-server-id={server.id}
					in:fly|global={{
						delay: 300,
						duration: 500 * (index + 1),
						x: -100 * (index + 1),
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
				>
					<div class="card-body flex flex-col relative z-10">
						<!-- Server Header -->
						<div class="flex items-center justify-between mb-2 px-4 py-1 bg-[#0C0D12] rounded-md">
							<h2 class="card-title text-xl text-[#ECF2FF] font-normal">
								{server.name}
							</h2>
							<input
								type="checkbox"
								class="toggle toggle-primary text-[#BBD0FF] border-[#444A61]"
								checked={selectedServers.includes(server.id)}
								data-testid="server-toggle-{server.id}"
								on:change={(e) => handleServerToggle(server.id, e.target.checked)}
							/>
						</div>

						<!-- Server Description -->
						<p class="mb-4 px-4 text-base text-[#ECF2FF] flex-grow">
							{server.description}
						</p>

						<!-- Server Actions -->
						<div class="card-actions mt-auto px-4 flex items-center justify-between">
							<span class="text-utama text-base bg-kedua px-3 py-1 rounded-full"
								>{server.cost} cu</span
							>
							<button
								class="btn btn-circle btn-outline bg-[#1F222D] hover:bg-[#1F222D] hover:border-utama btn-xs text-[#ECF2FF] hover:text-utama"
								data-testid="info-button-{server.id}"
								on:click={() => handleShowServerInfo(server)}
							>
								i
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Next/Back Buttons -->
	<NextAndBackButtons
		{isLoading}
		{canProceed}
		canGoBack={true}
		currentComputeUnits={computeUnitsStore.current}
		totalComputeUnits={computeUnitsStore.total}
		{newAgentCost}
		showComputeUnits={true}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>
