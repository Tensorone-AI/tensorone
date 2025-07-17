<script>
	import { createEventDispatcher } from 'svelte';
	import AgentStatus from './AgentStatus.svelte';
	import RecentActivity from './RecentActivity.svelte';
	import AgentDetails from './AgentDetails.svelte';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data and functions now centralized
	export let data = {};
	export let agent = null;
	export let statusConfig = {};
	export let calculateUptime = () => '--:--:--';
	export let currentTime = new Date();
	export let agentStatus = 'running';

	function handleSwitchToLogs() {
		dispatch('switch-to-logs');
	}
</script>

<div class="w-80 space-y-4 flex flex-col">
	<AgentStatus {data} {agent} {calculateUptime} {currentTime} {agentStatus} />
	<RecentActivity data={data.recentActivity || []} {agent} />
	<AgentDetails {data} {agent} {statusConfig} on:switch-to-logs={handleSwitchToLogs} />
</div>
