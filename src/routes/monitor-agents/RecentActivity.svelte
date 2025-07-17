<script>
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let data = [];
	export let agent = null;
</script>

<div
	class="card card-compact bg-[#0C0D12] w-full relative overflow-hidden p-6 flex-1"
	in:fly|global={{ delay: 450, duration: 150, y: -50, opacity: 0, easing: quintOut }}
>
	<h3 class="text-[#ECF2FF] mb-4">Recent Activity</h3>
	<div class="space-y-4">
		{#if agent}
			{#each data as activity}
				<div class="border-l-2 border-utama pl-4">
					<div class="flex justify-between items-start mb-1">
						<span class="font-medium text-sm text-[#ECF2FF]">{activity.type}</span>
						<span class="text-xs text-[#98A7C8] font-inter">{activity.time}</span>
					</div>
					<p class="text-xs text-[#98A7C8] font-inter">{activity.description}</p>
				</div>
			{/each}
		{:else}
			<div class="flex items-center justify-center h-44">
				<span class="text-[#98A7C8] text-sm">No activity available</span>
			</div>
		{/if}
	</div>
</div>
