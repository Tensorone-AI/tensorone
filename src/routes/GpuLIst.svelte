<script>
	import { wallet } from '$lib/stores/wallet';

	$: address = $wallet.address;

	export let name;
	export let buytype;
	export let image;
	export let secureprice;
	export let Communityprice;
	export let vram;
	export let ram;
	export let vcpus;

	let isHovered = false;

	function handleClick() {
		if (buytype === 'buy1') {
			buy1();
		} else if (buytype === 'buy2') {
			buy2();
		} else if (buytype === 'buy3') {
			buy3();
		} else if (buytype === 'buy4') {
			buy4();
		} else if (buytype === 'buy5') {
			buy5();
		} else if (buytype === 'buy6') {
			buy6();
		}
	}

	async function initiatePayment(product, description, amount) {
		try {
			const response = await fetch('/api/coinbase-initiate-payment', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					name: product,
					description: description,
					amount: amount,
					currency: 'USD',
					producttype: 'GPU',
					email: '',
					address: address
				})
			});

			if (!response.ok) throw new Error('Failed to initiate payment');

			const { hostedUrl } = await response.json();
			window.location.href = hostedUrl;
		} catch (err) {
			console.log('Failed to initiate payment. Please try again.');
		}
	}
	function buy1() {
		initiatePayment(
			'NVIDIA RTX 4090',
			'BM Threadripper PRO 5975WX/256GB/2x2TB NVMe + RTX 4090, 16384 CUDA cores, 24GB GDDR6X VRAM',
			'1368.00'
		);
	}
	function buy2() {
		initiatePayment(
			'NVIDIA A4000',
			'BM Xeon Gold 6326/128GB/1.92TB NVMe + A4000, 6144 CUDA cores, 16GB GDDR6 VRAM',
			'720.00'
		);
	}
	function buy3() {
		initiatePayment(
			'NVIDIA A5000',
			'BM EPYC 7513/192GB/2x1.6TB NVMe + A5000, 8192 CUDA cores, 24GB GDDR6 VRAM',
			'1080.00'
		);
	}
	function buy4() {
		initiatePayment(
			'NVIDIA A6000',
			'BM EPYC 7443P/256GB/2x3.84TB NVMe + A6000, 10752 CUDA cores, 48GB GDDR6 VRAM',
			'1872.00'
		);
	}
	function buy5() {
		initiatePayment(
			'NVIDIA A100',
			'BM EPYC 7713/512GB/2x3.84TB NVMe + A100, 6912 CUDA cores, 40GB HBM2e VRAM',
			'2376.00'
		);
	}
	function buy6() {
		initiatePayment(
			'NVIDIA H100',
			'BM EPYC 9654/768GB/2x7.68TB NVMe + H100, 14592 CUDA cores, 80GB HBM3 VRAM',
			'3816.00'
		);
	}
</script>

<!-- Card -->
<div
	class="card w-full rounded-2xl border border-[#444A61] relative overflow-hidden bg-black group hover:bg-kedua hover:border-utama transition-all duration-500 z-20 p-4"
