<script>
	import ResourceUtilization from './ResourceUtilization.svelte';
	import ResponseTimeChart from './ResponseTimeChart.svelte';

	// Props passed from parent - data now centralized
	export let resourceUtilizationData = {};
	export let responseTimeData = [];
	export let agent = null;
	export let getUtilizationStatus = () => 'low';
	export let getStatusStyle = () => '';
	export let getStatusText = () => '';
</script>

<div class="grid grid-cols-2 gap-4 flex-1">
	<ResourceUtilization
		data={resourceUtilizationData}
		{agent}
		{getUtilizationStatus}
		{getStatusStyle}
		{getStatusText}
	/>
	<ResponseTimeChart data={responseTimeData} {agent} />
</div>
