<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Props passed from parent - all logic moved to parent
	export let data = {};
	export let agent = null;
	export let calculateUptime = () => '--:--:--';
	export let currentTime = new Date();
	export let agentStatus = 'running';

	// Calculate reactive uptime using parent function
	$: calculatedUptime = agent
		? calculateUptime(data.startedAt, currentTime, agentStatus)
		: '--:--:--';

	// Format display values based on agent status and presence
	$: displayData = {
		uptime: calculatedUptime,
		memoryUsage: agent
			? agentStatus === 'stopped'
				? '0 MB'
				: data.memoryUsage || '-- MB'
			: '-- MB',
		cpuUsage: agent ? (agentStatus === 'stopped' ? '0%' : data.cpuUsage || '-- %') : '-- %',
		startedAt: agent ? data.startedAt || '--' : '--'
	};
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6"
	in:fly|global={{ delay: 300, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Agent Status</h3>
	<div class="space-y-2">
		<!-- Status indicator - fully reactive to selectedAgent changes -->
		<div class="flex items-center">
			<div class="w-2 h-2 {agent ? 'bg-utama' : 'bg-[#98A7C8]'} rounded-full mr-3"></div>
			<span class={agent ? 'text-utama' : 'text-[#98A7C8]'}>{agent ? 'Running' : 'No Agent'}</span>
		</div>

		<!-- Agent metrics that change based on status -->
		<div class="space-y-2 text-xs">
			<div class="flex justify-between">
				<span class="text-[#98A7C8] font-inter">Uptime</span>
				<span class="text-[#ECF2FF]">{displayData.uptime}</span>
			</div>
			<div class="flex justify-between">
				<span class="text-[#98A7C8] font-inter">Memory Usage</span>
				<span class="text-[#ECF2FF]">{displayData.memoryUsage}</span>
			</div>
			<div class="flex justify-between">
				<span class="text-[#98A7C8] font-inter">CPU Usage</span>
				<span class="text-[#ECF2FF]">{displayData.cpuUsage}</span>
			</div>
			<div class="flex justify-between">
				<span class="text-[#98A7C8] font-inter">Started At</span>
				<span class="text-xs text-[#ECF2FF]">{displayData.startedAt}</span>
			</div>
		</div>
	</div>
</div>
