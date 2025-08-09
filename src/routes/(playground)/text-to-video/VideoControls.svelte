<script>
	export let isPlaying;
	export let togglePlay;
	export let skipBackward;
	export let skipForward;
</script>

<div class="flex items-center justify-center gap-4 mb-4">
	<button
		on:click={skipBackward}
		class="bg-[#1F222D] border border-[#444A61] rounded-full w-[66px] h-8 hover:opacity-70 transition-all duration-200 flex items-center justify-center"
	>
		<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M7.33325 3.33342L1.33325 8.00008L7.33325 12.6667L7.33325 3.33342Z"
				stroke="#D9E4FF"
				style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M14.6667 3.33342L8.66675 8.00008L14.6667 12.6667L14.6667 3.33342Z"
				stroke="#D9E4FF"
				style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
	</button>
	<button
		on:click={togglePlay}
		class="bg-[#1F222D] border border-[#444A61] rounded-full w-[66px] h-8 hover:opacity-70 transition-all duration-200 flex items-center justify-center"
	>
		{#if isPlaying}
			<svg width="8" height="12" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
				<rect
					width="2"
					height="12"
					rx="1"
					fill="#D9E4FF"
					style="fill:#D9E4FF;fill:color(display-p3 0.8500 0.8953 1.0000);fill-opacity:1;"
				/>
				<rect
					x="6"
					width="2"
					height="12"
					rx="1"
					fill="#D9E4FF"
					style="fill:#D9E4FF;fill:color(display-p3 0.8500 0.8953 1.0000);fill-opacity:1;"
				/>
			</svg>
		{:else}
			<svg width="9" height="12" viewBox="0 0 9 12" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path
					d="M1.66675 10.6666L7.66675 5.99992L1.66675 1.33325L1.66675 10.6666Z"
					stroke="#D9E4FF"
					style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		{/if}
	</button>
	<button
		on:click={skipForward}
		class="bg-[#1F222D] border border-[#444A61] rounded-full w-[66px] h-8 hover:opacity-70 transition-all duration-200 flex items-center justify-center"
	>
		<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M8.66675 12.6666L14.6667 7.99992L8.66675 3.33325L8.66675 12.6666Z"
				stroke="#D9E4FF"
				style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M1.33325 12.6666L7.33325 7.99992L1.33325 3.33325L1.33325 12.6666Z"
				stroke="#D9E4FF"
				style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
	</button>
</div>
