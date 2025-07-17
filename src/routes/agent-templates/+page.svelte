<script>
	// ========================================
	// IMPORTS & INITIAL SETUP
	// ========================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import AgentCard from './AgentCard.svelte';
	import TemplateListHeader from './TemplateListHeader.svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { wallet } from '$lib/stores/wallet';
	import { supabase } from '$lib/db/supabaseClient';

	// ========================================
	// PROPS
	// ========================================
	export let data = {}; // Add default value for data prop if needed

	// ========================================
	// INLINE DATA
	// ========================================

	// Agent Templates data from Supabase
	let agentTemplates = [];
	let categories = [];

	// Function to fetch agent templates from Supabase
	async function fetchAgentTemplates() {
		try {
			const { data: templatesData, error } = await supabase
				.from('prebuilt-mcp')
				.select('*')
				.order('id', { ascending: true });

			if (error) {
				console.error('Error fetching agent templates:', error);
				return;
			}

			// Transform data to match expected format
			agentTemplates =
				templatesData?.map((template) => ({
					id: template.id,
					name: template.agent_name,
					category: template.category,
					popularity: template.popularity,
					usageCount: template.usageCount,
					description: template.description,
					tags: Array.isArray(template.tags) ? template.tags : JSON.parse(template.tags || '[]'),
					estimatedCost: parseInt(template.total_cu) || 0,
					lastUpdated: template.lastUpdated,
					complexity: template.complexity,
					config: template.config,
					slug: template.slug || template.id
				})) || [];

			// Extract unique categories
			categories = [...new Set(agentTemplates.map((template) => template.category))].sort();
		} catch (error) {
			console.error('Error fetching agent templates:', error);
		}
	}

	// Derive address from data or wallet store (assuming wallet connects to database)
	$: address = data?.address || $wallet?.address || '';

	// Available compute units from GPU table
	let availableComputeUnits = 0;

	// Function to fetch total compute units from GPU table
	async function fetchAvailableComputeUnits() {
		if (!address) return;

		try {
			const { data: gpuData, error } = await supabase
				.from('gpu')
				.select('compute')
				.eq('address', address);

			if (error) {
				console.error('Error fetching GPU compute units:', error);
				return;
			}

			// Sum all compute values
			availableComputeUnits = gpuData?.reduce((sum, gpu) => sum + (gpu.compute || 0), 0) || 0;
		} catch (error) {
			console.error('Error fetching available compute units:', error);
		}
	}

	// Component lifecycle for initial data loading
	onMount(() => {
		// Fetch agent templates and available compute units when component mounts
		fetchAgentTemplates();
		fetchAvailableComputeUnits();

		// Allow initial transitions to complete
		setTimeout(() => {
			isInitialLoad = false;
		}, 2000); // Give time for all initial animations to complete
	});

	// Reactive statement to refetch compute units when wallet address changes
	$: if (address) {
		fetchAvailableComputeUnits();
	}

	// ========================================
	// 2. REACTIVITY ONLY
	// ========================================

	// Local state for filtering and searching
	let searchTerm = '';
	let selectedCategory = '';
	let selectedSort = '';
	let isInitialLoad = true;
	let filterKey = 0; // Key to force re-render during filtering

	// Reactive filtered templates based on search and category
	$: filteredTemplates = agentTemplates.filter((template) => {
		const matchesSearch =
			!searchTerm ||
			template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
			template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
			template.tags.some((tag) => tag.toLowerCase().includes(searchTerm.toLowerCase()));

		const matchesCategory = !selectedCategory || template.category === selectedCategory;

		return matchesSearch && matchesCategory;
	});

	// Reactive sorted templates based on selected sort option
	$: sortedTemplates = (() => {
		const templates = [...filteredTemplates];

		switch (selectedSort) {
			case 'popularity':
				return templates.sort((a, b) => b.popularity - a.popularity);
			case 'usage':
				return templates.sort((a, b) => b.usageCount - a.usageCount);
			case 'cost-low':
				return templates.sort((a, b) => a.estimatedCost - b.estimatedCost);
			case 'cost-high':
				return templates.sort((a, b) => b.estimatedCost - a.estimatedCost);
			case 'newest':
				return templates.sort((a, b) => new Date(b.lastUpdated) - new Date(a.lastUpdated));
			default:
				return templates;
		}
	})();

	// ========================================
	// 3. DATA INPUT TO DATABASE
	// ========================================

	// Event handlers for child components (filters that might trigger database updates)
	function handleSearchChange(value) {
		searchTerm = value;
		// Force re-render with transitions
		filterKey += 1;
		// Note: Search analytics could be saved to database here
	}

	function handleCategoryChange(value) {
		selectedCategory = value;
		// Force re-render with transitions
		filterKey += 1;
		// Note: Category selection analytics could be saved to database here
	}

	function handleSortChange(value) {
		selectedSort = value;
		// Force re-render with transitions
		filterKey += 1;
		// Note: Sort preference could be saved to database here
	}

	// Template selection handler (saves usage data to database)
	function handleTemplateSelect(event) {
		const selectedTemplate = event.detail.agent;
		console.log('Template selected:', selectedTemplate);

		// Note: Template usage count could be incremented in database here
		// Note: User interaction analytics could be saved to database here

		// Navigate directly to chat with the selected template
		goto(`/chat-agent/${selectedTemplate.slug}`);
	}

	// Agent card click handler (saves interaction data to database)
	function handleAgentCardClick(agent) {
		// Note: Agent card click analytics could be saved to database here
		handleTemplateSelect({ detail: { agent } });
	}
</script>

<svelte:head>
	<title>Browse Agent Templates</title>
	<meta name="description" content="Browse and select from our collection of AI agent templates" />
</svelte:head>

<Header />

<!-- Agent Templates List View -->
<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
	<PageTitle subtitle="AI Agent Templates" title="Browse Agent Templates" {address} />

	<div
		class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start"
		in:fade|global={{ delay: 300, duration: 500 }}
		out:fade|global={{ duration: 300 }}
	>
		<div>
			<!-- Template List Header Component -->
			<TemplateListHeader
				{searchTerm}
				{selectedCategory}
				{selectedSort}
				{categories}
				{handleSearchChange}
				{handleCategoryChange}
				{handleSortChange}
			/>

			<!-- Template Cards -->
			<div class="flex-1 min-h-0 flex flex-col">
				{#key filterKey}
					<div
						class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 grid-rows-[repeat(auto-fit,min-content)]"
						in:fade={{ delay: 300, duration: 500 }}
						out:fade={{ duration: 300 }}
					>
						{#each sortedTemplates as agent, index (agent.id)}
							<div
								class="h-full"
								in:fly|global={isInitialLoad
									? {
											delay: 300 + index * 100,
											duration: 1000,
											x: -100,
											opacity: 0,
											easing: quintOut
										}
									: {
											delay: index * 50,
											duration: 300,
											opacity: 0
										}}
								out:fade|global={{ duration: 200 }}
							>
								<AgentCard {agent} {availableComputeUnits} onCardClick={handleAgentCardClick} />
							</div>
						{/each}
					</div>
				{/key}
			</div>
		</div>
	</div>
</section>
