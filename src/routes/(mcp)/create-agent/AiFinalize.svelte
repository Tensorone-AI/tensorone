<script>
	import { createEventDispatcher } from 'svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	// Props passed from parent (all helper functions moved to parent)
	export let selectedServers = [];
	export let selectedFramework = null;
	export let selectedModel = null;
	export let knowledgeBase = { uploadedFiles: [], rawData: '' };
	export let selectedVoice = null;
	export let characterDetails = {};
	export let agentBehavior = {};
	export let totalCost = 0;
	export let isLoading = false;
	export let canProceed = true;
	export let computeUnitsStore = { current: 0, total: 0 };
	export let newAgentCost = 0;

	// Individual costs from parent
	export let mcpServersCost = 0;
	export let frameworkCost = 0;
	export let modelCost = 0;
	export let knowledgeBaseCost = 0;
	export let voiceCost = 0;
	export let characterDetailsCost = 0;

	// Helper functions passed from parent
	export let getServerNameById = () => {};
	export let getAgentToneName = () => {};
	export let formatVoiceSettings = () => {};
	export let formatMemorySettings = () => {};
	export let formatBehaviorCategory = () => {};

	const dispatch = createEventDispatcher();

	// Edit handlers
	function handleEditSection(sectionId) {
		dispatch('editSection', { sectionId });
	}

	function handleActivate() {
		dispatch('finalize');
	}

	function handleNext() {
		dispatch('next');
	}

	function handleBack() {
		dispatch('back');
	}
</script>

<div
	class="bg-black rounded-xl border border-[#444A61] p-7 flex-1 overflow-y-auto content-start mt-4"
