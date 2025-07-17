<script>
	import { createEventDispatcher } from 'svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Props passed from parent
	export let data = {};
	export let agent = null;
	export let statusConfig = {}; // Status configuration moved to parent

	const dispatch = createEventDispatcher();

	// Process and format display data reactively
	$: agentDetails = data.agentDetails || data || {};
	$: displayData = agent
		? {
				created: agentDetails.created || '--/--/----',
				lastUpdated: agentDetails.lastUpdated || '--/--/----',
				agentId: agentDetails.agentId || 'unknown',
				loggingLevel: agentDetails.loggingLevel || 'info',
				autoRestart: agentDetails.autoRestart !== undefined ? agentDetails.autoRestart : true
			}
		: {
				created: '--/--/----',
				lastUpdated: '--/--/----',
				agentId: '--',
				loggingLevel: 'info',
				autoRestart: false
			};

	// Get status configurations using parent statusConfig
	$: autoRestartStatus = statusConfig.autoRestart?.[
		displayData.autoRestart ? 'enabled' : 'disabled'
	] || { color: 'text-[#ECF2FF]', label: '--' };
	$: loggingLevelStatus = statusConfig.loggingLevel?.[displayData.loggingLevel.toLowerCase()] ||
		statusConfig.loggingLevel?.info || { color: 'text-[#ECF2FF]', label: '--' };

	function handleLoggingLevelClick() {
		if (agent) {
			dispatch('switch-to-logs');
		}
	}
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6"
	in:fly|global={{ delay: 600, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Agent Details</h3>
	<div class="space-y-2 text-sm">
		<div class="flex justify-between">
			<span class="text-[#98A7C8] font-inter">Created</span>
			<span class="text-[#ECF2FF]">{displayData.created}</span>
		</div>
		<div class="flex justify-between">
			<span class="text-[#98A7C8] font-inter">Last Updated</span>
			<span class="text-[#ECF2FF]">{displayData.lastUpdated}</span>
		</div>
		<div class="flex justify-between">
			<span class="text-[#98A7C8] font-inter">Logging Level</span>
			{#if agent}
				<button
					class="{loggingLevelStatus.color} hover:opacity-80 cursor-pointer underline"
					on:click={handleLoggingLevelClick}
				>
					{loggingLevelStatus.label}
				</button>
			{:else}
				<span class="text-[#ECF2FF]">--</span>
			{/if}
		</div>
		<div class="flex justify-between">
			<span class="text-[#98A7C8] font-inter">Auto Restart</span>
			<span class={agent ? autoRestartStatus.color : 'text-[#ECF2FF]'}>
				{agent ? autoRestartStatus.label : '--'}
			</span>
		</div>
	</div>
</div>
