<script>
	import { writable } from 'svelte/store';

	export let gpu;

	const months = ['1 month', '2 months', '6 months', '12 months'];

	let selectedMonth = writable('1 month');

	// Available GPU specifications database
	const availableGpuSpecs = {
		'NVIDIA A4000': {
			price: 1095,
			gpu: '1',
			gpuRam: '16',
			vCpus: '8',
			ram: '32',
			storage: '256',
			bandwidth: '1',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 48
		},
		'NVIDIA RTX 4090': {
			price: 1096,
			gpu: '1/2',
			gpuRam: '12',
			vCpus: '8',
			ram: '32',
			storage: '512',
			bandwidth: '1',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 64
		},
		'NVIDIA A5000': {
			price: 2737,
			gpu: '1',
			gpuRam: '24',
			vCpus: '16',
			ram: '64',
			storage: '1600',
			bandwidth: '2',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 128
		},
		'NVIDIA A6000': {
			price: 3828,
			gpu: '1',
			gpuRam: '48',
			vCpus: '32',
			ram: '128',
			storage: '3840',
			bandwidth: '10',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 300
		},
		'NVIDIA TESLA A100': {
			price: 4927,
			gpu: '1',
			gpuRam: '40',
			vCpus: '64',
			ram: '256',
			storage: '3840',
			bandwidth: '5',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 410
		},
		'NVIDIA TESLA H100': {
			price: 8760,
			gpu: '1',
			gpuRam: '80',
			vCpus: '96',
			ram: '512',
			storage: '7680',
			bandwidth: '10',
			os: 'Ubuntu 22.04 LTS',
			computeUnits: 600
		}
	};

	$: gpuSpecs = availableGpuSpecs[gpu.name] || {
		price: 0,
		gpu: '1',
		gpuRam: '16',
		vCpus: '8',
		ram: '32',
		storage: '256',
		bandwidth: '10',
		os: 'Ubuntu 22.04 LTS',
		computeUnits: 48
	};

	$: priceNow = '$' + gpuSpecs.price * $selectedMonth.split(' ')[0];
</script>

<!-- Card Content -->

<div class="w-full mb-4">
	<!-- Card Header -->
	<div
		class="flex flex-row items-center justify-between gap-3 bg-[#1F222D] border-b border-[#444A61] rounded-t-2xl px-8 py-4"
	>
		<div class="min-w-[280px]">
			<p class="xl:text-3xl text-2xl text-left text-[#ECF2FF] font-medium">
				{gpu.name}
			</p>
			<p class="text-xl text-[#BBD0FF]">{gpu.time}</p>
		</div>
		<div class="flex items-center justify-end gap-4">
			<div>
				<p
					class="bg-[#06070A] border border-[#444A61] px-3 py-2 rounded-full text-lg text-utama text-center w-28"
				>
					{priceNow}
				</p>
			</div>
			<div class="tooltip xl:w-52 lg:w-36" data-tip="Enter your username">
				<input
					type="text"
					placeholder="Username"
					class="input placeholder:text-[#98A7C8] text-[#ECF2FF] bg-[#06070A] border border-[#444A61] w-full rounded-full transition-all duration-200
				   focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
				/>
			</div>
			<div class="tooltip xl:w-52 lg:w-36" data-tip="Enter your password">
				<input
					type="text"
					placeholder="Password"
					class="input placeholder:text-[#98A7C8] text-[#ECF2FF] bg-[#06070A] border border-[#444A61] w-full rounded-full transition-all duration-200
				   focus:border-utama focus:outline-none focus:ring-2 focus:ring-utama/20"
				/>
			</div>
			<button
				class="btn btn-secondary rounded-full text-lg text-utama font-normal border border-utama hover:border-utama hover:opacity-70 px-4"
				>Open GPU</button
			>
		</div>
	</div>
	<!-- Card Table -->
	<div class="w-full overflow-x-auto px-6 py-2">
		<table class="table w-full">
			<thead class="text-utama text-lg">
				<tr>
					<th class="font-normal w-32">GPU</th>
					<th class="font-normal w-32">vRAM</th>
					<th class="font-normal w-32">vCPUs</th>
					<th class="font-normal w-32">RAM</th>
					<th class="font-normal w-32">Storage</th>
					<th class="font-normal w-32">Bandwidth</th>
					<th class="font-normal w-32">OS</th>
					<th class="font-normal w-32">Compute Units</th>
				</tr>
			</thead>
			<tbody class="text-[#ECF2FF] text-lg">
				<tr>
					<td class="font-bold w-32">{gpuSpecs.gpu || 1}</td>
					<td class="font-bold w-32">{gpuSpecs.gpuRam} GB GDDR6X</td>
					<td class="font-bold w-32">{gpuSpecs.vCpus} Cores</td>
					<td class="font-bold w-32">{gpuSpecs.ram} GB</td>
					<td class="font-bold w-32">{gpuSpecs.storage} NVMe</td>
					<td class="font-bold w-32">{gpuSpecs.bandwidth} Gb/s</td>
					<td class="font-bold w-32">{gpuSpecs.os || 'Ubuntu 22.04 LTS'}</td>
					<td class="font-bold w-32">{gpuSpecs.computeUnits || 0}</td>
				</tr>
			</tbody>
		</table>
	</div>
</div>

<!-- Renew Section -->
<div class="px-8 pb-8">
	<div
		class="flex items-center justify-between sm:px-7 px-3 py-2 md:gap-8 gap-3 bg-[#0C0D12] rounded-xl w-full"
	>
		<h3 class="text-[#ECF2FF] md:text-xl text-lg">Renew</h3>

		{#each months as item}
			<button
				class="btn bg-transparent border border-[#0C0D12] rounded-full px-4 py-1 text-[#98A7C8] text-lg font-bold hover:bg-transparent hover:border-transparent hover:text-utama transition-colors duration-200"
				on:click={() => selectedMonth.set(item)}
				class:active-month={item === $selectedMonth}
			>
				{item}
			</button>
		{/each}

		<button
			class="btn btn-sm bg-utama hover:bg-utama border border-transparent hover:border-transparent hover:opacity-70 flex items-center justify-center rounded-full"
			><span class="text-lg text-kedua font-normal">Renew</span>
			<svg
				width="18"
				height="18"
				viewBox="0 0 24 24"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
				class="pt-1"
			>
				<path
					d="M8 5L15 12L8 19"
					stroke="#00200F"
					style="stroke:#00200F;stroke:color(display-p3 0.0000 0.1250 0.0586);stroke-opacity:1;"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		</button>
	</div>
</div>

<style>
	/* Smooth transitions */
	input {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
