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
				d="M32 12C35.314 12 38 14.686 38 18V32C38 35.314 35.314 38 32 38C28.686 38 26 35.314 26 32V18C26 14.686 28.686 12 32 12Z"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M32 38V50"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M24 50H40"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M44 25C46 27 46 31 44 33"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M48 21C52 25 52 33 48 37"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M20 25C18 27 18 31 20 33"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M16 21C12 25 12 33 16 37"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
	</div>
	<h3 class="text-xl mb-2">No voice generated yet</h3>
	<p class="text-sm opacity-75">Enter text and select a voice to create your AI speech</p>
</div>
