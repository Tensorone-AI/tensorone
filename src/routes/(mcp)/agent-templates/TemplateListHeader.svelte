<script>
	// ========================================
	// PROPS
	// ========================================
	export let searchTerm = '';
	export let selectedCategory = '';
	export let selectedSort = '';
	export let categories = [];
	export let handleSearchChange = () => {};
	export let handleCategoryChange = () => {};
	export let handleSortChange = () => {};
</script>

<!-- Template List Header -->
<div class="mb-4 border-b-2 border-[#1F222D] pb-4 flex justify-between items-center gap-10">
	<div class="relative w-7/12">
		<svg
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			xmlns="http://www.w3.org/2000/svg"
			class="absolute top-3 left-3"
		>
			<path
				d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z"
				stroke="#BBD0FF"
				style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M20.9999 21L16.6499 16.65"
				stroke="#BBD0FF"
				style="stroke:#BBD0FF;stroke:color(display-p3 0.7333 0.8138 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
		<input
			type="text"
			placeholder="Search Templates"
			value={searchTerm}
			on:input={(e) => handleSearchChange(e.target.value)}
			class="input input-md bg-[#0C0D12] border border-[#444A61] text-[#ECF2FF] text-base placeholder:text-[#BBD0FF] rounded-full transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20 pl-14 w-full"
		/>
	</div>
	<div class="w-5/12 flex items-center gap-4">
		<span class="text-[#ECF2FF] text-2xl flex-shrink-0 whitespace-nowrap">Sort by</span>
		<select
			value={selectedCategory}
			on:change={(e) => handleCategoryChange(e.target.value)}
			class="select text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full min-w-0 flex-1 focus:border-utama focus:outline-none transition-colors duration-200 truncate"
		>
			<option value="">All Categories</option>
			{#each categories as category}
				<option value={category}>{category}</option>
			{/each}
		</select>

		<select
			value={selectedSort}
			on:change={(e) => handleSortChange(e.target.value)}
			class="select text-base px-4 bg-[#0C0D12] border border-[#444A61] rounded-full min-w-0 flex-1 focus:border-utama focus:outline-none transition-colors duration-200 truncate"
		>
			<option value="">Default</option>
			<option value="popularity">Most Popular</option>
			<option value="usage">Most Used</option>
			<option value="cost-low">Cost (Low to High)</option>
			<option value="cost-high">Cost (High to Low)</option>
			<option value="newest">Newest</option>
		</select>
	</div>
</div>

<style>
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
	.select {
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
