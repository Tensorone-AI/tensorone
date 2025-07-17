<script>
	import { createEventDispatcher } from 'svelte';
	import LogEntry from './LogEntry.svelte';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data now centralized
	export let logsData;
	export let filteredLogs;
	export let showTimestamps;
	export let selectedLogId;
	export let logContainer;
	export let getLogLevelClass;
	export let getBorderLevelClass;

	function handleLogSelect(event) {
		dispatch('log-select', event.detail);
	}
</script>

<div class="flex-1 overflow-hidden bg-[#06070A]">
	{#if filteredLogs.length === 0}
		<div class="flex items-center justify-center h-full">
			<div class="text-center">
				<svg
					class="w-12 h-12 text-[#98A7C8] mx-auto mb-4"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
					/>
				</svg>
				<h3 class="text-[#ECF2FF] font-medium mb-2">
					{logsData.agent ? 'No Logs Found' : 'No Logs Available'}
				</h3>
				<p class="text-[#98A7C8] text-sm">
					{logsData.agent
						? logsData.logs.length === 0
							? 'No logs available'
							: 'No logs match your current filters'
						: 'No agent available'}
				</p>
			</div>
		</div>
	{:else}
		<div class="relative h-full">
			<div
				bind:this={logContainer}
				class="absolute inset-0 overflow-y-auto p-4 font-iosevka text-sm messages-scrollbar"
			>
				{#each filteredLogs as log (log.id)}
					<LogEntry
						{log}
						{showTimestamps}
						{getLogLevelClass}
						{getBorderLevelClass}
						isSelected={selectedLogId === log.id}
						on:select={handleLogSelect}
					/>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	/* Custom scrollbar styles for messages container */
	.messages-scrollbar {
		/* Firefox */
		scrollbar-width: thin;
		scrollbar-color: #444a61 transparent;
	}

	/* Webkit browsers (Chrome, Safari, Edge) */
	.messages-scrollbar::-webkit-scrollbar {
		width: 6px;
	}

	.messages-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}

	.messages-scrollbar::-webkit-scrollbar-thumb {
		background-color: #444a61;
		border-radius: 3px;
	}

	.messages-scrollbar::-webkit-scrollbar-thumb:hover {
		background-color: #5a6175;
	}
</style>
