<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import Computer from './Computer.svelte';
	import User from './User.svelte';

	export let conversation = [];
	export let isLoading = false;
	export let chatTitle = '';
	export let copyStates = {};
	export let handleCopy = () => {};
</script>

<!-- Welcome Message -->
{#if conversation.length === 0}
	<div
		in:fly={{
			delay: 900,
			duration: 600,
			y: 30,
			opacity: 0,
			easing: quintOut
		}}
	>
		<Computer {chatTitle} message={"Hello! I'm your AI agent. How can I help you today?"} />
	</div>
{/if}

<!-- Conversation Messages with Loading Indicator in between -->
{#each conversation as { type, message }, index (type + index)}
	<div
		in:fly={{
			delay: 600 + index * 100,
			duration: 1500,
			x: type === 'assistant' ? -30 : 30,
			opacity: 0,
			easing: quintOut
		}}
		out:fade={{ duration: 200 }}
	>
		{#if type === 'assistant'}
			<Computer {chatTitle} {message} />
		{:else}
			<User {message} copyState={copyStates[message] || 'default'} {handleCopy} />
		{/if}
	</div>

	<!-- Show loading indicator after user message when loading -->
	{#if isLoading && type === 'user' && index === conversation.length - 1}
		<div
			class="flex items-center gap-2 p-4"
			in:fade={{ duration: 300 }}
			out:fade={{ duration: 200 }}
		>
			<span class="loading loading-dots loading-sm text-[#ECF2FF]"></span>
			<span class="text-[#ECF2FF] text-sm">AI is thinking...</span>
		</div>
	{/if}
{/each}
