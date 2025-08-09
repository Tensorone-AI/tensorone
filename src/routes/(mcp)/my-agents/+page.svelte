<script>
	// ========================================
	// IMPORTS & INITIAL SETUP
	// ========================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import AgentCard from './AgentCard.svelte';
	import NewAgentCard from './NewAgentCard.svelte';
	import DeleteAgentModal from './DeleteAgentModal.svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { wallet } from '$lib/stores/wallet';
	import { supabase } from '$lib/db/supabaseClient.js';

	// ========================================
	// PROPS & STATE VARIABLES
	// ========================================
	export let data = {};

	let title = 'My Agent';
	let selectedAgent = null;
	let showDeleteModal = false;
	let agentToDelete = null;
	let agents = [];
	let loading = false;
	let error = null;

	// ========================================
	// 1. FETCHING FROM DATABASE
	// ========================================

	async function loadAgents() {
		if (!$wallet.address) {
			console.warn('No wallet address available');
			return;
		}

		loading = true;
		error = null;

		try {
			const { data: agentsData, error: supabaseError } = await supabase
				.from('mcp')
				.select('*')
				.eq('address', $wallet.address)
				.order('id', { ascending: false });

			if (supabaseError) {
				console.error('Error fetching agents from Supabase:', supabaseError);
				error = `Failed to load agents: ${supabaseError.message}`;
				return;
			}

			// Handle the case when agents array might be empty or undefined
			const agentsArray = agentsData || [];
			agents = agentsArray.map((agent) => ({
				id: agent.id,
				slug: agent.slug,
				name: agent.agent_name,
				computeUnit: agent.total_cu,
				description: agent.description,
				status: 'running'
			}));
		} catch (err) {
			error = 'Network error while loading agents';
			console.error('Error loading agents:', err);
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		loadAgents();
	});

	// ========================================
	// 2. REACTIVITY ONLY
	// ========================================

	// Reactive statements for data derivation and UI state
	$: address = data?.address || $wallet?.address || '';

	// Reactively load agents when wallet address changes
	$: if ($wallet.address && $wallet.address !== address) {
		loadAgents();
	}

	// ========================================
	// 3. DATA INPUT TO DATABASE
	// ========================================

	async function handleDeleteModalConfirm() {
		if (agentToDelete) {
			try {
				const response = await fetch('/api/mcp/delete-my-agent', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						id: agentToDelete.id
					})
				});

				const result = await response.json();

				if (result.success) {
					// Remove agent from local state after successful deletion
					agents = agents.filter((agent) => agent.id !== agentToDelete.id);
					console.log('Agent deleted successfully:', agentToDelete.id);
				} else {
					console.error('Failed to delete agent:', result.error);
					error = result.error || 'Failed to delete agent';
				}
			} catch (err) {
				console.error('Error deleting agent:', err);
				error = 'Network error while deleting agent';
			}
		}
		showDeleteModal = false;
		agentToDelete = null;
	}

	// ========================================
	// UI EVENT HANDLERS (No Database Operations)
	// ========================================

	function handleAgentChatClick(agent) {
		selectedAgent = agent;
		console.log('Starting chat with agent:', selectedAgent);
		goto(`/chat-agent/${selectedAgent.slug}`);
	}

	function handleAgentDeleteClick(agent) {
		agentToDelete = agent;
		showDeleteModal = true;
	}

	function handleNewAgent() {
		goto('/create-agent');
	}

	function handleDeleteModalClose() {
		showDeleteModal = false;
		agentToDelete = null;
	}
</script>

<svelte:head>
	<title>Agent List</title>
	<meta name="description" content="Manage your AI agents and compute units" />
</svelte:head>

<Header />

<!-- Agents List View -->
<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
	<PageTitle subtitle="My Agents" title="Select an Existing Agent" {address} />

	<!-- Agent's Cards -->
	<div
		class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 grid-rows-[repeat(auto-fit,min-content)] bg-black rounded-xl border border-[#444A61] p-7 flex-1 overflow-y-auto content-start"
		in:fade={{ delay: 300, duration: 500 }}
		out:fade={{ duration: 300 }}
	>
		{#if loading}
			<div class="col-span-full flex justify-center items-center py-10">
				<div class="loading loading-spinner loading-lg text-utama"></div>
				<span class="ml-3 text-white">Loading agents...</span>
			</div>
		{:else if error}
			<div class="col-span-full flex flex-col justify-center items-center py-10">
				<div class="text-red-500 text-center">
					<h3 class="text-lg font-semibold mb-2">Error Loading Agents</h3>
					<p class="text-sm">{error}</p>
				</div>
				<button class="btn btn-primary mt-4" on:click={loadAgents}> Try Again </button>
			</div>
		{:else if agents.length === 0}
			<div
				class="h-full"
				in:fly|global={{
					delay: 300,
					duration: 1000,
					x: -100 * (agents.length + 1),
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				<NewAgentCard onCreateClick={handleNewAgent} />
			</div>
		{:else}
			{#each agents as agent, index (agent.id)}
				<div
					class="h-full"
					in:fly|global={{
						delay: 300,
						duration: 1000,
						x: -100 * (index + 1),
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
				>
					<AgentCard
						{agent}
						onChatClick={() => handleAgentChatClick(agent)}
						onDeleteClick={() => handleAgentDeleteClick(agent)}
					/>
				</div>
			{/each}
			<div
				class="h-full"
				in:fly|global={{
					delay: 300,
					duration: 1000,
					x: -100 * (agents.length + 1),
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				<NewAgentCard onCreateClick={handleNewAgent} />
			</div>
		{/if}
	</div>
</section>

<!-- Delete Modal -->
<DeleteAgentModal
	{showDeleteModal}
	agentName={agentToDelete?.name || 'Unnamed Agent'}
	onClose={handleDeleteModalClose}
	onConfirm={handleDeleteModalConfirm}
/>
