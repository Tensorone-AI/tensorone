<script>
	// Props passed from parent - all data now centralized
	export let logsData;
	export let filteredLogs;
	export let selectedLogId;
</script>

<div class="bg-[#0C0D12] border-t border-[#444A61] rounded-b-xl px-4 py-2">
	<div class="flex items-center justify-between text-xs text-[#98A7C8]">
		<div class="flex items-center space-x-4">
			<span>Total: {logsData.logs.length} logs</span>
			<span>Filtered: {filteredLogs.length} logs</span>
			<span>Status: {logsData.isStreaming ? 'Streaming' : 'Paused'}</span>
		</div>
		<div class="flex items-center space-x-2">
			{#if selectedLogId}
				<span>Log #{selectedLogId} selected</span>
			{/if}
			<span>Last updated: {new Date().toLocaleTimeString()}</span>
		</div>
	</div>
</div>
