<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import LogsHeader from './LogsHeader.svelte';
	import LogsFilters from './LogsFilters.svelte';
	import LogsContent from './LogsContent.svelte';
	import LogsStatusBar from './LogsStatusBar.svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	const dispatch = createEventDispatcher();

	// Props from parent - all data now centralized
	export let logsData = {};
	export let filteredLogs = [];
	export let selectedLogId = null;
	export let autoScroll = true;
	export let showTimestamps = true;
	export let isStreaming = true;
	export let logLevels = [];
	export let logSources = [];
	export let logContainer;
	export let getLogLevelClass;
	export let getBorderLevelClass;

	// Utility functions passed from parent
	export let initializeMockData = () => {};
	export let fetchLogs = () => {};
	export let pauseLogsStreaming = () => {};
	export let resumeLogsStreaming = () => {};

	// Event handlers - now just dispatch to parent
	function handleClearLogs() {
		dispatch('clear-logs');
	}

	function handleDownloadLogs() {
		dispatch('download-logs', {
			count: filteredLogs.length,
			agentUUID: logsData.agentUUID,
			agentName: logsData.agent?.name
		});
	}

	function handleFilterChange(event) {
		dispatch('filter-change', event.detail);
	}

	function handleLogSelect(event) {
		dispatch('log-select', event.detail);
	}

	function toggleAutoScroll() {
		dispatch('auto-scroll-toggle', {
			autoScroll: !autoScroll,
			agentUUID: logsData.agentUUID
		});
	}

	function toggleTimestamps() {
		dispatch('timestamps-toggle', {
			showTimestamps: !showTimestamps,
			agentUUID: logsData.agentUUID
		});
	}

	function toggleStreaming() {
		dispatch('streaming-toggle', {
			isStreaming: !isStreaming,
			agentUUID: logsData.agentUUID
		});
	}

	// Export functions for parent to call
	export function pauseStreaming() {
		pauseLogsStreaming();
	}

	export function resumeStreaming() {
		resumeLogsStreaming();
	}

	onMount(() => {
		console.log('LogsPage mounted for agent:', logsData.agentUUID);

		// Initialize mock data (will check for existing logs first)
		initializeMockData();

		// Fetch logs if needed
		if (logsData.agentUUID) {
			fetchLogs();
		}
	});
</script>

<div
	class="flex flex-col h-full border border-[#444A61] rounded-xl"
	in:fly|global={{ delay: 400, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	<LogsHeader
		{logsData}
		{filteredLogs}
		{showTimestamps}
		{autoScroll}
		on:clear-logs={handleClearLogs}
		on:download-logs={handleDownloadLogs}
		on:toggle-auto-scroll={toggleAutoScroll}
		on:toggle-timestamps={toggleTimestamps}
		on:toggle-streaming={toggleStreaming}
	/>

	<LogsFilters {logsData} {logLevels} {logSources} on:filter-change={handleFilterChange} />

	<LogsContent
		{logsData}
		{filteredLogs}
		{showTimestamps}
		{selectedLogId}
		{getLogLevelClass}
		{getBorderLevelClass}
		bind:logContainer
		on:log-select={handleLogSelect}
	/>

	{#if logsData.agent}
		<LogsStatusBar {logsData} {filteredLogs} {selectedLogId} />
	{/if}
</div>