>
	<!-- Card Header -->
	<div
		class="p-4 flex justify-between items-center bg-[#0C0D12] rounded-md -z-20 border border-[#0C0D12] group-hover:border-utama transition-all duration-500"
	>
		<span class="text-[#ECF2FF] xl:text-3xl text-xl text-left font-medium">{name}</span>
		<svg width="46" height="30" viewBox="0 0 46 30" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M5.26464 12.9148C5.26464 12.9148 9.33328 6.86689 17.457 6.2412V4.04702C8.45895 4.77507 0.666992 12.4531 0.666992 12.4531C0.666992 12.4531 5.08023 25.3065 17.457 26.4834V24.1511C8.37434 23 5.26464 12.9148 5.26464 12.9148ZM17.457 19.5129V21.6488C10.5925 20.4158 8.68711 13.2267 8.68711 13.2267C8.68711 13.2267 11.983 9.54815 17.457 8.9516V11.2953C17.4528 11.2953 17.4499 11.2941 17.4465 11.2941C14.5735 10.9467 12.3291 13.6507 12.3291 13.6507C12.3291 13.6507 13.5871 18.2028 17.457 19.5129ZM17.457 0V4.04702C17.7211 4.02662 17.9853 4.00931 18.2509 4.00021C28.4807 3.65285 35.1461 12.4531 35.1461 12.4531C35.1461 12.4531 27.4906 21.8316 19.515 21.8316C18.784 21.8316 18.0997 21.7633 17.457 21.6486V24.1511C18.0066 24.2215 18.5765 24.2628 19.1711 24.2628C26.593 24.2628 31.9603 20.444 37.1575 15.9243C38.0191 16.6196 41.5468 18.311 42.272 19.0515C37.3305 23.2196 25.8139 26.5796 19.2848 26.5796C18.6555 26.5796 18.0511 26.5411 17.457 26.4834V30H45.667V0H17.457ZM17.457 8.9516V6.2412C17.7184 6.22281 17.9818 6.20878 18.2509 6.20022C25.6071 5.96743 30.4333 12.5691 30.4333 12.5691C30.4333 12.5691 25.2206 19.863 19.6314 19.863C18.8271 19.863 18.1061 19.7327 17.457 19.5129V11.2953C20.3208 11.644 20.897 12.9185 22.6187 15.8101L26.448 12.5571C26.448 12.5571 23.6527 8.86362 18.9406 8.86362C18.4284 8.86344 17.9383 8.89969 17.457 8.9516Z"
				fill="#ECF2FF"
				style="fill:#ECF2FF;fill:color(display-p3 0.9250 0.9475 1.0000);fill-opacity:1;"
			/>
		</svg>
	</div>

	<!-- Image -->
	<figure class="-mt-8 group-hover:blur-md transition-all duration-500">
		<img src={image} alt="gpu" class="max-w-72 max-h-52" />
	</figure>

	<!-- Hover Text Elements -->
	<div
		class="text-xl text-[#98A7C8] space-y-3 absolute top-1/2 left-4 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-20"
	>
		<p class="bg-[#0C0D12] border border-[#1F222D] rounded-full px-4 py-1">
			<span>Community Cloud: </span>
			<span class="text-utama">${Communityprice}</span>
		</p>
		<p class="bg-[#0C0D12] border border-[#1F222D] rounded-full px-4 py-1">
			<span>Secure Cloud: </span>
			<span class="text-utama">${secureprice}</span>
		</p>
	</div>
	<div
		class="text-base text-[#ECF2FF] absolute top-1/2 right-4 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-20"
	>
		<p class="font-bold">{vram}GB <span class="text-[#98A7C8] font-normal">VRAM</span></p>
		<p class="font-bold">{ram}GB <span class="text-[#98A7C8] font-normal">RAM</span></p>
		<p class="font-bold">{vcpus} <span class="text-[#98A7C8] font-normal">Cores</span></p>
	</div>

	<!-- Buy Button -->
	<button
		class="bg-kedua border border-utama rounded-full py-2 px-5 flex items-center justify-center gap-3 w-40 group-hover:w-full group-hover:bg-utama hover:opacity-70 transition-[width,background-color,opacity] duration-500 ease-in-out active:scale-95 active:transition-transform active:duration-300"
		on:click={handleClick}
	>
		<span
			class="text-utama text-xl group-hover:text-kedua transform group-hover:translate-x-0 transition-[color,transform] duration-500"
			>Purchase</span
		>
		<svg
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			xmlns="http://www.w3.org/2000/svg"
			class="transform group-hover:translate-x-0 transition-[stroke,transform] duration-500"
		>
			<path
				d="M5 12L19 12"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="stroke-utama group-hover:stroke-kedua transition-[stroke,transform] duration-500"
			/>
			<path
				d="M12 5L19 12L12 19"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="stroke-utama group-hover:stroke-kedua transition-[stroke,transform] duration-500"
			/>
		</svg>
	</button>
</div>
