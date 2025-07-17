<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let data = [];
	export let agent = null;

	// Generate last 7 days dynamically
	function generateLast7Days() {
		const days = [];
		const today = new Date();
		
		for (let i = 6; i >= 0; i--) {
			const date = new Date(today);
			date.setDate(today.getDate() - i);
			
			const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
							   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
			
			const month = monthNames[date.getMonth()];
			const day = date.getDate();
			
			days.push(`${month} ${day}`);
		}
		
		return days;
	}

	$: days = generateLast7Days();
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6"
	in:fly|global={{ delay: 300, duration: 150, x: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Intent Volume (Last 7 Days)</h3>
	<div class="mt-auto">
		{#if agent}
			<div class="flex items-end space-x-2 h-32">
				{#each data as volume, i}
					<div class="flex-1 bg-[#1F222D] rounded" style="height: {(volume / 100) * 100}%">
						<div class="w-full h-full bg-utama rounded"></div>
					</div>
				{/each}
			</div>
			<div class="grid grid-cols-7 gap-2 text-xs text-[#ECF2FF] mt-2">
				{#each days as day}
					<div class="text-center">{day}</div>
				{/each}
			</div>
		{:else}
			<div class="flex items-center justify-center h-32">
				<span class="text-[#98A7C8] text-sm">No data available</span>
			</div>
		{/if}
	</div>
</div>
