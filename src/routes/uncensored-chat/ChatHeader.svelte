<script>
	import { fade } from 'svelte/transition';
	import ShareChat from './ShareChat.svelte';

	export let chatTitle;
	export let onNewChat;
	export let onToggleShareModal;
</script>

<div
	class="flex justify-between items-center mb-4 bg-[#0C0D12] border-b border-[#444A61] px-8 py-3 rounded-tl-xl min-h-[74px]"
	in:fade|global={{ delay: 600, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<div class="text-[#ECF2FF] text-2xl font-satoshi font-medium max-w-[880px] truncate py-2">
		{chatTitle}
	</div>
	<div class="flex items-center justify-center lg:gap-3 gap-1">
		<button
			class="btn btn-sm bg-transparent border-transparent hover:bg-transparent hover:border-transparent hover:opacity-70 group"
			on:click={onNewChat}
		>
			<svg
				width="16"
				height="16"
				viewBox="0 0 16 16"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<g clip-path="url(#clip0_151_4258)">
					<path
						d="M8 14H15"
						stroke="#98A7C8"
						style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M11.2504 1.41112C11.5524 1.10906 11.9621 0.939362 12.3893 0.939362C12.6008 0.939362 12.8103 0.981023 13.0057 1.06197C13.2011 1.14291 13.3787 1.26156 13.5282 1.41112C13.6778 1.56069 13.7964 1.73825 13.8774 1.93367C13.9583 2.12909 14 2.33853 14 2.55005C14 2.76157 13.9583 2.97102 13.8774 3.16644C13.7964 3.36186 13.6778 3.53942 13.5282 3.68898L4 13L1 14L2 11L11.2504 1.41112Z"
						stroke="#98A7C8"
						style="stroke:#98A7C8;stroke:color(display-p3 0.5978 0.6539 0.7834);stroke-opacity:1;"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</g>
				<defs>
					<clipPath id="clip0_151_4258">
						<rect width="16" height="16" fill="white" style="fill:white;fill-opacity:1;" />
					</clipPath>
				</defs>
			</svg>
		</button>
		<ShareChat {onToggleShareModal} />
	</div>
</div>
