<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import NextAndBackButtons from './NextAndBackButtons.svelte';

	const dispatch = createEventDispatcher();

	// All props from parent (centralized in +page.svelte)
	export let knowledgeBase = { uploadedFiles: [], rawData: '' };
	export let selectedKnowledgeBaseCost = 0;
	export let isLoading = false;
	export let canProceed = true;
	export let computeUnitsStore = { current: 0, total: 0 };
	export let newAgentCost = 0;
	export let hasInsufficientComputeUnits = false;
	export let nextButtonText = 'Next';
	export let nextButtonClass = 'btn-primary';

	// Helper functions passed from parent
	export let handleBrowseClick = () => {};

	// Local UI state only
	let fileInput;

	// Event handlers - just dispatch to parent
	function handleFileUpload(event) {
		dispatch('fileUpload', { files: event.target.files, fileInput });
	}

	function removeFile(fileId) {
		dispatch('fileRemove', { fileId });
	}

	function handleRawDataChange(event) {
		dispatch('rawDataChange', { value: event.target.value });
	}

	function handleBrowseClickLocal() {
		handleBrowseClick(fileInput);
	}

	function handleNext() {
		dispatch('next');
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div
	class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<div
		class="mb-4 border-b-2 border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Build Knowledge Base</h3>
			<p class="text-base text-[#D9E4FF]">Equip your agent with background knowledge and data</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Cost: <span class="text-utama">{selectedKnowledgeBaseCost} cu</span>
			</p>
		</div>
	</div>

	<!-- Knowledge Base Content -->
	<div class="flex-1 min-h-0 flex flex-col">
		<div class="grid gap-6 lg:grid-cols-2 h-full">
			<!-- Upload File Section -->
			<div
				class="flex flex-col border-r-2 border-[#1F222D] pr-6"
				in:fly|global={{
					delay: 300,
					duration: 500,
					x: -100,
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				<h4 class="text-xl text-[#ECF2FF] mb-4">Upload File</h4>

				<!-- File Input (Hidden) -->
				<input
					bind:this={fileInput}
					type="file"
					multiple
					accept=".txt,.pdf,.doc,.docx,.csv,.json"
					class="hidden"
					on:change={handleFileUpload}
				/>

				<!-- Uploaded Files List -->
				<div class="flex-1 mb-4 space-y-2">
					{#each knowledgeBase.uploadedFiles as file (file.id)}
						<div
							class="bg-kedua rounded-full px-4 py-2 flex items-center justify-between"
							in:fly={{ delay: 100, duration: 300, x: -50, opacity: 0 }}
							out:fade={{ duration: 200 }}
						>
							<div class="flex items-center gap-3 min-w-0 flex-1">
								<div class="min-w-0 flex-1">
									<p class="text-utama truncate">{file.name}</p>
								</div>
							</div>
							<button
								class="hover:opacity-70 transition-all duration-200"
								on:click={() => removeFile(file.id)}
							>
								<svg
									width="24"
									height="24"
									viewBox="0 0 24 24"
									fill="none"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										d="M16.9502 7.05029L7.0507 16.9498"
										stroke="#23F784"
										style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
									<path
										d="M7.0498 7.05029L16.9493 16.9498"
										stroke="#23F784"
										style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
								</svg>
							</button>
						</div>
					{/each}
				</div>

				<!-- Browse Button -->
				<button
					class="border border-[#444A61] bg-[#0C0D12] rounded-full px-4 py-2 flex items-center justify-center gap-2 hover:opacity-70 transition-all duration-200"
					on:click={handleBrowseClickLocal}
				>
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M14 10V12.6667C14 13.0203 13.8595 13.3594 13.6095 13.6095C13.3594 13.8595 13.0203 14 12.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V10"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M11.3337 5.33333L8.00033 2L4.66699 5.33333"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M8 2V10"
							stroke="#ECF2FF"
							style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>

					<span class="text-[#ECF2FF]">Browse</span>
				</button>
			</div>

			<!-- Raw Data Section -->
			<div
				class="flex flex-col"
				in:fly|global={{
					delay: 450,
					duration: 500,
					x: -100,
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				<h4 class="text-xl text-[#ECF2FF] mb-4">Raw Data</h4>

				<!-- Textarea -->
				<textarea
					class="flex-1 textarea bg-[#0C0D12] border border-[#444A61] w-full min-h-[500px] text-[#ECF2FF] placeholder:text-[#98A7C8] px-7 py-4 rounded-3xl resize-none overflow-y-auto transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
					placeholder="Enter raw data..."
					value={knowledgeBase.rawData}
					on:input={handleRawDataChange}
				></textarea>
			</div>
		</div>
	</div>

	<!-- Next/Back Buttons -->
	<NextAndBackButtons
		{isLoading}
		{canProceed}
		currentComputeUnits={computeUnitsStore.current}
		totalComputeUnits={computeUnitsStore.total}
		{newAgentCost}
		{hasInsufficientComputeUnits}
		{nextButtonText}
		{nextButtonClass}
		on:next={handleNext}
		on:back={handleBack}
	/>
</div>

<style>
	textarea::-webkit-scrollbar {
		width: 8px;
	}

	textarea::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 4px;
	}

	textarea::-webkit-scrollbar-thumb {
		background: #23f784;
		border-radius: 4px;
	}

	textarea::-webkit-scrollbar-thumb:hover {
		background: #1ed670;
	}

	textarea {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
