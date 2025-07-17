<script>
	export let chatItems = [];
	export let ontoggleActiveHistory;
	export let onToggleDeleteModal;
</script>

<div class="h-[calc(100vh-17rem)] messages-scrollbar overflow-y-auto">
	<ul class="text-[#ECF2FF] text-sm px-4 space-y-5">
		{#each chatItems as item (item.id)}
			<li class="flex justify-between items-center" class:text-primary={item.isActive}>
				<button
					class="overflow-hidden whitespace-nowrap text-ellipsis max-w-[calc(100%-3rem)] hover:text-utama transition-colors duration-200"
					on:click={() => ontoggleActiveHistory(item.id)}
					title={item.title}>{item.title}</button
				>
				<button
					class="btn btn-ghost btn-sm w-8 h-8 min-h-8 p-0 text-[#939393] hover:text-red-400 hover:bg-red-400/10 transition-colors duration-200"
					on:click={() => onToggleDeleteModal(item)}
					title="Delete"
				>
					<svg
						class="w-4 h-4"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						></path>
					</svg>
				</button>
			</li>
		{/each}
	</ul>
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
