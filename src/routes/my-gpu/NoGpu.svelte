<script>
	import { fade, fly } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import bggpu1 from '$lib/img/rtx4090.webp';
	import bggpu3 from '$lib/img/a5000.webp';

	function handleGetGPU() {
		goto('/');
	}
</script>

<!-- Top Background -->
<img
	src={bggpu1}
	alt="Background"
	class="absolute hidden md:block
		   md:left-20 md:-top-[290px] md:w-[650px]
		   lg:left-20 lg:-top-[350px] lg:w-[700px]
		   xl:left-28 xl:-top-[450px] xl:w-[800px]
		   3xl:left-[150px] 3xl:-top-[600px] 3xl:w-[1100px]"
	in:fly|global={{ delay: 300, x: 200, duration: 800 }}
	out:fly|global={{ x: 200, duration: 300 }}
/>

<!-- Middle Text -->
<div
	class="py-8 sm:px-8 px-8 flex flex-col justify-center items-center md:items-start tablet-only:h-full tablet-only:w-full text-center md:text-left gap-6 z-50 md:absolute
		   md:left-16 md:top-[16rem] md:max-w-[650px]
		   lg:left-16 lg:top-[16rem] lg:max-w-[650px]
		   xl:left-20 xl:top-[12rem] xl:max-w-[750px]
		   3xl:left-[150px] 3xl:top-[23rem] 3xl:max-w-[1000px]"
	in:fade|global={{ delay: 300, duration: 800 }}
	out:fade|global={{ duration: 300 }}
>
	<h2 class="text-utama text-5xl md:text-6xl 2xl:text-7xl 3xl:text-8xl font-satoshi z-50">
		No GPU Purchased
	</h2>
	<p class="text-[#D9E4FF] text-sm md:text-base 3xl:text-xl z-50">
		Rent GPU for your AI and computing projects. If you already purchased a GPU, please wait for a
		day maximum before your GPU becomes available
	</p>
	<button
		class="btn btn-sm md:btn-md btn-primary rounded-full w-fit hover:opacity-70 transition-all duration-200"
		on:click={handleGetGPU}
	>
		<span class="text-lg md:text-xl font-normal">Get a GPU</span>
		<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M5 12H19"
				stroke="black"
				style="stroke:black;stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M12 5L19 12L12 19"
				stroke="black"
				style="stroke:black;stroke-opacity:1;"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
	</button>
</div>

<!-- Bottom Background -->
<img
	src={bggpu3}
	alt="Background"
	class="absolute hidden md:block
		   md:left-60 md:-bottom-[320px] md:w-[600px]
		   lg:left-40 lg:-bottom-[430px] lg:w-[700px]
		   xl:left-40 xl:-bottom-[630px] xl:w-[1000px]
		   3xl:-bottom-[800px] 3xl:left-[300px] 3xl:w-[1300px]"
	in:fly|global={{ delay: 300, x: -200, y: 200, duration: 800 }}
	out:fly|global={{ x: -200, y: 200, duration: 300 }}
/>
