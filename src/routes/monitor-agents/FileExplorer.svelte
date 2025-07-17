<script>
	import { createEventDispatcher } from 'svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data and functions now centralized
	export let files = [];
	export let selectedFileId = null;
	export let searchQuery = '';
	export let formatFileSize = () => '0 B';
	export let handleFileSelect = () => {};
	export let handleDownload = () => {};
	export let handleSearchInput = () => {};
</script>

<!-- File Explorer Sidebar -->
<div
	class="w-80 bg-[#0C0D12] rounded-l-xl border-r border-[#444A61] overflow-hidden flex flex-col"
	in:fly|global={{ delay: 400, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	<!-- File Explorer Header -->
	<div>
		<div class="flex items-center justify-between p-4 border-b border-[#444A61]">
			<div>
				<h3 class="text-[#ECF2FF] text-lg">Files</h3>
			</div>
			<div class="flex items-center space-x-2">
				<button
					on:click={handleDownload}
					disabled={!selectedFileId}
					class="p-2 bg-[#1F222D] rounded-full hover:opacity-70 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
					title="Download current file"
				>
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M9.45437 0.727295H3.63619C3.25042 0.727295 2.88045 0.880541 2.60767 1.15332C2.33489 1.4261 2.18164 1.79607 2.18164 2.18184V13.8182C2.18164 14.204 2.33489 14.5739 2.60767 14.8467C2.88045 15.1195 3.25042 15.2727 3.63619 15.2727H12.3635C12.7492 15.2727 13.1192 15.1195 13.392 14.8467C13.6648 14.5739 13.818 14.204 13.818 13.8182V5.09093L9.45437 0.727295Z"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-width="0.909091"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M9.45508 0.727295V5.09093H13.8187"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-width="0.909091"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M8 12.3636V8"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-width="0.909091"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M5.81836 10.1818H10.182"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-width="0.909091"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>
			</div>
		</div>

		<!-- Search Files -->
		<div class="p-4">
			<div class="relative border-b border-[#444A61] pb-4">
				<input
					value={searchQuery}
					on:input={handleSearchInput}
					placeholder="Search files..."
					class="w-full bg-[#06070A] border border-[#444A61] rounded-full px-3 py-2 pr-8 text-sm text-[#ECF2FF] placeholder-[#BBD0FF] transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
				/>
				<svg
					width="18"
					height="18"
					viewBox="0 0 18 18"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
					class="absolute right-3 top-2.5 w-4 h-4"
				>
					<path
						d="M8.25 14.25C11.5637 14.25 14.25 11.5637 14.25 8.25C14.25 4.93629 11.5637 2.25 8.25 2.25C4.93629 2.25 2.25 4.93629 2.25 8.25C2.25 11.5637 4.93629 14.25 8.25 14.25Z"
						stroke="#BBD0FF"
						style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M15.7508 15.75L12.4883 12.4875"
						stroke="#BBD0FF"
						style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</div>
		</div>
	</div>

	<!-- File List -->
	<div class="flex-1 relative">
		<div class="absolute inset-0 overflow-y-auto px-4 space-y-2 messages-scrollbar">
			{#if files.length === 0}
				<div class="p-4 text-center">
					<p class="text-[#98A7C8] text-sm">
						{searchQuery ? 'No files match your search' : 'No files available'}
					</p>
				</div>
			{:else}
				{#each files as file (file.id)}
					<button
						on:click={() => handleFileSelect(file.id)}
						class="w-full p-3 text-left hover:bg-[#1F222D] border border-[#444A61] rounded transition-all duration-200 {selectedFileId ===
						file.id
							? 'bg-[#1F222D]'
							: ''}"
					>
						<div class="flex items-center space-x-3">
							<svg
								width="16"
								height="16"
								viewBox="0 0 16 16"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M9.33464 1.33325H4.0013C3.64768 1.33325 3.30854 1.47373 3.05849 1.72378C2.80844 1.97382 2.66797 2.31296 2.66797 2.66659V13.3333C2.66797 13.6869 2.80844 14.026 3.05849 14.2761C3.30854 14.5261 3.64768 14.6666 4.0013 14.6666H12.0013C12.3549 14.6666 12.6941 14.5261 12.9441 14.2761C13.1942 14.026 13.3346 13.6869 13.3346 13.3333V5.33325L9.33464 1.33325Z"
									stroke="#98A7C8"
									style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
									stroke-width="1.33333"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M9.33203 1.33325V5.33325H13.332"
									stroke="#98A7C8"
									style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
									stroke-width="1.33333"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M10.6654 8.66675H5.33203"
									stroke="#98A7C8"
									style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
									stroke-width="1.33333"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M10.6654 11.3333H5.33203"
									stroke="#98A7C8"
									style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
									stroke-width="1.33333"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M6.66536 6H5.9987H5.33203"
									stroke="#98A7C8"
									style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
									stroke-width="1.33333"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<div class="flex-1 min-w-0">
								<p class="text-[#ECF2FF] truncate">{file.name}</p>
								<p class="text-[#98A7C8] text-xs">
									{formatFileSize(file.content)} - {file.lastModified}
								</p>
							</div>
						</div>
					</button>
				{/each}
			{/if}
		</div>
	</div>
</div>

<style>
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}

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
