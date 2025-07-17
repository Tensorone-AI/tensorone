<script>
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	// Props for backend integration - all logic moved to parent
	export let navigationData = {};
	export let statusBadgeConfig = {};
	export let visibilityBadgeConfig = {};
	export let getTabClasses = () => '';

	// Event handlers - dispatch the correct events that parent expects
	function handleTabSelect(tab) {
		// Dispatch the same event that the parent handleTabChange expects
		dispatch('tab-change', {
			previousTabId: navigationData.activeTabId,
			newTabId: tab.id,
			tabData: tab
		});
	}

	function handleTabKeydown(event, tab) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleTabSelect(tab);
		}
	}
</script>

<nav
	class="flex justify-between items-center border-b-2 border-[#1F222D] pb-4 mb-4"
	aria-label="Navigation tabs"
	in:fade|global={{ delay: 300, duration: 500 }}
>
	<div role="tablist" class="flex bg-[#0C0D12] border border-[#1F222D] rounded-full">
		{#each navigationData.tabs as tab (tab.id)}
			<button
				on:click={() => handleTabSelect(tab)}
				on:keydown={(e) => handleTabKeydown(e, tab)}
				class={getTabClasses(tab, navigationData.activeTabId === tab.id, false)}
				disabled={tab.disabled || navigationData.isLoading}
				role="tab"
				aria-selected={navigationData.activeTabId === tab.id}
				aria-controls="{tab.id}-panel"
				tabindex={navigationData.activeTabId === tab.id ? 0 : -1}
				title={tab.disabled ? `${tab.label} is currently unavailable` : tab.label}
			>
				<span>{tab.label}</span>
			</button>
		{/each}
	</div>
	<!-- Status Badges -->
	<div class="flex space-x-2">
		<!-- Reactive Visibility Badge -->
		<span class={visibilityBadgeConfig.classes}>{visibilityBadgeConfig.text}</span>

		<!-- Reactive Status Badge -->
		<span class={statusBadgeConfig.classes}>{statusBadgeConfig.text}</span>
	</div>
</nav>

<style>
	/* Smooth scrolling for horizontal navigation on mobile */
	nav {
		overflow-x: auto;
		scrollbar-width: none;
		-ms-overflow-style: none;
	}

	nav::-webkit-scrollbar {
		display: none;
	}

	/* Ensure buttons don't shrink on mobile */
	button {
		flex-shrink: 0;
		white-space: nowrap;
	}
</style>
