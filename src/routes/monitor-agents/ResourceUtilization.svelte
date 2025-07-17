<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Props passed from parent - all logic moved to parent
	export let data = {};
	export let agent = null;
	export let getUtilizationStatus = () => 'low';
	export let getStatusStyle = () => '';
	export let getStatusText = () => '';

	// Reactive state - calculations moved to parent
	$: resourceData = {
		utilization: agent ? data.resourceUtilization || 0 : 0,
		status: getUtilizationStatus(agent ? data.resourceUtilization || 0 : 0),
		lastUpdated: null
	};

	// Get status configurations - functions passed from parent
	$: statusStyle = getStatusStyle(resourceData.status);
	$: statusText = getStatusText(resourceData.status);
	$: showStatus = data.showStatus !== undefined ? data.showStatus : true;
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6"
	in:fly|global={{ delay: 300, duration: 150, x: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Resource Utilization</h3>
	{#if agent}
		<div class="mb-4">
			<div class="bg-none bg-transparent {statusStyle} text-2xl font-medium">
				{resourceData.utilization}% of allocated resources
			</div>
			<div class="flex items-center justify-between mt-1">
				<div class="flex items-center gap-2">
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M8.00053 14.1818C11.6155 14.1818 14.546 11.2513 14.546 7.63634C14.546 4.02138 11.6155 1.09088 8.00053 1.09088C4.38558 1.09088 1.45508 4.02138 1.45508 7.63634C1.45508 11.2513 4.38558 14.1818 8.00053 14.1818Z"
							stroke="#98A7C8"
							style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M8 4.72729V8.00002L10.1818 9.09093"
							stroke="#98A7C8"
							style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
					<span class="text-sm text-[#98A7C8] font-inter">Real-time utilization</span>
				</div>
			</div>
		</div>

		{#if showStatus}
			<div class="text-right mt-auto">
				<span class="px-2 py-1 text-sm rounded {statusStyle}">
					{statusText}
				</span>
			</div>
		{/if}
	{:else}
		<div class="flex items-center justify-center h-52">
			<span class="text-[#98A7C8] text-sm">No data available</span>
		</div>
	{/if}
</div>
