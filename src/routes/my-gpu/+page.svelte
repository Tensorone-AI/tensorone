<script>
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import MyGpu from './MyGpu.svelte';
	import NoGpu from './NoGpu.svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { wallet } from '$lib/stores/wallet';
	import { supabase } from '$lib/db/supabaseClient';
	import { onMount } from 'svelte';

	// Props
	export let data = {};
	$: address = data?.address || $wallet?.address || '';

	// State for GPU data
	let ownGpu = [];
	let loading = true;
	let rawGpuData = [];

	// Function to format time_expire into countdown format
	function formatTimeCountdown(timeExpire) {
		const now = new Date();
		const expireDate = new Date(timeExpire);
		const diff = expireDate - now;

		if (diff <= 0) return '0d:0h';

		const days = Math.floor(diff / (1000 * 60 * 60 * 24));
		const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

		return `${days}d:${hours}h`;
	}

	// Function to fetch GPU data from Supabase
	async function fetchGpuData() {
		if (!address) return;

		try {
			loading = true;
			const { data: gpuData, error } = await supabase
				.from('gpu')
				.select('address, gpu, time_expire')
				.eq('address', address);

			if (error) {
				console.error('Error fetching GPU data:', error);
				return;
			}

			console.log('Fetched GPU data:', gpuData);
			console.log('Address:', address);

			rawGpuData = gpuData;

			updateGpuData();
		} catch (error) {
			console.error('Error fetching GPU data:', error);
		} finally {
			loading = false;
		}
	}

	// Function to update GPU data display
	function updateGpuData() {
		ownGpu = rawGpuData.map((gpu) => ({
			id: gpu.id,
			name: gpu.gpu,
			url: `https://tensorone.vultr.com/gpu-${gpu.id}`,
			time: formatTimeCountdown(gpu.time_expire)
		}));
	}

	// Fetch GPU data when component mounts or address changes
	onMount(() => {
		fetchGpuData();

		// Update countdown every minute
		const interval = setInterval(() => {
			if (rawGpuData.length > 0) {
				updateGpuData();
			}
		}, 60000); // Update every minute

		return () => clearInterval(interval);
	});

	$: if (address) fetchGpuData();

	const gpuSpecsLookup = {
		'NVIDIA A4000': { computeUnits: 48 },
		'NVIDIA RTX 4090': { computeUnits: 64 },
		'NVIDIA A5000': { computeUnits: 64 },
		'NVIDIA A6000': { computeUnits: 84 },
		'NVIDIA TESLA A100': { computeUnits: 108 },
		'NVIDIA TESLA H100': { computeUnits: 144 }
	};

	$: totalComputeUnits = ownGpu.reduce((total, gpu) => {
		const specs = gpuSpecsLookup[gpu.name];
		return total + (specs?.computeUnits || 0);
	}, 0);
</script>

<svelte:head>
	<title>My GPU</title>
	<meta
		name="description"
		content="View and manage your rented GPUs with Tensorone. Access high-performance cloud GPUs, monitor usage, and optimize your AI and computing projects."
	/>
</svelte:head>
<Header />

{#if loading}
	<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
		<PageTitle subtitle="My GPU" title="My Active GPUs" {address} />

		<div
			class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-x-hidden overflow-y-hidden relative tablet-only:h-full tablet-only:w-full"
			in:fade|global={{ delay: 300, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<div class="flex justify-center items-center h-full">
				<div class="loading loading-spinner loading-lg text-utama"></div>
			</div>
		</div>
	</section>
{:else if ownGpu.length === 0}
	<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
		<PageTitle subtitle="My GPU" title="My Active GPUs" {address} />

		<div
			class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-x-hidden overflow-y-hidden relative tablet-only:h-full tablet-only:w-full"
			in:fade|global={{ delay: 300, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<NoGpu />
		</div>
	</section>
{:else}
	<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
		<PageTitle subtitle="My GPU" title="My Active GPUs" {address} />

		<div
			class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start space-y-6"
			in:fade|global={{ delay: 300, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			{#each ownGpu as gpu, index}
				<div
					class="card card-compact bg-black border border-[#1F222D] rounded-2xl w-full"
					in:fly|global={{
						delay: 300,
						duration: 1500 * (index + 1),
						y: -100 * (index + 1),
						opacity: 0,
						easing: quintOut
					}}
					out:fade|global={{ duration: 300 }}
				>
					<MyGpu {gpu} />
				</div>
			{/each}
			<div
				class="text-right text-lg text-[#ECF2FF]"
				in:fade|global={{ delay: 300, duration: 3000 }}
			>
				Total Compute Units: {totalComputeUnits}
			</div>
		</div>
	</section>
{/if}
