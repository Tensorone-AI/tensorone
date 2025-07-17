<script>
	import IntentVolumeChart from './IntentVolumeChart.svelte';
	import IntentCategoriesChart from './IntentCategoriesChart.svelte';

	// Props passed from parent - data now centralized
	export let intentVolumeData = [];
	export let intentCategoriesData = [];
	export let agent = null;
</script>

<div class="grid grid-cols-2 gap-4 mb-4">
	<IntentVolumeChart data={intentVolumeData} {agent} />
	<IntentCategoriesChart data={intentCategoriesData} {agent} />
</div>
