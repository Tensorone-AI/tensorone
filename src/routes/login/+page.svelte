<script>
	import logo from '$lib/img/logo.webp';
	import loader from '$lib/video/loader.webm';
	import loginbg from '$lib/img/loginbg.webp';
	import { fade } from 'svelte/transition';

	import { openModal, getWalletAddress } from '$lib/auth/reown';
	import { wallet } from '$lib/stores/wallet';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	function handleConnect() {
		openModal();
	}

	onMount(() => {
		const address = getWalletAddress();
		if (address) {
			wallet.setAddress(address);
			goto('/');
		} else {
			wallet.setLoading(false);
		}
	});
</script>

<svelte:head>
	<title>Login</title>
	<meta
		name="description"
		content="Sign in to your account to access our blockchain-based AI services, manage your $TPO tokens, and rent high-performance cloud GPUs for your projects."
	/>
</svelte:head>

<!-- login form -->
<div class="h-screen w-screen shadow-sm relative flex justify-center items-center bg-black">
	<img src={logo} alt="Logo" class="max-w-52 3xl:max-w-60 absolute top-8 left-10 z-30" />
	<div class="h-screen lg:w-1/2 hidden lg:block overflow-hidden absolute top-0 left-0">
		<img
			src={loginbg}
			alt="Background"
			class="absolute top-0 left-0 w-full h-full object-cover opacity-70 -scale-x-100"
		/>
		<!-- Dark corner shadows overlay -->
		<div class="absolute inset-0 bg-gradient-to-br from-black/40 via-transparent to-black/40"></div>
		<div class="absolute inset-0 bg-gradient-to-bl from-black/40 via-transparent to-black/40"></div>
		<div class="absolute inset-0 bg-gradient-to-tr from-black/40 via-transparent to-black/40"></div>
		<div class="absolute inset-0 bg-gradient-to-tl from-black/40 via-transparent to-black/40"></div>
	</div>
	<div class="flex flex-col justify-center items-center h-screen w-full relative z-30">
		<div
			class="bg-[#00000080] backdrop-blur-md border border-[#444A61] rounded-tr-[32px] rounded-bl-[32px] rounded-tl-[140px] rounded-br-[140px] px-36 py-6 space-y-8 3xl:space-y-10"
		>
			<div>
				<figure class="flex flex-col items-center text-center" transition:fade={{ duration: 300 }}>
					<video loop autoplay muted src={loader} alt="gpu" class="max-w-40 3xl:max-w-56" />
				</figure>
				<h2 class="text-4xl 3xl:text-6xl text-utama text-center font-satoshi font-light mb-4">
					BUILD AN INSTANT AI AGENT
				</h2>
				<h5 class="flex items-center justify-center gap-3 text-[#ECF2FF]">
					<span class="text-sm 3xl:text-2xl font-satoshi"
						>You are one click away from the complete AI suite</span
					>
					<svg
						width="auto"
						height="auto"
						viewBox="0 0 16 16"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						class="w-3 h-3 3xl:w-4 3xl:h-4"
					>
						<g clip-path="url(#clip0_442_4661)">
							<path
								d="M8 1V15"
								stroke="#ECF2FF"
								style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
							<path
								d="M15 8L8 15L1 8"
								stroke="#ECF2FF"
								style="stroke:#ECF2FF;stroke:color(display-p3 0.9250 0.9475 1.0000);stroke-opacity:1;"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</g>
						<defs>
							<clipPath id="clip0_442_4661">
								<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
							</clipPath>
						</defs>
					</svg>
				</h5>
			</div>
			<div class="flex flex-col items-center text-center">
				<button
					class="btn btn-sm 3xl:btn-md btn-primary flex items-center gap-3 rounded-full px-5 3xl:px-20 mb-4 hover:opacity-70 transition-all duration-200"
					on:click={handleConnect}
					><span class="text-sm 3xl:text-lg text-[#0C0D12] font-normal">Connect Wallet</span>
					<svg
						width="auto"
						height="auto"
						viewBox="0 0 7 14"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						class="w-3 h-3 3xl:w-4 3xl:h-4"
					>
						<path
							d="M0.5 13L6.5 7L0.5 1"
							stroke="black"
							style="stroke:black;stroke-opacity:1;"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>
				<p class="text-[#D9E4FF] text-[0.6rem] 3xl:text-sm" transition:fade={{ duration: 300 }}>
					By signing up, I agree with Tensor One's
					<br />
					<a href="/" class="text-utama underline hover:brightness-75">Terms and Condition</a> &
					<a href="/" class="text-utama underline hover:brightness-75">Privacy Policy.</a>
				</p>
			</div>
		</div>
	</div>
	<div class="fixed inset-0 overflow-hidden">
		<!-- Green light source in bottom right corner -->
		<div
			class="absolute bottom-0 right-0 w-[800px] h-[800px] translate-x-[400px] translate-y-[400px]"
		>
			<!-- Core bright green light -->
			<div class="absolute inset-0 bg-kedua rounded-full blur-[100px]"></div>
			<!-- Secondary glow layer -->
			<div class="absolute inset-0 bg-kedua rounded-full blur-[150px] scale-125"></div>
			<!-- Outer diffuse glow -->
			<div class="absolute inset-0 bg-kedua rounded-full blur-[200px] scale-150"></div>
		</div>
	</div>
</div>

<!-- /login form -->
