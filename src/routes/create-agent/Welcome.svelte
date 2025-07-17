<script>
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';
	import componentImg from '$lib/img/component-img.svg';

	// All props from parent (centralized in +page.svelte)
	export let isLoading = false;

	// Event dispatcher for parent communication
	const dispatch = createEventDispatcher();

	function handleGetStarted() {
		dispatch('next');
	}
</script>

<div
	class="bg-[#06070A] rounded-xl border border-utama flex flex-col flex-1 overflow-hidden content-start relative"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<!-- Welcome Section -->
	<div class="flex-1 flex items-center justify-between min-h-0">
		<!-- Left Side - Text Content -->
		<div class="flex-1 p-16 space-y-8 3xl:max-w-[750px] max-w-[650px]">
			<h2
				class="3xl:text-8xl text-6xl text-utama"
				in:fly|global={{
					delay: 300,
					duration: 700,
					x: -100,
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				STACK YOUR AGENT
			</h2>
			<p
				class="text-lg text-[#ECF2FF] text-justify"
				in:fly|global={{
					delay: 450,
					duration: 700,
					x: -100,
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				An AI agent is a fine-tuned package of AI capabilities, tools, and external services. Once
				deployed, it can work autonomously on a wide variety of tasks. Use our no-code wizard to
				execute your unique vision with a personalized AI agent.
			</p>
			<button
				class="btn btn-primary rounded-full text-kedua text-lg font-normal w-full hover:opacity-70 transition-all duration-200 flex items-center gap-2"
				on:click={handleGetStarted}
				disabled={isLoading}
				in:fly|global={{
					delay: 600,
					duration: 700,
					x: -100,
					opacity: 0,
					easing: quintOut
				}}
				out:fade|global={{ duration: 300 }}
			>
				<span>Get Started</span>
				<svg
					width="25"
					height="24"
					viewBox="0 0 25 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M5.5 12L19.5 12"
						stroke="black"
						style="stroke:black;stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M12.5 5L19.5 12L12.5 19"
						stroke="black"
						style="stroke:black;stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</button>
		</div>

		<!-- Right Side - Stack Visualization -->

		<img
			src={componentImg}
			alt="Component Stack Img"
			class="absolute right-0 bottom-0 3xl:w-[1100px] 3xl:h-[830px] h-[586px]"
			in:fly|global={{
				delay: 750,
				duration: 1000,
				y: 50,
				opacity: 0,
				easing: quintOut
			}}
			out:fade|global={{ duration: 300 }}
		/>
	</div>
</div>
