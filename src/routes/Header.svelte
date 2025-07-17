<script>
	// export let title;

	import { onMount } from 'svelte';

	let visible = false;

	function typewriter(node, { speed = 2 }) {
		const text = node.textContent;
		const duration = text.length / (speed * 0.01);

		return {
			duration,
			tick: (t) => {
				const i = ~~(text.length * t);
				node.textContent = text.slice(0, i);
			}
		};
	}

	onMount(() => {
		setTimeout(() => {
			visible = true;
		}, 500);
	});
</script>

<header class="sticky top-0 z-[100] lg:hidden">
	<label
		for="my-drawer"
		class="drawer-button lg:hidden absolute top-3 left-4 bg-black rounded-full px-1 pb-1"
	>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			class="inline-block h-5 w-5 stroke-current"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M4 6h16M4 12h16M4 18h16"
			/>
		</svg>
	</label>
</header>
