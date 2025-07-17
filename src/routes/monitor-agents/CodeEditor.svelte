<script>
	import { createEventDispatcher } from 'svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data and functions now centralized
	export let agent = null;
	export let activeFile = null;
	export let lastUpdated = null;
	export let formatFileSize = () => '0 B';
	export let getSyntaxClass = () => 'language-text';
	export let isCopied = false;
	export let toggleFullscreen = () => {};
	export let handleCopy = () => {};
</script>

<!-- Code Editor Area -->
<div
	class="flex-1 flex flex-col overflow-hidden rounded-r-xl"
	in:fly|global={{ delay: 400, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	{#if activeFile}
		<!-- Editor Header -->
		<div class="bg-[#0C0D12] border-b border-[#444A61] p-4">
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-3">
					<div>
						<h2 class="text-[#ECF2FF] text-lg">{activeFile.name}</h2>
					</div>
					<span
						class="px-4 py-1.5 bg-[#06070A] border border-[#1F222D] text-[#D9E4FF] text-xs rounded-full"
					>
						{activeFile.type}
					</span>
				</div>

				<div class="flex items-center space-x-6">
					<button
						on:click={handleCopy}
						class="hover:opacity-70 transition-all duration-200"
						title={isCopied ? 'Copied!' : 'Copy code'}
					>
						{#if isCopied}
							<!-- Check Icon -->
							<svg
								width="16"
								height="16"
								viewBox="0 0 16 16"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M13.5 4.5L6 12L2.5 8.5"
									stroke="#BBD0FF"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
						{:else}
							<!-- Copy Icon -->
							<svg
								width="16"
								height="16"
								viewBox="0 0 16 16"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<g clip-path="url(#clip0_554_3579)">
									<path
										d="M13.7227 5.59998H7.07653C6.26085 5.59998 5.59961 6.26122 5.59961 7.0769V13.7231C5.59961 14.5387 6.26085 15.2 7.07653 15.2H13.7227C14.5384 15.2 15.1996 14.5387 15.1996 13.7231V7.0769C15.1996 6.26122 14.5384 5.59998 13.7227 5.59998Z"
										stroke="#BBD0FF"
										style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
										stroke-width="1.6"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
									<path
										d="M3.01617 10.4H2.2777C1.886 10.4 1.51034 10.2444 1.23336 9.96747C0.956385 9.69049 0.800781 9.31483 0.800781 8.92313V2.27697C0.800781 1.88527 0.956385 1.50961 1.23336 1.23263C1.51034 0.955653 1.886 0.800049 2.2777 0.800049H8.92386C9.31556 0.800049 9.69122 0.955653 9.9682 1.23263C10.2452 1.50961 10.4008 1.88527 10.4008 2.27697V3.01543"
										stroke="#BBD0FF"
										style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
										stroke-width="1.6"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
								</g>
								<defs>
									<clipPath id="clip0_554_3579">
										<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
									</clipPath>
								</defs>
							</svg>
						{/if}
					</button>

					<button
						on:click={toggleFullscreen}
						class="hover:opacity-70 transition-all duration-200"
						title="Toggle fullscreen"
					>
						<svg
							width="16"
							height="16"
							viewBox="0 0 16 16"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<g clip-path="url(#clip0_554_3582)">
								<path
									d="M4.88889 1H2.55556C2.143 1 1.74733 1.16389 1.45561 1.45561C1.16389 1.74733 1 2.143 1 2.55556V4.88889M15 4.88889V2.55556C15 2.143 14.8361 1.74733 14.5444 1.45561C14.2527 1.16389 13.857 1 13.4444 1H11.1111M11.1111 15H13.4444C13.857 15 14.2527 14.8361 14.5444 14.5444C14.8361 14.2527 15 13.857 15 13.4444V11.1111M1 11.1111V13.4444C1 13.857 1.16389 14.2527 1.45561 14.5444C1.74733 14.8361 2.143 15 2.55556 15H4.88889"
									stroke="#BBD0FF"
									style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</g>
							<defs>
								<clipPath id="clip0_554_3582">
									<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
								</clipPath>
							</defs>
						</svg>
					</button>
				</div>
			</div>
		</div>

		<!-- Code Content -->
		<div class="flex-1 relative bg-black">
			<div class="absolute inset-0 overflow-auto p-6 messages-scrollbar">
				<pre class="text-sm text-[#ECF2FF] leading-relaxed whitespace-pre-wrap break-words"><code
						class={`${getSyntaxClass(activeFile.type)} font-iosevka`}>{activeFile.content}</code
					></pre>
			</div>
		</div>

		<!-- Status Bar -->
		<div class="bg-[#0C0D12] border-t border-[#444A61] px-4 py-2">
			<div class="flex items-center justify-between text-xs text-[#98A7C8]">
				<div class="flex items-center space-x-4">
					<span>Lines: {activeFile.content.split('\n').length}</span>
					<span>Size: {formatFileSize(activeFile.content)}</span>
					<span>Type: {activeFile.type}</span>
					{#if agent?.status}
						<span
							class="px-2 py-1 rounded-full bg-{agent.status === 'running'
								? 'green'
								: agent.status === 'stopped'
									? 'red'
									: 'yellow'}-500/20 text-{agent.status === 'running'
								? 'green'
								: agent.status === 'stopped'
									? 'red'
									: 'yellow'}-400"
						>
							{agent.status}
						</span>
					{/if}
				</div>
				<div class="flex items-center space-x-2">
					<span>Modified: {activeFile.lastModified}</span>
					{#if lastUpdated}
						<span>•</span>
						<span>Updated: {new Date(lastUpdated).toLocaleTimeString()}</span>
					{/if}
				</div>
			</div>
		</div>
	{:else}
		<!-- No File Selected -->
		<div class="flex-1 flex items-center justify-center">
			<div class="text-center">
				<svg
					class="w-16 h-16 text-[#98A7C8] mx-auto mb-4"
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
				<h3 class="text-[#ECF2FF] text-lg font-medium mb-2">
					{agent ? 'No File Selected' : 'No Files Available'}
				</h3>
				<p class="text-[#98A7C8]">
					{agent ? 'Select a file from the sidebar to view its contents' : 'No agent available'}
				</p>
			</div>
		</div>
	{/if}
</div>

<style>
	.language-javascript {
		color: #e6db74;
	}
	.language-json {
		color: #66d9ef;
	}
	.language-markdown {
		color: #a6e22e;
	}
	.language-python {
		color: #fd971f;
	}
	.language-html {
		color: #f92672;
	}
	.language-css {
		color: #ae81ff;
	}

	pre {
		tab-size: 2;
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
