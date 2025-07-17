<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import MessageList from './MessageList.svelte';
	import ChatInput from './ChatInput.svelte';
	import TalkMode from './TalkMode.svelte';

	export let conversation = [];
	export let isLoading = false;
	export let messagesContainer;
	export let prompt = '';
	export let chatTitle = '';
	export let handleScroll = () => {};
	export let updatePrompt = () => {};
	export let handleKeydown = () => {};
	export let sendMessage = () => {};
	export let handleTalkModeToggle = () => {};
	export let handleBackToChat = () => {};
	export let isTalkMode = false;

	export let voiceLevel = 0;
	export let statusText = '';
	export let isListening = false;
	export let isProcessing = false;
	export let isAgentSpeaking = false;
	export let startListening = () => {};
	export let stopListening = () => {};
	export let startCallModeRecording = () => {};
	export let stopCallModeRecording = () => {};
	export let stopCurrentAudio = () => {};

	export let copyStates = {};
	export let handleCopy = () => {};
	export let hasCallFeature = false;
	export let microphoneStream = null;
</script>

<div
	class="relative bg-black border border-[#444A61] rounded-xl h-[calc(100vh-11rem)]"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	{#if isTalkMode}
		<!-- Talk Mode - Standalone voice conversation -->
		<div class="h-full w-full">
			<TalkMode
				{voiceLevel}
				{statusText}
				{isListening}
				{isProcessing}
				{isAgentSpeaking}
				{startListening}
				{stopListening}
				{startCallModeRecording}
				{stopCallModeRecording}
				{stopCurrentAudio}
				{handleBackToChat}
				{hasCallFeature}
				{microphoneStream}
			/>
		</div>
	{:else}
		<!-- Chat Mode -->
		<!-- Messages Container -->
		<div
			class="messages-scrollbar h-[calc(100vh-17rem)] overflow-y-auto scroll-smooth overflow-x-hidden"
			bind:this={messagesContainer}
			on:scroll={handleScroll}
			in:fade|global={{ delay: 600, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<div class="mx-52 pt-2">
				<MessageList {conversation} {isLoading} {chatTitle} {copyStates} {handleCopy} />
			</div>
		</div>

		<!-- Chat Input -->
		<div
			class="p-4 lg:px-7 lg:py-3 w-full bottom-0 z-100 absolute"
			in:fly={{
				delay: 700,
				duration: 600,
				y: 50,
				opacity: 0,
				easing: quintOut
			}}
			out:fade={{ duration: 200 }}
		>
			<ChatInput
				{isLoading}
				{prompt}
				{updatePrompt}
				{handleKeydown}
				{sendMessage}
				{handleTalkModeToggle}
				{hasCallFeature}
			/>
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
