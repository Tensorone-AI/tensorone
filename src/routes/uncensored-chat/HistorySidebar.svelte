<script>
	import { fade, fly } from 'svelte/transition';
	import HistoryList from './HistoryList.svelte';

	export let chatItems;
	export let isSidebarOpen;
	export let onToggleActiveHistory;
	export let onToggleDeleteModal;
	export let onToggleSidebar;
</script>

<div
	class={`hidden lg:block h-[calc(100vh-11rem)] relative bg-black border-l border-b border-[#444A61] rounded-tr-xl rounded-br-xl transition-all duration-300 ease-in-out overflow-hidden ${isSidebarOpen ? 'lg:w-1/5' : 'lg:w-12'}`}
>
	<!-- History Header -->
	<div
		class="flex items-center bg-[#0C0D12] border-b border-[#444A61] py-3 rounded-tr-xl rounded-br-xl min-h-[74px] transition-all duration-300 ease-in-out"
		class:justify-between={isSidebarOpen}
		class:justify-center={!isSidebarOpen}
		class:px-4={isSidebarOpen}
		class:px-2={!isSidebarOpen}
		class:mb-4={isSidebarOpen}
	>
		<button
			class="btn btn-sm bg-transparent border-transparent hover:bg-transparent hover:border-transparent hover:opacity-70 p-0 transition-transform duration-300 ease-in-out"
			on:click={onToggleSidebar}
		>
			<svg
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
				class="transition-transform duration-300 ease-in-out"
				class:rotate-180={!isSidebarOpen}
			>
				<path
					d="M9 18L15 12L9 6"
					stroke="#ECF2FF"
					style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
	</div>

	<!-- History List - only show when sidebar is open -->
	{#if isSidebarOpen}
		<div in:fade={{ delay: 150, duration: 200 }} out:fade={{ duration: 150 }}>
			<HistoryList
				{chatItems}
				ontoggleActiveHistory={onToggleActiveHistory}
				{onToggleDeleteModal}
			/>
		</div>
	{/if}
</div>
