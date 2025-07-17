<script>
	import { fly, fade } from 'svelte/transition';

	// Props from parent - all data management handled in parent
	export let recentDeposits;
</script>

<!-- Recent Deposits Section -->
<div>
	<h3 class="text-[#ECF2FF] text-3xl font-medium mb-6">Recent Deposit</h3>

	<div class="space-y-4">
		{#each recentDeposits as deposit, index (deposit.id)}
			<div
				class="bg-[#0C0D12] rounded-2xl px-4 py-3 flex items-center justify-between"
				in:fly|global={{ x: -100, duration: 500, delay: 300 + index * 150 }}
				out:fade|global={{ duration: 300 }}
			>
				<span class="text-[#ECF2FF] text-sm break-all">
					{deposit.txHash}
				</span>
				<div
					class="text-utama bg-kedua rounded-full px-6 py-3 flex items-center gap-3 flex-shrink-0"
				>
					Deposited Amount
					<span class="border border-utama rounded-full px-4 py-1">
						${deposit.amount}
					</span>
				</div>
			</div>
		{:else}
			<div
				class="text-center text-[#BBD0FF] py-8"
				in:fly|global={{ x: -100, duration: 500, delay: 300 }}
				out:fade|global={{ duration: 300 }}
			>
				No recent deposits found
			</div>
		{/each}
	</div>
</div>
