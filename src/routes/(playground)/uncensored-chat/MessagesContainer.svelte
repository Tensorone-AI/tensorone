<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import Computer from './Computer.svelte';
	import User from './User.svelte';

	export let conversation;
	export let isLoading;
	export let container;
	export let copyStates;
	export let currentConversationId;
	export let onScroll;
	export let onCopyMessage;
</script>

<div
	class="messages-scrollbar h-[calc(100vh-24rem)] overflow-y-auto scroll-smooth overflow-x-hidden font-inter"
	bind:this={container}
	on:scroll={onScroll}
	in:fade|global={{ delay: 600, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<div class="mx-52 pt-2">
		{#if conversation.length !== 0}
			{#each conversation as { type, message }, index}
				<div
					in:fly|global={{
						delay: 600,
						duration: 1500,
						x: type === 'assistant' ? -30 : 30,
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 200 }}
				>
					{#if type === 'assistant'}
						<Computer {message} />
					{:else}
						<User
							{message}
							messageId={`${currentConversationId}-${index}`}
							copyState={copyStates[`${currentConversationId}-${index}`] || 'default'}
							onCopy={onCopyMessage}
						/>
					{/if}
				</div>
			{/each}
		{/if}
		{#if isLoading}
			<div
				class="flex items-center gap-2 p-4"
				in:fade={{ duration: 300 }}
				out:fade={{ duration: 200 }}
			>
				<span class="loading loading-dots loading-sm text-[#ECF2FF]"></span>
				<span class="text-[#ECF2FF] text-sm">AI is thinking...</span>
			</div>
		{/if}
	</div>
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
