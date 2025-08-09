<script>
	export let isLoading = false;
	export let prompt = '';
	export let updatePrompt = () => {};
	export let handleKeydown = () => {};
	export let sendMessage = () => {};
	export let handleTalkModeToggle = () => {};
	export let hasCallFeature = false;
</script>

<div class="col-span-12 relative mx-44">
	<!-- Text Input -->
	<textarea
		class="textarea w-full h-16 text-[#ECF2FF] text-base placeholder:text-[#444A61] pl-8 pr-20 pt-[18px] bg-[#0C0D12] border border-[#444A61] rounded-full disabled:opacity-50 disabled:bg-[#0C0D12] resize-none overflow-y-auto transition-all duration-200 focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
		placeholder="Ask Anything"
		bind:value={prompt}
		on:input={updatePrompt}
		on:keydown={handleKeydown}
		disabled={isLoading}
		style="resize: none; overflow-y: auto;"
	/>

	<div class="absolute bottom-[20px] right-5 flex items-center gap-3">
		<!-- Call/Talk Button - Show when call feature is available -->
		{#if hasCallFeature}
			<button
				class="hover:opacity-70 transition-all duration-200"
				on:click={handleTalkModeToggle}
				title="Switch to voice mode"
			>
				<svg
					width="36"
					height="36"
					viewBox="0 0 32 32"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M0 16C0 7.16344 7.16344 0 16 0C24.8366 0 32 7.16344 32 16C32 24.8366 24.8366 32 16 32C7.16344 32 0 24.8366 0 16Z"
						fill="#444A61"
						style="fill:#444A61;fill:color(display-p3 0.2670 0.2910 0.3792);fill-opacity:1;"
					/>
					<g clip-path="url(#clip0_773_2962)">
						<path
							d="M17.0336 12.3334C17.6848 12.4605 18.2832 12.7789 18.7523 13.248C19.2214 13.7172 19.5399 14.3156 19.6669 14.9667M17.0336 9.66675C18.3865 9.81704 19.648 10.4229 20.6111 11.3848C21.5742 12.3466 22.1816 13.6074 22.3336 14.9601M21.6669 20.2801V22.2801C21.6677 22.4657 21.6297 22.6495 21.5553 22.8196C21.4809 22.9898 21.3718 23.1425 21.235 23.268C21.0982 23.3935 20.9367 23.4891 20.7608 23.5486C20.5849 23.608 20.3985 23.6301 20.2136 23.6134C18.1622 23.3905 16.1916 22.6895 14.4603 21.5667C12.8495 20.5432 11.4838 19.1775 10.4603 17.5667C9.3336 15.8276 8.63244 13.8474 8.41361 11.7867C8.39695 11.6024 8.41886 11.4166 8.47795 11.2412C8.53703 11.0657 8.63199 10.9045 8.75679 10.7678C8.88159 10.6311 9.03348 10.5219 9.20281 10.4471C9.37213 10.3723 9.55517 10.3336 9.74028 10.3334H11.7403C12.0638 10.3302 12.3775 10.4448 12.6228 10.6558C12.8681 10.8667 13.0283 11.1597 13.0736 11.4801C13.158 12.1201 13.3146 12.7486 13.5403 13.3534C13.63 13.592 13.6494 13.8514 13.5962 14.1007C13.543 14.35 13.4195 14.5788 13.2403 14.7601L12.3936 15.6067C13.3427 17.2758 14.7246 18.6577 16.3936 19.6067L17.2403 18.7601C17.4215 18.5808 17.6504 18.4573 17.8997 18.4041C18.149 18.351 18.4083 18.3704 18.6469 18.4601C19.2518 18.6858 19.8802 18.8423 20.5203 18.9267C20.8441 18.9724 21.1399 19.1356 21.3513 19.3851C21.5627 19.6346 21.6751 19.9531 21.6669 20.2801Z"
							stroke="#D9E4FF"
							style="stroke:#D9E4FF;stroke:color(display-p3 0.8500 0.8953 1.0000);stroke-opacity:1;"
							stroke-width="1.33333"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</g>
					<defs>
						<clipPath id="clip0_773_2962">
							<rect
								width="16"
								height="16"
								fill="white"
								style="fill:white;fill-opacity:1;"
								transform="translate(7 9)"
							/>
						</clipPath>
					</defs>
				</svg>
			</button>
		{/if}

		<!-- Send Button -->
		<button
			class="disabled:opacity-50 hover:opacity-70 transition-all duration-200"
			on:click={sendMessage}
			disabled={isLoading || !prompt.trim()}
		>
			<svg
				width="36"
				height="36"
				viewBox="0 0 32 32"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M0 16C0 7.16344 7.16344 0 16 0C24.8366 0 32 7.16344 32 16C32 24.8366 24.8366 32 16 32C7.16344 32 0 24.8366 0 16Z"
					fill="#23F784"
					style="fill:#23F784;fill:color(display-p3 0.1373 0.9686 0.5176);fill-opacity:1;"
				/>
				<path
					d="M16 23V9"
					stroke="black"
					style="stroke:black;stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M9 16L16 9L23 16"
					stroke="black"
					style="stroke:black;stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
	</div>
</div>

<style>
	/* Hide scrollbar while keeping scroll functionality */
	textarea::-webkit-scrollbar {
		display: none;
	}

	textarea {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	/* Smooth transitions */
	textarea {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
