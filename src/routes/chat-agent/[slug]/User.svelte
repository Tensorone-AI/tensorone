<script>
	export let message = '';
	export let copyState = 'default';
	export let handleCopy = () => {};

	function onCopyClick() {
		handleCopy(message);
	}
</script>

<div class="chat chat-end pb-4">
	<div
		class="bg-[#1F222D] text-[#ECF2FF] sm:text-base text-sm whitespace-pre-wrap px-4 py-2 rounded-xl rounded-br-none message flex items-end justify-between gap-6"
	>
		<span>{message}</span>
		<div class="flex items-center justify-end gap-2">
			<!-- Copy Button -->
			<button
				on:click={onCopyClick}
				title={copyState === 'success'
					? 'Copied!'
					: copyState === 'error'
						? 'Copy failed'
						: 'Copy message'}
				aria-label={copyState === 'success'
					? 'Copied!'
					: copyState === 'error'
						? 'Copy failed'
						: 'Copy message'}
				class="hover:brightness-150 transition-all"
			>
				{#if copyState === 'success'}
					<!-- Check Icon -->
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M13.5 4.5L6 12L2.5 8.5"
							stroke="#444A61"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{:else if copyState === 'error'}
					<!-- Cross Icon -->
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M12 4L4 12M4 4L12 12"
							stroke="#444A61"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				{:else}
					<!-- Default Copy Icon -->
					<svg
						width="16"
						height="16"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<g clip-path="url(#clip0_271_1398)">
							<path
								d="M13.6154 6H7.38462C6.61991 6 6 6.61991 6 7.38462V13.6154C6 14.3801 6.61991 15 7.38462 15H13.6154C14.3801 15 15 14.3801 15 13.6154V7.38462C15 6.61991 14.3801 6 13.6154 6Z"
								stroke="#444A61"
								style="stroke:#444A61;stroke:color(display-p3 0.2670 0.2910 0.3792);stroke-opacity:1;"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
							<path
								d="M3.07692 10H2.38462C2.01739 10 1.66521 9.85412 1.40554 9.59446C1.14588 9.33479 1 8.98261 1 8.61538V2.38462C1 2.01739 1.14588 1.66521 1.40554 1.40554C1.66521 1.14588 2.01739 1 2.38462 1H8.61538C8.98261 1 9.33479 1.14588 9.59446 1.40554C9.85412 1.66521 10 2.01739 10 2.38462V3.07692"
								stroke="#444A61"
								style="stroke:#444A61;stroke:color(display-p3 0.2670 0.2910 0.3792);stroke-opacity:1;"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</g>
						<defs>
							<clipPath id="clip0_271_1398">
								<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
							</clipPath>
						</defs>
					</svg>
				{/if}
			</button>
		</div>
	</div>
</div>

<style>
	.message {
		max-width: 80%;
		word-wrap: break-word;
		overflow-wrap: break-word;
	}

	button {
		transition: opacity 0.2s ease-in-out;
	}
</style>
