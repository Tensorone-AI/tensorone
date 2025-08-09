<script>
	// Logic moved to parent, this is now purely presentational
	export let onCreateClick;
</script>

<button
	class="card card-compact bg-black border-2 border-[#1F222D] hover:border-primary hover:bg-black transition-all duration-200 w-full relative overflow-hidden group h-64 flex flex-col"
	on:click={onCreateClick}
>
	<div
		class="card-body flex flex-row justify-center items-center space-x-2 relative z-10 flex-1 m-3 bg-[#0C0D12] rounded-md"
	>
		<div class="font-light text-primary text-3xl">+</div>
		<h2 class="text-2xl text-[#ECF2FF] font-normal group-hover:text-primary transition-colors">
			Create Agent
		</h2>
	</div>
</button>
