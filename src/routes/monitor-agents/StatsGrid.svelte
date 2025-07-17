<script>
	import StatsCard from './StatsCard.svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Props passed from parent - data now centralized
	export let data = {
		totalIntents: '0',
		successRate: '0',
		avgResponse: '0',
		activeUsers: '0'
	};
	export let agent = null;

	// Show zeros when no agent, otherwise use provided data
	$: displayData = agent
		? data
		: {
				totalIntents: '0',
				successRate: '0',
				avgResponse: '0',
				activeUsers: '0'
			};
</script>

<div class="grid grid-cols-4 gap-4 mb-4">
	<div in:fly|global={{ delay: 300, duration: 150, x: -50, opacity: 0, easing: quintOut }}>
		<StatsCard title="Total Intents" value={displayData.totalIntents} icon="chart" />
	</div>
	<div in:fly|global={{ delay: 450, duration: 150, x: -50, opacity: 0, easing: quintOut }}>
		<StatsCard
			title="Success Rate"
			value="{displayData.successRate}%"
			icon="trending-up"
			valueColor="text-green-400"
		/>
	</div>
	<div in:fly|global={{ delay: 600, duration: 150, x: -50, opacity: 0, easing: quintOut }}>
		<StatsCard title="Avg Response" value="{displayData.avgResponse}ms" icon="clock" />
	</div>
	<div in:fly|global={{ delay: 750, duration: 150, x: -50, opacity: 0, easing: quintOut }}>
		<StatsCard title="Active Users" value={displayData.activeUsers} icon="users" />
	</div>
</div>
