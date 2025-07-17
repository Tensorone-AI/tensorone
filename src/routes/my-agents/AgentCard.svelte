<script>
	// All logic moved to parent, this component is now purely presentational
	export let agent;
	export let onChatClick;
	export let onDeleteClick;
</script>

<div
	class="card card-compact bg-black border-2 border-[#1F222D] rounded-[18px] w-full relative overflow-hidden h-64 flex flex-col"
>
	<div class="card-body flex flex-col items relative z-10 flex-1">
		<div class="flex justify-between items-start space-x-2 bg-[#0C0D12] px-3 py-2 rounded-md">
			<div class="flex justify-between items-center w-full">
				<h2 class="card-title text-xl text-[#ECF2FF] font-normal">
					{agent.name || 'Unnamed Agent'}
				</h2>
				<span class="text-utama text-base bg-kedua px-3 py-1 rounded-full">
					{agent.computeUnit || 0} CU
				</span>
			</div>
			<button
				class="btn btn-ghost btn-sm w-8 h-8 min-h-8 p-0 text-[#939393] hover:text-red-400 hover:bg-red-400/10 transition-colors duration-200"
				on:click={onDeleteClick}
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
		</div>
		<div class="flex-1 flex items-center justify-center py-2 px-3 min-h-0 overflow-hidden">
			<p class="text-[#ECF2FF] text-sm leading-relaxed line-clamp-3">
				{agent.description || 'No Description'}
			</p>
		</div>
		<div class="card-actions w-full mt-auto">
			<button
				class="btn btn-secondary btn-sm border border-utama hover:border-utama hover:opacity-70 rounded-full font-normal px-3 h-9 w-full text-utama justify-center"
				on:click={onChatClick}
				><span class="text-base">Chat</span>
				<svg
					width="20"
					height="20"
					viewBox="0 0 25 25"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M5.66699 12.3333L19.667 12.3333"
						stroke="#23F784"
						style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M12.667 5.33331L19.667 12.3333L12.667 19.3333"
						stroke="#23F784"
						style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</button>
		</div>
	</div>
</div>
