<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let date;
</script>

<div
	class="text-center border-t border-[#444A61] pt-3 mx-52"
	in:fly|global={{
		delay: 100,
		duration: 800,
		y: 50,
		opacity: 0,
		easing: quintOut
	}}
	out:fade|global={{ duration: 200 }}
>
	<p class="text-[#BBD0FF] font-bold text-xs">{date}</p>
</div>
