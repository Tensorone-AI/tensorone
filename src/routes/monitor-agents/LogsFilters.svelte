<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	// Props passed from parent - all data now centralized
	export let logsData;
	export let logLevels;
	export let logSources;

	// Reactive state based on agent availability
	$: hasAgent = logsData.agent != null;

	function handleFilterChange(filterType, value) {
		dispatch('filter-change', { filterType, value });
	}
</script>

<div class="p-4 bg-[#06070A]">
	<div class="flex items-center space-x-4">
		<!-- Search -->
		<div class="relative flex-1 max-w-md">
			<input
				value={logsData.filters?.searchQuery || ''}
				on:input={(e) => handleFilterChange('searchQuery', e.target.value)}
				placeholder="Search logs..."
				class="w-full bg-[#06070A] border border-[#444A61] rounded-full px-3 py-2 pr-8 text-sm text-[#ECF2FF] placeholder-[#BBD0FF] focus:outline-none focus:border-utama transition-all duration-200"
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

		<!-- Level Filter -->
		<select
			value={logsData.filters?.level || 'all'}
			on:change={(e) => handleFilterChange('level', e.target.value)}
			disabled={!hasAgent}
			class="select select-sm text-sm pl-6 pr-8 h-9 bg-[#06070A] border border-[#444A61] rounded-full text-[#ECF2FF] focus:outline-none transition-colors duration-200 {hasAgent
				? 'focus:border-utama cursor-pointer'
				: 'opacity-50 cursor-not-allowed'}"
		>
			<option value="all">{hasAgent ? 'All Levels' : 'No Agent'}</option>
			{#each logLevels as level}
				<option value={level.toLowerCase()}>{level}</option>
			{/each}
		</select>

		<!-- Source Filter -->
		<select
			value={logsData.filters?.source || 'all'}
			on:change={(e) => handleFilterChange('source', e.target.value)}
			disabled={!hasAgent}
			class="select select-sm text-sm pl-6 pr-8 h-9 bg-[#06070A] border border-[#444A61] rounded-full text-[#ECF2FF] focus:outline-none transition-colors duration-200 {hasAgent
				? 'focus:border-utama cursor-pointer'
				: 'opacity-50 cursor-not-allowed'}"
		>
			<option value="all">{hasAgent ? 'All Sources' : 'No Agent'}</option>
			{#each logSources as source}
				<option value={source}>{source}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
	select {
		--select-option-bg: #000000;
	}

	select option {
		background-color: var(--select-option-bg);
		color: white;
		padding: 8px 12px;
	}

	select option:hover,
	select option:focus {
		background-color: #23f784;
		color: black;
	}

	select option:checked {
		background-color: #23f784;
		color: black;
	}

	/* Custom scrollbar for select dropdowns */
	select::-webkit-scrollbar {
		width: 8px;
	}

	select::-webkit-scrollbar-track {
		background: #1a1a1a;
	}

	select::-webkit-scrollbar-thumb {
		background: #23f784;
		border-radius: 4px;
	}
</style>
