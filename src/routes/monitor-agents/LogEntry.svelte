<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let log;
	export let showTimestamps;
	export let isSelected = false;
	export let getLogLevelClass;
	export let getBorderLevelClass;

	function handleClick() {
		dispatch('select', { logId: log.id });
	}
</script>

<div
	class="mb-1 hover:bg-white/5 px-2 py-1 cursor-pointer transition-all duration-200 border-l-2 {isSelected
		? getBorderLevelClass(log.level)
		: 'border-l-transparent'}"
	on:click={handleClick}
	role="button"
	tabindex="0"
	on:keydown={(e) => e.key === 'Enter' && handleClick()}
>
	<div class="flex items-start space-x-2">
		{#if showTimestamps}
			<span class="text-[#98A7C8] text-xs flex-shrink-0 mt-0.5">[{log.timestamp}]</span>
		{/if}
		<span class="{getLogLevelClass(log.level)} font-medium flex-shrink-0 mt-0.5">{log.level}:</span>
		<span class="text-[#ECF2FF] flex-1">{log.message}</span>
	</div>

	{#if isSelected && log.details}
		<div
			class="mt-2 ml-6 p-2 bg-[#0C0D12] border border-[#1F222D] rounded-xl text-xs text-[#BBD0FF]"
		>
			<span>Details:</span>
			<pre class="mt-1 font-iosevka">{JSON.stringify(log.details, null, 2)}</pre>
		</div>
	{/if}
</div>
