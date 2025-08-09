<script>
	// ================================
	// IMPORTS & EXPORTS
	// ================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import ControlsPanel from './ControlsPanel.svelte';
	import ImageResult from './ImageResult.svelte';
	import ZoomImageModal from './ZoomImageModal.svelte';
	import ErrorMessage from './ErrorMessage.svelte';
	import { fade } from 'svelte/transition';
	import { wallet } from '$lib/stores/wallet';

	// Props
	export let data = {};

	// ================================
	// CONFIGURATION DATA
	// ================================
	const modelOptions = [
		{
			label: 'Realistic',
			modelName: 'hyper realistic, photorealistic, 4K resolution, intricate details'
		},
		{
			label: 'Photography',
			modelName: 'professional DSLR photo, shallow depth of field, high dynamic range'
		},
		{
			label: 'Anime',
			modelName: 'vibrant anime style, sharp line art, dynamic shading, bold colors'
		},
		{
			label: 'Cartoon',
			modelName: 'bright cartoon style, bold outlines, simple shading, playful vibe'
		},
		{
			label: 'Low Poly',
			modelName: 'low poly aesthetic, geometric shapes, minimalistic, flat shading'
		},
		{
			label: 'Cyberpunk',
			modelName: 'cyberpunk scene, neon lights, futuristic cityscape, rainy atmosphere'
		},
		{
			label: 'Voxel Art',
			modelName: 'voxel art style, isometric perspective, pixelated 3D blocks'
		},
		{
			label: 'Fantasy',
			modelName: 'epic fantasy illustration, magical environment, detailed textures'
		},
		{
			label: 'Vector Illustration',
			modelName: 'flat vector illustration, clean lines, bold colors, scalable'
		}
	];

	const aspectRatios = [
		{ name: 'Mobile Vertical', width: '320', height: '1024', group: 0 },
		{ name: 'Square', width: '1024', height: '1024', group: 0 },
		{ name: 'Landscape', width: '1024', height: '576', group: 0 },
		{ name: 'Widescreen', width: '1024', height: '512', group: 1 },
		{ name: 'Portrait', width: '576', height: '1024', group: 1 },
		{ name: 'Random', width: 'random', height: 'random', group: 1 }
	];

	// ================================
	// STATE VARIABLES
	// ================================
	let prompt = '';
	let activeRatio = '';
	let selectedModel = '';
	let imageUrl = '';
	let isLoading = false;
	let isPromptRecLoading = false;
	let isZoomed = false;
	let error = null;

	// ================================
	// CATEGORY 1: REACTIVITY ONLY
	// ================================
	$: address = data?.address || $wallet?.address || '';
	$: activeDimensions = getActiveDimensions(activeRatio);
	$: isFormValid = prompt.trim() !== '' && activeRatio !== '' && selectedModel !== '';
	$: canGenerate = isFormValid && !isLoading && !isPromptRecLoading;

	function getActiveDimensions(ratioName) {
		const found = aspectRatios.find((r) => r.name === ratioName);
		return found ? { width: found.width, height: found.height } : { width: '1024', height: '1024' };
	}

	function handlePromptInput(event) {
		prompt = event.target.value;
	}

	function handleModelChange(event) {
		selectedModel = event.target.value;
	}

	function handleRatioSelect(ratioName) {
		activeRatio = ratioName;
	}

	function handleKeydown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			generateImage();
		}
	}

	function toggleZoom() {
		isZoomed = !isZoomed;
	}

	function downloadImage() {
		if (!imageUrl) {
			console.error('No image available to download');
			return;
		}

		const link = document.createElement('a');
		link.href = imageUrl;
		link.download = `tensor_ai_${Date.now()}.png`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	// Error handling
	function clearError() {
		error = null;
	}

	// ================================
	// MAIN FUNCTIONS (COMBINES CATEGORIES)
	// ================================
	async function generateImage() {
		if (!canGenerate) return;

		// Validate input
		if (!prompt.trim()) {
			error = 'Please enter a prompt to generate an image';
			return;
		}

		if (prompt.trim().length < 3) {
			error = 'Prompt must be at least 3 characters long';
			return;
		}

		if (!selectedModel) {
			error = 'Please select a model';
			return;
		}

		if (!activeRatio) {
			error = 'Please select an aspect ratio';
			return;
		}

		imageUrl = '';
		isLoading = true;
		error = null;

		try {
			const response = await fetch('/api/playground/image', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					prompt: prompt.trim(),
					model: selectedModel,
					width: activeDimensions.width,
					height: activeDimensions.height
				})
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const blob = await response.blob();
			imageUrl = URL.createObjectURL(blob);
		} catch (err) {
			error = err.message || 'An error occurred while generating the image';
			console.error('Image generation error:', err);
			imageUrl = '';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Text to Image</title>
	<meta
		name="description"
		content="Generate AI images from text prompts using various artistic styles and aspect ratios."
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-8 flex flex-col">
	<PageTitle subtitle="Playground" title="Text to Image" {address} />

	<!-- Error Message Component -->
	{#if error}
		<ErrorMessage {error} onClear={clearError} />
	{/if}

	<div class="flex flex-1 gap-8 min-h-0">
		<!-- Controls Panel -->
		<ControlsPanel
			bind:prompt
			{selectedModel}
			{activeRatio}
			{modelOptions}
			{aspectRatios}
			{isLoading}
			{canGenerate}
			onPromptInput={handlePromptInput}
			onModelChange={handleModelChange}
			onRatioSelect={handleRatioSelect}
			onKeydown={handleKeydown}
			onGenerate={generateImage}
		/>

		<!-- Result Section -->
		<div
			class="xl:w-3/5 min-h-0"
			in:fade|global={{ delay: 550, duration: 500 }}
			out:fade|global={{ duration: 300 }}
		>
			<ImageResult
				{imageUrl}
				{isLoading}
				onToggleZoom={toggleZoom}
				onDownloadImage={downloadImage}
			/>
		</div>
	</div>
</section>

<!-- Zoom Modal -->
<ZoomImageModal isOpen={isZoomed} imageSrc={imageUrl} on:close={() => (isZoomed = false)} />
