<!-- components/EmptyState.svelte -->
<script>
	import { fly } from 'svelte/transition';
</script>

<div class="text-center text-[#98A7C8]" in:fly={{ duration: 200 }}>
	<div class="mb-4 opacity-50">
		<svg
			width="64"
			height="64"
			viewBox="0 0 64 64"
			fill="none"
			xmlns="http://www.w3.org/2000/svg"
			class="mx-auto"
		>
			<path
				d="M8 16H40C42.209 16 44 17.791 44 20V44C44 46.209 42.209 48 40 48H8C5.791 48 4 46.209 4 44V20C4 17.791 5.791 16 8 16Z"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M44 24L56 16V48L44 40"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<circle cx="24" cy="32" r="6" stroke="currentColor" stroke-width="2" fill="none" />
			<path d="M22 30L28 32L22 34V30Z" fill="currentColor" />
		</svg>
	</div>
	<h3 class="text-xl mb-2">No video generated yet</h3>
	<p class="text-sm opacity-75">Enter a prompt and click generate to create your AI video</p>
</div>
