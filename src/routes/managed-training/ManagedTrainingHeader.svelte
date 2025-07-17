<script>
	import { fade } from 'svelte/transition';
</script>

<div
	class="text-center space-y-2 mb-8 border-b border-[#444A61] pb-8"
	in:fade={{ delay: 300, duration: 500 }}
	out:fade={{ duration: 300 }}
>
	<div>
		<h2
			class="text-xl sm:text-2xl md:text-3xl xl:text-5xl 3xl:text-6xl text-center text-[#ECF2FF] px-4 font-satoshi"
		>
			Let Us Train Your Models to Perfection
		</h2>
	</div>
	<p class="text-base 3xl:text-xl text-[#BBD0FF] font-medium">
		Accelerate your journey towards powerful AI tools with our Managed Training Solutions.
	</p>
	<p class="text-utama text-base 3xl:text-xl font-medium">
		50% discount for students and academic research!
	</p>
</div>