>
	<div
		class="mb-4 border-b border-[#1F222D] pb-4 flex justify-between items-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		<div class="space-y-3">
			<h3 class="text-xl lg:text-3xl text-[#ECF2FF] font-medium">Finalize & Activate</h3>
			<p class="text-base text-[#D9E4FF]">Review your options and make changes if necessary.</p>
		</div>
		<div>
			<p class="text-base text-[#D9E4FF]">
				Total Cost: <span class="text-utama">{totalCost} cu</span>
			</p>
		</div>
	</div>

	<!-- Card Grid -->
	<div class="grid gap-4 sm:grid-cols-4 mb-4">
		<!-- MCP Server Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 300,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">MCP Server</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('mcpServer')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					{#if selectedServers && selectedServers.length > 0}
						{#each selectedServers as serverId}
							<p class="text-[#D9E4FF] text-base">{getServerNameById(serverId)}</p>
						{/each}
					{:else}
						<p class="text-[#D9E4FF] text-base">No servers selected</p>
					{/if}
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">
						Cost: <span class="text-utama">{mcpServersCost} cu</span>
					</p>
				</div>
			</div>
		</div>

		<!-- Framework Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 350,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Framework</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('framework')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					<p class="text-[#D9E4FF] text-base">
						{selectedFramework?.name || 'No framework selected'}
					</p>
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">
						Cost: <span class="text-utama">{frameworkCost} cu</span>
					</p>
				</div>
			</div>
		</div>

		<!-- Model Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 400,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Model</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('aiModel')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					<p class="text-[#D9E4FF] text-base">
						{selectedModel
							? `${selectedModel.provider} ${selectedModel.name}`
							: 'No model selected'}
					</p>
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">Cost: <span class="text-utama">{modelCost} cu</span></p>
				</div>
			</div>
		</div>

		<!-- Voice Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 450,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Voice</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('aiVoice')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					<p class="text-[#D9E4FF] text-base">
						{formatVoiceSettings(selectedVoice)}
					</p>
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">Cost: <span class="text-utama">{voiceCost} cu</span></p>
				</div>
			</div>
		</div>
	</div>

	<div class="grid gap-4 sm:grid-cols-4 mb-4">
		<!-- Character Details Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 500,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Character Details</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('aiCharacterDetails')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					<p class="text-[#D9E4FF] text-base">
						<span class="text-[#ECF2FF] font-bold">Name:</span>
						{characterDetails.name || 'Unnamed Agent'}
					</p>
					<p class="text-[#D9E4FF] text-base">
						<span class="text-[#ECF2FF] font-bold">Bio:</span>
						{characterDetails.description || 'No description provided'}
					</p>
					<p class="text-[#D9E4FF] text-base">
						<span class="text-[#ECF2FF] font-bold">Agent Tone:</span>
						{getAgentToneName(characterDetails.personalization?.agentTone) || 'Not set'}
					</p>
					<p class="text-[#D9E4FF] text-base">
						<span class="text-[#ECF2FF] font-bold">Memory:</span>
						{formatMemorySettings(characterDetails.memory)}
					</p>
					<p class="text-[#D9E4FF] text-base">
						<span class="text-[#ECF2FF] font-bold">Your Name:</span>
						{characterDetails.personalization?.userName || 'Not set'}
					</p>
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">
						Cost: <span class="text-utama">{characterDetailsCost} cu</span>
					</p>
				</div>
			</div>
		</div>

		<!-- Knowledge Base Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full"
			in:fly|global={{
				delay: 525,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Knowledge Base</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('knowledgeBase')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					{#if knowledgeBase.uploadedFiles && knowledgeBase.uploadedFiles.length > 0}
						<div>
							<span class="text-[#ECF2FF] font-bold">Files:</span>
							{#each knowledgeBase.uploadedFiles as file}
								<p class="text-[#D9E4FF] text-sm">{file.name}</p>
							{/each}
						</div>
					{/if}

					{#if knowledgeBase.rawData && knowledgeBase.rawData.trim() !== ''}
						<div>
							<span class="text-[#ECF2FF] font-bold">Pasted Data:</span>
							<p class="text-[#D9E4FF] text-sm">
								{knowledgeBase.rawData.length > 100
									? knowledgeBase.rawData.substring(0, 100) + '...'
									: knowledgeBase.rawData}
							</p>
						</div>
					{/if}

					{#if (!knowledgeBase.uploadedFiles || knowledgeBase.uploadedFiles.length === 0) && (!knowledgeBase.rawData || knowledgeBase.rawData.trim() === '')}
						<p class="text-[#D9E4FF] text-base">No knowledge base configured</p>
					{/if}
				</div>
				<div class="p-4 space-y-4 flex justify-end">
					<p class="text-sm text-[#D9E4FF]">
						Cost: <span class="text-utama">{knowledgeBaseCost} cu</span>
					</p>
				</div>
			</div>
		</div>

		<!-- Agent Behavior Card -->
		<div
			class="card card-compact bg-black border border-[#444A61] rounded-md w-full relative overflow-hidden h-full col-span-2"
			in:fly|global={{
				delay: 550,
				duration: 500,
				x: -100,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex flex-col relative z-10 h-full">
				<!-- Card Header -->
				<div
					class="flex items-center justify-between gap-3 mb-4 p-4 bg-[#0C0D12] border-b border-[#444A61]"
				>
					<h2 class="text-[#ECF2FF]">Agent Behavior</h2>
					<button
						class="btn btn-sm px-4 bg-[#06070A] hover:bg-[#06070A] border border-[#444A61] hover:border-utama text-[#ECF2FF] text-base font-normal rounded-full disabled:bg-[#06070A] disabled:border-[#444A61] disabled:opacity-50"
						on:click={() => handleEditSection('agentBehavior')}
						disabled={isLoading}
					>
						Edit
					</button>
				</div>
				<div class="px-4 pb-4 space-y-4 flex-1">
					{#if agentBehavior && Object.keys(agentBehavior).length > 0}
						<div class="grid grid-cols-3 gap-4">
							{#if agentBehavior.reasoning}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Reasoning:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior.reasoning, 'reasoning') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
							{#if agentBehavior.acting}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Acting:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior.acting, 'acting') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
							{#if agentBehavior.observing}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Observing:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior.observing, 'observing') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
							{#if agentBehavior.planning}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Planning:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior.planning, 'planning') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
							{#if agentBehavior.collaborating}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Collaborating:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior.collaborating, 'collaborating') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
							{#if agentBehavior['self-refining']}
								<div>
									<h4 class="text-[#ECF2FF] text-sm font-bold">Self-Refining:</h4>
									<ul class="text-[#D9E4FF] text-xs">
										{#each formatBehaviorCategory(agentBehavior['self-refining'], 'self-refining') as behavior}
											<li>{behavior}</li>
										{/each}
									</ul>
								</div>
							{/if}
						</div>
					{:else}
						<p class="text-[#D9E4FF] text-base">No behavior settings configured</p>
					{/if}
				</div>
			</div>
		</div>
	</div>

	<div
		class="text-[#98A7C8] bg-[#0C0D12] border border-[#1F222D] py-2.5 px-6 rounded-full text-center font-medium"
	>
		Compute Unit: <span class="text-[#ECF2FF]"
			>{computeUnitsStore.current + newAgentCost}/{computeUnitsStore.total}</span
		>
	</div>

	<!-- Activate Buttons -->
	<div class="mt-8">
		<button
			class="btn bg-gradient-to-r from-[#06BF54] to-[#00200F] text-xl text-[#ECF2FF] uppercase font-normal border border-utama hover:border-utama rounded-full w-full hover:opacity-70 transition-all duration-200"
			on:click={handleActivate}
			disabled={isLoading || !canProceed}
			class:opacity-55={isLoading}
			class:cursor-not-allowed={isLoading}
		>
			{#if isLoading}
				Creating Agent<span class="dots">
					<span class="dot1">.</span><span class="dot2">.</span><span class="dot3">.</span>
				</span>
			{:else}
				Activate
			{/if}
		</button>
	</div>
</div>

<style>
	.dots {
		display: inline-block;
	}

	.dot1,
	.dot2,
	.dot3 {
		opacity: 0;
		animation: dotAnimation 1.5s infinite;
	}

	.dot1 {
		animation-delay: 0s;
	}

	.dot2 {
		animation-delay: 0.5s;
	}

	.dot3 {
		animation-delay: 1s;
	}

	@keyframes dotAnimation {
		0%,
		33% {
			opacity: 0;
		}
		34%,
		66% {
			opacity: 1;
		}
		67%,
		100% {
			opacity: 0;
		}
	}
</style>
