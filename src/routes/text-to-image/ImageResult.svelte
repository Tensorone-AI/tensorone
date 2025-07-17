<script>
	import { fly } from 'svelte/transition';
	import ZoomImageButton from './ZoomImageButton.svelte';
	import DownloadImageButton from './DownloadImageButton.svelte';

	export let imageUrl;
	export let isLoading;
	export let onToggleZoom;
	export let onDownloadImage;
</script>

<div
	class="rounded-3xl h-full flex items-center justify-center relative overflow-hidden transition-all duration-300 p-4 {isLoading
		? 'bg-kedua border border-utama animate-pulse'
		: 'bg-black border border-[#444A61]'}"
>
	{#if imageUrl}
		<div class="relative w-full h-full flex items-center justify-center" key={imageUrl}>
			<img
				src={imageUrl}
				alt="Generated"
				class="max-w-full max-h-full object-contain rounded-2xl"
				in:fly={{ delay: 100, duration: 400, y: 20 }}
				loading="lazy"
			/>

			<div class="absolute bottom-2 right-2 flex gap-4">
				<ZoomImageButton onClick={onToggleZoom} />
				<DownloadImageButton onClick={onDownloadImage} />
			</div>
		</div>
	{:else if isLoading}
		<div class="flex flex-col items-center justify-center text-utama" in:fly={{ duration: 200 }}>
			<div class="loading loading-spinner w-12 h-12 mb-4 text-utama"></div>
			<p class="text-lg font-medium">Generating your image...</p>
			<p class="text-sm opacity-75">This may take a few moments</p>
		</div>
	{:else}
		<div class="text-center text-[#98A7C8]" in:fly={{ duration: 200 }}>
			<div class="mb-4 opacity-50">
				<svg
					width="64"
					height="64"
					viewBox="0 0 64 64"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
					class="mx-auto"
				>
					<path
						d="M16 48L20.586 43.414C21.367 42.633 22.633 42.633 23.414 43.414L32 52L40.586 43.414C41.367 42.633 42.633 42.633 43.414 43.414L48 48M8 56H56C57.105 56 58 55.105 58 54V18C58 16.895 57.105 16 56 16H8C6.895 16 6 16.895 6 18V54C6 55.105 6.895 56 8 56ZM42 30C42 33.314 39.314 36 36 36C32.686 36 30 33.314 30 30C30 26.686 32.686 24 36 24C39.314 24 42 26.686 42 30Z"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</div>
			<h3 class="text-xl mb-2">No image generated yet</h3>
			<p class="text-sm opacity-75">Enter a prompt and click generate to create your AI image</p>
		</div>
	{/if}
</div>
