<script>
	import { createEventDispatcher } from 'svelte';
	import FileExplorer from './FileExplorer.svelte';
	import CodeEditor from './CodeEditor.svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	const dispatch = createEventDispatcher();

	// Data passed from parent - all state management now centralized
	export let fileExplorerData = {};
	export let codeEditorData = {};
	export let isFullscreen = false;
	export let formatFileSize = () => '0 B';
	export let getSyntaxClass = () => 'language-text';

	// Code editor state and functions passed from parent
	export let isCopied = false;
	export let handleFileSelect = () => {};
	export let handleDownload = () => {};
	export let handleSearchInput = () => {};
	export let toggleFullscreen = () => {};
	export let handleCopy = () => {};

	// Event handlers - now just dispatch to parent
	function handleFileSelectEvent(event) {
		dispatch('file-select', event.detail);
	}

	function handleCodeEdit(event) {
		dispatch('code-edit', event.detail);
	}

	function handleFullscreenToggle(event) {
		dispatch('fullscreen-toggle', event.detail);
	}

	function handleFileDownload(event) {
		dispatch('file-download', event.detail);
	}

	function handleCodeCopy(event) {
		dispatch('code-copy', event.detail);
	}

	function handleSearchQueryChange(event) {
		dispatch('search-query-change', event.detail);
	}
</script>

<!-- Code Page Layout -->
<div
	class="flex h-full border border-[#444A61] rounded-xl"
	in:fly|global={{ delay: 400, duration: 150, y: -50, opacity: 0, easing: quintOut }}
	class:fullscreen={isFullscreen}
>
	<FileExplorer
		files={fileExplorerData.files}
		selectedFileId={fileExplorerData.selectedFileId}
		searchQuery={fileExplorerData.searchQuery}
		{formatFileSize}
		{handleFileSelect}
		{handleDownload}
		{handleSearchInput}
		on:file-select={handleFileSelectEvent}
		on:file-download={handleFileDownload}
		on:search-query-change={handleSearchQueryChange}
	/>

	<CodeEditor
		agent={codeEditorData.agent}
		activeFile={codeEditorData.activeFile}
		lastUpdated={codeEditorData.lastUpdated}
		{formatFileSize}
		{getSyntaxClass}
		{isCopied}
		{toggleFullscreen}
		{handleCopy}
		on:code-edit={handleCodeEdit}
		on:fullscreen-toggle={handleFullscreenToggle}
		on:code-copy={handleCodeCopy}
	/>
</div>

<style>
	.fullscreen {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 50;
	}
</style>
