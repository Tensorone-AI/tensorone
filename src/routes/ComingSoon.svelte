<script>
	import { fade, fly } from 'svelte/transition';
	import bggpu1 from '$lib/img/rtx4090.webp';
	import bggpu3 from '$lib/img/a5000.webp';

	export let description =
		'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua';
</script>

<!-- Top Background -->
<img
	src={bggpu1}
	alt="Background"
	class="absolute hidden md:block
		   md:left-20 md:-top-[290px] md:w-[650px]
		   lg:left-20 lg:-top-[300px] lg:w-[700px]
		   xl:left-28 xl:-top-[430px] xl:w-[900px]
		   3xl:left-[150px] 3xl:-top-[500px] 3xl:w-[1100px]"
	in:fly={{ delay: 300, x: 200, duration: 800 }}
	out:fly={{ x: 200, duration: 300 }}
/>

<!-- Middle Text -->
<div
	class="py-14 sm:px-14 px-8 flex flex-col justify-center tablet-only:h-full tablet-only:w-full text-center md:text-left gap-6 z-50 md:absolute
		   md:left-16 md:top-[18rem] md:max-w-[500px]
		   lg:left-16 lg:top-[22rem] lg:max-w-[650px]
		   xl:left-20 xl:top-[22rem] xl:max-w-[750px]
		   3xl:left-[150px] 3xl:top-[31rem] 3xl:max-w-[800px]"
	in:fade={{ delay: 300, duration: 800 }}
	out:fade={{ duration: 300 }}
>
	<h2 class="text-utama text-5xl md:text-6xl 2xl:text-7xl 3xl:text-8xl font-satoshi z-50">
		Coming Soon
	</h2>
	<p class="text-[#D9E4FF] text-sm md:text-base 3xl:text-xl z-50">
		{description}
	</p>
</div>

<!-- Bottom Background -->
<img
	src={bggpu3}
	alt="Background"
	class="absolute hidden md:block
		   md:left-60 md:-bottom-[320px] md:w-[600px]
		   lg:left-60 lg:-bottom-[380px] lg:w-[700px]
		   xl:left-48 xl:-bottom-[600px] xl:w-[1000px]
		   3xl:-bottom-[750px] 3xl:left-[400px] 3xl:w-[1300px]"
	in:fly={{ delay: 300, x: -200, y: 200, duration: 800 }}
	out:fly={{ x: -200, y: 200, duration: 300 }}
/>
