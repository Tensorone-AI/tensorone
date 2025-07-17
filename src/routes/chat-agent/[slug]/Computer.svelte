<script>
	export let chatTitle = 'AI Agent';
	export let message = '';
</script>

<div class="chat chat-start pb-4">
	<div
		class="bg-[#0C0D12] sm:text-base text-sm whitespace-pre-wrap text-[#ECF2FF] flex flex-col justify-center items-start px-4 py-2 rounded-xl"
	>
		<div class="chat-header text-[#98A7C8]">{chatTitle}:</div>
		<span>{message}</span>
	</div>
</div>
