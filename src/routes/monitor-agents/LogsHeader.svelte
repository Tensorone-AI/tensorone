<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data now centralized
	export let logsData;
	export let filteredLogs;
	export let showTimestamps;
	export let autoScroll;

	// Reactive states based on agent availability
	$: hasAgent = logsData.agent != null;
	$: streamingStatus = hasAgent ? (logsData.isStreaming ? 'Live' : 'Paused') : 'No Agent';
	$: streamingColor = hasAgent
		? logsData.isStreaming
			? 'bg-utama animate-pulse'
			: 'bg-[#98A7C8]'
		: 'bg-[#98A7C8]';

	function handleClearLogs() {
		dispatch('clear-logs');
	}

	function handleDownloadLogs() {
		dispatch('download-logs');
	}

	function toggleAutoScroll() {
		dispatch('toggle-auto-scroll');
	}

	function toggleTimestamps() {
		dispatch('toggle-timestamps');
	}

	function toggleStreaming() {
		dispatch('toggle-streaming');
	}
</script>

<div class="bg-[#0C0D12] border-b border-[#444A61] rounded-t-xl p-4">
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-4">
			<h2 class="text-[#ECF2FF] text-lg">Agent Logs</h2>
			<div
				class="flex items-center space-x-2 bg-[#06070A] border border-[#1F222D] rounded-full px-3 py-1.5"
			>
				<!-- Streaming indicator -->
				<div class="flex items-center space-x-2">
					<div class="w-2 h-2 rounded-full {streamingColor}"></div>
					<span class="text-xs text-[#D9E4FF]">{streamingStatus}</span>
				</div>
				<span class="text-[#D9E4FF] text-sm">({filteredLogs.length} entries)</span>
			</div>
		</div>

		<div class="flex items-center space-x-2">
			<!-- View Options -->
			<button
				on:click={toggleTimestamps}
				disabled={!hasAgent}
				class="px-3 py-1.5 text-xs border rounded-full {showTimestamps
					? 'bg-kedua text-utama border-utama'
					: 'bg-[#1F222D] text-[#ECF2FF] border-[#444A61]'} transition-all duration-200 {hasAgent
					? 'hover:opacity-70 cursor-pointer'
					: 'opacity-50 cursor-not-allowed'}"
			>
				Timestamps
			</button>

			<button
				on:click={toggleAutoScroll}
				disabled={!hasAgent}
				class="px-3 py-1.5 text-xs border rounded-full {autoScroll
					? 'bg-kedua text-utama border-utama'
					: 'bg-[#1F222D] text-[#ECF2FF] border-[#444A61]'} transition-all duration-200 {hasAgent
					? 'hover:opacity-70 cursor-pointer'
					: 'opacity-50 cursor-not-allowed'}"
			>
				Auto-scroll
			</button>

			<button
				on:click={toggleStreaming}
				disabled={!hasAgent}
				class="px-3 py-1.5 text-xs border rounded-full {hasAgent && logsData.isStreaming
					? 'bg-kedua text-utama border-utama'
					: 'bg-[#1F222D] text-[#ECF2FF] border-[#444A61]'} transition-all duration-200 {hasAgent
					? 'hover:opacity-70 cursor-pointer'
					: 'opacity-50 cursor-not-allowed'}"
			>
				{hasAgent ? (logsData.isStreaming ? 'Pause' : 'Resume') : 'No'} Stream
			</button>

			<!-- Action Buttons -->
			<button
				on:click={handleDownloadLogs}
				disabled={!hasAgent || filteredLogs.length === 0}
				class="px-3 py-1.5 bg-[#1F222D] border border-[#444A61] rounded-full transition-all duration-200 flex items-center gap-2 {hasAgent &&
				filteredLogs.length > 0
					? 'hover:opacity-70 cursor-pointer'
					: 'opacity-50 cursor-not-allowed'}"
				title="Download logs"
			>
				<svg
					width="auto"
					height="auto"
					viewBox="0 0 16 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
					class="w-4 h-4"
				>
					<path
						d="M14 10V12.6667C14 13.0203 13.8595 13.3594 13.6095 13.6095C13.3594 13.8595 13.0203 14 12.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V10"
						stroke="#ECF2FF"
						style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M5 7L8 10L11 7"
						stroke="#ECF2FF"
						style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M8 10V3"
						stroke="#ECF2FF"
						style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
				<span class="text-[#ECF2FF] text-xs">Download</span>
			</button>

			<button
				on:click={handleClearLogs}
				disabled={!hasAgent || filteredLogs.length === 0}
				class="px-3 py-1.5 bg-[#220007] border border-[#F80036] rounded-full text-xs text-[#F80036] transition-all duration-200 {hasAgent &&
				filteredLogs.length > 0
					? 'hover:opacity-70 cursor-pointer'
					: 'opacity-50 cursor-not-allowed'}"
			>
				Clear Logs
			</button>
		</div>
	</div>
</div>
