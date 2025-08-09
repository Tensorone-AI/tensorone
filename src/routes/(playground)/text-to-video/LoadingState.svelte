<!-- components/LoadingState.svelte -->
<script>
	import { fly } from 'svelte/transition';
</script>

<div class="flex flex-col items-center justify-center text-utama" in:fly={{ duration: 200 }}>
	<div class="loading loading-spinner w-12 h-12 mb-4 text-utama"></div>
	<p class="text-lg font-medium">Generating your video...</p>
	<p class="text-sm opacity-75">Queueing your request, This may take a few minutes</p>
</div>
