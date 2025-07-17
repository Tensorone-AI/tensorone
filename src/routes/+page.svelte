<script>
	import Header from './Header.svelte';
	import PageTitle from './PageTitle.svelte';
	import GpuLIst from './GpuLIst.svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import rtx4090 from '$lib/img/rtx4090.webp';
	import a4000 from '$lib/img/a4000.webp';
	import a5000 from '$lib/img/a5000.webp';
	import a6000 from '$lib/img/a6000.webp';
	import teslaH100 from '$lib/img/tesla-h100.webp';
	import teslaA100 from '$lib/img/tesla-a100.webp';
	import { wallet } from '$lib/stores/wallet';

	// Props
	export let data = {};

	// Reactive state - centralized for backend management
	$: address = data?.address || $wallet?.address || '';
</script>

<svelte:head>
	<title>Rent GPU</title>
	<meta
		name="description"
		content="Rent high-performance GPUs from Tensorone, a blockchain-based AI company. Leverage $TPO tokens for seamless and cost-effective cloud GPU rentals for your AI and computing projects."
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-10">
	<PageTitle subtitle="Rent GPU" title="Select Your GPU" {address} />

	<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
		<div
			in:fly={{ delay: 300, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA RTX 4090"
				buytype="buy1"
				secureprice="1.50"
				Communityprice="1.40"
				vram="12"
				ram="32"
				vcpus="8"
				image={rtx4090}
			/>
		</div>
		<div
			in:fly={{ delay: 450, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA A4000"
				buytype="buy2"
				secureprice="1.50"
				Communityprice="1.40"
				vram="16"
				ram="32"
				vcpus="8"
				image={a4000}
			/>
		</div>
		<div
			in:fly={{ delay: 600, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA A5000"
				buytype="buy3"
				secureprice="3.75"
				Communityprice="3.50"
				vram="24"
				ram="64"
				vcpus="16"
				image={a5000}
			/>
		</div>
		<div
			in:fly={{ delay: 750, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA A6000"
				buytype="buy4"
				secureprice="5.25"
				Communityprice="5.10"
				vram="48"
				ram="128"
				vcpus="32"
				image={a6000}
			/>
		</div>
		<div
			in:fly={{ delay: 900, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA TESLA A100"
				buytype="buy5"
				secureprice="6.75"
				Communityprice="6.50"
				vram="40"
				ram="256"
				vcpus="64"
				image={teslaA100}
			/>
		</div>
		<div
			in:fly={{ delay: 1050, duration: 150, x: -50, opacity: 0, easing: quintOut }}
			out:fly={{ duration: 300, x: -50, opacity: 0, easing: quintOut }}
		>
			<GpuLIst
				name="NVIDIA TESLA H100"
				buytype="buy6"
				secureprice="12.00"
				Communityprice="11.60"
				vram="80"
				ram="512"
				vcpus="96"
				image={teslaH100}
			/>
		</div>
	</div>
</section>
