<script>
	import { fly } from 'svelte/transition';

	export let customVoiceFile;
	export let myClone;
	export let isLoadingClone = false;
	export let address;
	export let selectedVoiceType;
	export let onVoiceUpload;
	export let onTriggerUpload;
	export let onRemoveVoice;
	export let onToggleModal;
	export let onUploadClone;
	export let onDeleteClone;
	export let onToggleClone;

	// Clone is active if selectedVoiceType is 'clone'
	$: cloneActive = selectedVoiceType === 'clone';
</script>

<div
	class="mb-4 pb-4 border-b border-[#444A61]"
	in:fly={{ delay: 350, duration: 300, x: -50 }}
	out:fly={{ duration: 300, x: -50, opacity: 0 }}
>
	<div class="flex items-center gap-3 pb-4">
		<h4 class="text-[#ECF2FF] text-xl">Voice Clone</h4>
		<button
			class="btn btn-circle btn-outline bg-[#1F222D] hover:bg-[#1F222D] hover:border-utama btn-xs text-[#ECF2FF] hover:text-utama"
			on:click={onToggleModal}>i</button
		>
	</div>

	<!-- Hidden file input -->
	<input id="voice-upload" type="file" accept="audio/*" on:change={onVoiceUpload} class="hidden" />

	{#if myClone}
		<!-- Voice Clone Controls -->
		<div class="flex gap-2 w-full">
			<!-- Toggle Clone Button -->
			<button
				type="button"
				on:click={onToggleClone}
				class="flex items-center justify-center gap-2 rounded-full px-4 py-2 flex-1 transition-colors border text-[#ECF2FF]"
				class:bg-kedua={cloneActive}
				class:border-utama={cloneActive}
				class:bg-[#0C0D12]={!cloneActive}
				class:border-[#444A61]={!cloneActive}
				class:hover:border-utama={!cloneActive}
				disabled={isLoadingClone}
			>
				{#if isLoadingClone}
					<div class="loading loading-spinner loading-sm"></div>
				{:else}
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M8 1V3M8 13V15M15 8H13M3 8H1M12.243 3.757L10.828 5.172M5.172 10.828L3.757 12.243M12.243 12.243L10.828 10.828M5.172 5.172L3.757 3.757"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{/if}
				<span>My Clone</span>
			</button>

			<!-- Delete Clone Button -->
			<button
				type="button"
				on:click={onDeleteClone}
				class="flex items-center justify-center gap-2 rounded-full px-4 py-2 transition-colors border border-red-500 hover:bg-red-500 hover:text-white text-red-500"
				disabled={isLoadingClone}
			>
				<svg
					width="16"
					height="16"
					viewBox="0 0 16 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M2 4h12M5.333 4V2.667C5.333 2.298 5.479 1.944 5.741 1.682C6.003 1.420 6.357 1.274 6.726 1.274h2.548c.369 0 .723.146.985.408.262.262.408.616.408.985V4m2 0v9.333c0 .369-.146.723-.408.985-.262.262-.616.408-.985.408H4.667c-.369 0-.723-.146-.985-.408C3.420 14.056 3.274 13.702 3.274 13.333V4h9.452Z"
						stroke="currentColor"
						stroke-width="1.5"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
				<span>Delete</span>
			</button>
		</div>
	{:else}
		<!-- Upload Button -->
		<button
			type="button"
			on:click={onUploadClone}
			class="flex items-center justify-center gap-2 rounded-full px-4 py-2 w-full transition-colors"
			class:bg-kedua={customVoiceFile}
			class:border-utama={customVoiceFile}
			class:bg-[#0C0D12]={!customVoiceFile}
			class:border-[#444A61]={!customVoiceFile}
			class:hover:border-utama={!customVoiceFile}
			class:border={true}
			disabled={isLoadingClone}
		>
			{#if isLoadingClone}
				<div class="loading loading-spinner loading-sm"></div>
				<span class="text-[#ECF2FF]">Processing...</span>
			{:else if customVoiceFile}
				<span class="text-utama truncate flex-1">Click again to clone: {customVoiceFile.name}</span>

				<button
					type="button"
					on:click|stopPropagation={onRemoveVoice}
					class="ml-2 p-1 rounded-full hover:opacity-70 transition-all"
				>
					<svg
						width="14"
						height="14"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M14 2L2 14"
							stroke="#ECF2FF"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M2 2L14 14"
							stroke="#ECF2FF"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>
			{:else}
				<svg
					width="17"
					height="16"
					viewBox="0 0 17 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M14.5 10V12.6667C14.5 13.0203 14.3595 13.3594 14.1095 13.6095C13.8594 13.8595 13.5203 14 13.1667 14H3.83333C3.47971 14 3.14057 13.8595 2.89052 13.6095C2.64048 13.3594 2.5 13.0203 2.5 12.6667V10"
						stroke="#ECF2FF"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M11.8334 5.33333L8.50008 2L5.16675 5.33333"
						stroke="#ECF2FF"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path d="M8.5 2V10" stroke="#ECF2FF" stroke-linecap="round" stroke-linejoin="round" />
				</svg>
				<span class="text-[#ECF2FF]">Upload Voice Sample</span>
			{/if}
		</button>
	{/if}
</div>
