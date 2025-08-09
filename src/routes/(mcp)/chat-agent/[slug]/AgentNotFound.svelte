<script>
	import { fade } from 'svelte/transition';

	export let handleGoBack = () => {};
</script>

<div
	class="min-h-screen w-full flex items-center justify-center"
	in:fade={{ duration: 500 }}
	out:fade={{ duration: 300 }}
>
	<div class="text-center">
		<h1 class="text-4xl text-[#ECF2FF] mb-4">Agent Not Found</h1>
		<p class="text-[#98A7C8] mb-6">
			The agent you're looking for doesn't exist or has been removed.
		</p>
		<button class="btn btn-primary" on:click={handleGoBack}> Back to Agent List </button>
	</div>
</div>
