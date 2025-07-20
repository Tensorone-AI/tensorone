<script>
	import logoBlack from '$lib/img/sidebar-logo.webp';
	import ActiveAside from './ActiveAside.svelte';
	import { page } from '$app/stores';

	let currentPath;
	$: currentPath = $page.url.pathname;
</script>

<aside class="drawer-side z-[110] messages-scrollbar">
	<label for="my-drawer" class="drawer-overlay" />
	<!-- sidebar menu -->
	<nav
		class="flex min-h-full bg-[#06070A] 3xl:w-60 w-44 flex-col gap-5 px-2 pt-7 pb-3 border-r border-[#444A61]"
	>
		<div class="mx-3 flex items-center gap-2">
			<a href="https://tensorone.ai/"><img src={logoBlack} alt="logo" class="w-full" /></a>
		</div>
		<ul class="menu flex flex-col gap-4 text-[#ECF2FF] text-xs px-0 font-satoshi font-bold">
			<li>
				<details
					open={currentPath === '/uncensored-chat' ||
						currentPath === '/text-to-image' ||
						currentPath === '/text-to-speech' ||
						currentPath === '/website-generator' ||
						currentPath === '/app-builder' ||
						currentPath === '/text-to-video'}
				>
					<summary
						class={currentPath === '/uncensored-chat' ||
						currentPath === '/text-to-image' ||
						currentPath === '/text-to-speech' ||
						currentPath === '/website-generator' ||
						currentPath === '/app-builder' ||
						currentPath === '/text-to-video'
							? 'active-tab relative'
							: ''}
					>
						{#if currentPath === '/uncensored-chat' || currentPath === '/text-to-image' || currentPath === '/text-to-speech' || currentPath === '/website-generator' || currentPath === '/app-builder' || currentPath === '/text-to-video'}
							<ActiveAside />
						{/if}
						<svg
							width="16"
							height="16"
							viewBox="0 0 25 25"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M1 3.5C1 2.11929 2.11929 1 3.5 1H7.97059C9.3513 1 10.4706 2.11929 10.4706 3.5V3.91177C10.4706 5.29248 9.3513 6.41177 7.97059 6.41177H3.5C2.11929 6.41177 1 5.29248 1 3.91177V3.5Z"
								fill={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M1 12.9706C1 11.5899 2.11929 10.4706 3.5 10.4706H7.97059C9.3513 10.4706 10.4706 11.5899 10.4706 12.9706V21.5C10.4706 22.8807 9.3513 24 7.97059 24H3.5C2.11929 24 1 22.8807 1 21.5V12.9706Z"
								fill={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M14.5294 3.5C14.5294 2.11929 15.6487 1 17.0294 1H21.5C22.8807 1 24 2.11929 24 3.5V12.0294C24 13.4101 22.8807 14.5294 21.5 14.5294H17.0294C15.6487 14.5294 14.5294 13.4101 14.5294 12.0294V3.5Z"
								fill={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M14.5294 21.0883C14.5294 19.7075 15.6487 18.5883 17.0294 18.5883H21.5C22.8807 18.5883 24 19.7075 24 21.0883V21.5C24 22.8807 22.8807 24 21.5 24H17.0294C15.6487 24 14.5294 22.8807 14.5294 21.5V21.0883Z"
								fill={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M1 3.5C1 2.11929 2.11929 1 3.5 1H7.97059C9.3513 1 10.4706 2.11929 10.4706 3.5V3.91177C10.4706 5.29248 9.3513 6.41177 7.97059 6.41177H3.5C2.11929 6.41177 1 5.29248 1 3.91177V3.5Z"
								stroke={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M1 12.9706C1 11.5899 2.11929 10.4706 3.5 10.4706H7.97059C9.3513 10.4706 10.4706 11.5899 10.4706 12.9706V21.5C10.4706 22.8807 9.3513 24 7.97059 24H3.5C2.11929 24 1 22.8807 1 21.5V12.9706Z"
								stroke={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M14.5294 3.5C14.5294 2.11929 15.6487 1 17.0294 1H21.5C22.8807 1 24 2.11929 24 3.5V12.0294C24 13.4101 22.8807 14.5294 21.5 14.5294H17.0294C15.6487 14.5294 14.5294 13.4101 14.5294 12.0294V3.5Z"
								stroke={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M14.5294 21.0883C14.5294 19.7075 15.6487 18.5883 17.0294 18.5883H21.5C22.8807 18.5883 24 19.7075 24 21.0883V21.5C24 22.8807 22.8807 24 21.5 24H17.0294C15.6487 24 14.5294 22.8807 14.5294 21.5V21.0883Z"
								stroke={currentPath === '/uncensored-chat' ||
								currentPath === '/text-to-image' ||
								currentPath === '/text-to-speech' ||
								currentPath === '/website-generator' ||
								currentPath === '/app-builder' ||
								currentPath === '/text-to-video'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
						</svg>
						Playground
					</summary>
					<ul class="text-[#D9E4FF] font-normal">
						<li>
							<a
								class={currentPath === '/uncensored-chat' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/uncensored-chat">Uncensored AI Chat</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/text-to-image' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/text-to-image">Text to Image</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/text-to-speech' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/text-to-speech">Text to Speech</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/text-to-video' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/text-to-video">Text to Video</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/website-generator' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/website-generator">Website Generator</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/app-builder' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/app-builder">App Builder</a
							>
						</li>
					</ul>
				</details>
			</li>
			<li>
				<details
					open={currentPath === '/agent-templates' ||
						currentPath === '/create-agent' ||
						currentPath === '/my-agents' ||
						currentPath === '/monitor-agents'}
				>
					<summary
						class={currentPath === '/agent-templates' ||
						currentPath === '/create-agent' ||
						currentPath === '/my-agents' ||
						currentPath === '/monitor-agents'
							? 'active-tab relative'
							: ''}
					>
						{#if currentPath === '/agent-templates' || currentPath === '/create-agent' || currentPath === '/my-agents' || currentPath === '/monitor-agents'}
							<ActiveAside />
						{/if}
						<svg
							width="16"
							height="16"
							viewBox="0 0 25 25"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M1 3.5C1 2.11929 2.11929 1 3.5 1H7.97059C9.3513 1 10.4706 2.11929 10.4706 3.5V3.91177C10.4706 5.29248 9.3513 6.41177 7.97059 6.41177H3.5C2.11929 6.41177 1 5.29248 1 3.91177V3.5Z"
								fill={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M1 12.9706C1 11.5899 2.11929 10.4706 3.5 10.4706H7.97059C9.3513 10.4706 10.4706 11.5899 10.4706 12.9706V21.5C10.4706 22.8807 9.3513 24 7.97059 24H3.5C2.11929 24 1 22.8807 1 21.5V12.9706Z"
								fill={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M14.5294 3.5C14.5294 2.11929 15.6487 1 17.0294 1H21.5C22.8807 1 24 2.11929 24 3.5V12.0294C24 13.4101 22.8807 14.5294 21.5 14.5294H17.0294C15.6487 14.5294 14.5294 13.4101 14.5294 12.0294V3.5Z"
								fill={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M14.5294 21.0883C14.5294 19.7075 15.6487 18.5883 17.0294 18.5883H21.5C22.8807 18.5883 24 19.7075 24 21.0883V21.5C24 22.8807 22.8807 24 21.5 24H17.0294C15.6487 24 14.5294 22.8807 14.5294 21.5V21.0883Z"
								fill={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
							/>
							<path
								d="M1 3.5C1 2.11929 2.11929 1 3.5 1H7.97059C9.3513 1 10.4706 2.11929 10.4706 3.5V3.91177C10.4706 5.29248 9.3513 6.41177 7.97059 6.41177H3.5C2.11929 6.41177 1 5.29248 1 3.91177V3.5Z"
								stroke={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M1 12.9706C1 11.5899 2.11929 10.4706 3.5 10.4706H7.97059C9.3513 10.4706 10.4706 11.5899 10.4706 12.9706V21.5C10.4706 22.8807 9.3513 24 7.97059 24H3.5C2.11929 24 1 22.8807 1 21.5V12.9706Z"
								stroke={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M14.5294 3.5C14.5294 2.11929 15.6487 1 17.0294 1H21.5C22.8807 1 24 2.11929 24 3.5V12.0294C24 13.4101 22.8807 14.5294 21.5 14.5294H17.0294C15.6487 14.5294 14.5294 13.4101 14.5294 12.0294V3.5Z"
								stroke={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
							<path
								d="M14.5294 21.0883C14.5294 19.7075 15.6487 18.5883 17.0294 18.5883H21.5C22.8807 18.5883 24 19.7075 24 21.0883V21.5C24 22.8807 22.8807 24 21.5 24H17.0294C15.6487 24 14.5294 22.8807 14.5294 21.5V21.0883Z"
								stroke={currentPath === '/agent-templates' ||
								currentPath === '/create-agent' ||
								currentPath === '/my-agents' ||
								currentPath === '/monitor-agents'
									? '#23F784'
									: '#BBD0FF'}
								stroke-width="1.5"
							/>
						</svg>
						AI Agents
					</summary>
					<ul class="text-[#D9E4FF] font-normal">
						<li>
							<a
								class={currentPath === '/agent-templates' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/agent-templates">Browse Templates</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/create-agent' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/create-agent">Create New Agent</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/my-agents' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/my-agents">My Agents</a
							>
						</li>
						<li>
							<a
								class={currentPath === '/monitor-agents' ? 'active-tab' : 'hover:text-[#23f784]'}
								href="/monitor-agents">Monitor Agents</a
							>
						</li>
					</ul>
				</details>
			</li>
			<li>
				<a class={currentPath === '/' ? 'active-tab relative' : 'hover:text-[#23f784]'} href="/">
					{#if currentPath === '/'}
						<ActiveAside />
					{/if}
					<svg width="16" height="16" viewBox="0 0 31 30" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M27.0382 5.03219C26.2707 4.19745 25.1337 3.73963 23.9966 3.90302C19.9091 4.49025 17.0515 7.38112 15.5448 11.1003C15.5299 11.1003 15.515 11.0954 15.5001 11.0954C15.3957 11.0954 15.2979 11.1181 15.1934 11.1261C14.9929 6.83595 15.8946 3.64257 18.4091 0.780819C18.5781 0.58831 18.4803 0.277707 18.2234 0.234029C15.1189 -0.304672 11.9994 0.101376 9.22466 1.30011C8.17378 1.75469 7.37651 2.6687 7.18423 3.77522C6.49304 7.75482 8.4307 11.3057 11.5966 13.8536C11.5601 13.9604 11.522 14.0655 11.4938 14.1756C7.25385 13.0351 4.42444 11.2135 2.41385 7.99586C2.27793 7.77908 1.94477 7.77423 1.82377 7.99909C0.34193 10.712 -0.228262 13.7339 0.0816966 16.6798C0.199382 17.796 0.844163 18.8184 1.86189 19.3377C5.52504 21.2078 9.58269 20.5073 13.042 18.359C13.1364 18.4269 13.2293 18.4916 13.3287 18.5515C10.9071 22.1347 8.25666 24.1973 4.50068 25.0709C4.24874 25.1291 4.141 25.4381 4.32001 25.6193C6.50796 27.8356 9.27604 29.2964 12.243 29.9192C13.3668 30.1554 14.5619 29.8723 15.3841 29.0877C18.3378 26.2664 18.908 22.2868 17.8853 18.4124C17.9814 18.346 18.0659 18.2684 18.1555 18.194C20.902 21.5507 22.0938 24.6487 21.7838 28.4083C21.7639 28.6606 22.0291 28.8564 22.2628 28.7448C25.0972 27.3988 27.378 25.2812 28.9013 22.7204C29.4781 21.7497 29.5726 20.5526 29.062 19.548C27.2238 15.9308 23.5176 14.1707 19.4202 13.9264C19.3853 13.8197 19.3605 13.7064 19.3174 13.6029C23.4297 12.0968 26.8144 11.948 30.3781 13.3958C30.6185 13.4929 30.8903 13.3068 30.8538 13.0545C30.4179 10.0067 29.0587 7.23715 27.0332 5.03057L27.0382 5.03219ZM15.4984 17.1473C14.3564 17.1473 13.4315 16.2446 13.4315 15.13C13.4315 14.0154 14.3564 13.1127 15.4984 13.1127C16.6405 13.1127 17.5654 14.0154 17.5654 15.13C17.5654 16.2446 16.6405 17.1473 15.4984 17.1473Z"
							fill={currentPath === '/' ? '#23F784' : '#BBD0FF'}
						/>
					</svg>
					Rent GPU
				</a>
			</li>
			<li>
				<a
					class={currentPath === '/my-gpu' ? 'active-tab relative' : 'hover:text-[#23f784]'}
					href="/my-gpu"
				>
					{#if currentPath === '/my-gpu'}
						<ActiveAside />
					{/if}
					<svg width="16" height="16" viewBox="0 0 28 30" xmlns="http://www.w3.org/2000/svg">
						<path
							fill-rule="evenodd"
							clip-rule="evenodd"
							d="M6.89837 0.709718C11.5884 -0.236573 16.4116 -0.236573 21.1016 0.709718C24.0391 1.3024 26.4031 3.55165 27.2141 6.52551L27.2831 6.77862C28.239 10.2838 28.239 13.9933 27.2831 17.4984L27.2141 17.7515C26.4031 20.7254 24.0391 22.9747 21.1016 23.5673C19.1283 23.9655 17.1314 24.1961 15.1308 24.2592V27.3126H17.7694C18.394 27.3126 18.9003 27.8352 18.9003 28.4798C18.9003 29.1245 18.394 29.647 17.7694 29.647H10.2306C9.60602 29.647 9.09973 29.1245 9.09973 28.4798C9.09973 27.8352 9.60602 27.3126 10.2306 27.3126H12.8692V24.2592C10.8686 24.1961 8.87168 23.9655 6.89837 23.5673C3.96089 22.9747 1.59691 20.7254 0.785925 17.7515L0.716905 17.4984C-0.238968 13.9933 -0.238968 10.2838 0.716904 6.77861L0.785925 6.52551C1.59691 3.55165 3.96089 1.3024 6.89837 0.709718ZM17.8874 7.69131C18.4032 7.62051 18.9191 7.81889 19.2673 8.18062L19.2651 8.17992C20.1841 9.1361 20.8007 10.3362 20.9985 11.6569C21.015 11.7663 20.8917 11.8469 20.7827 11.8049C19.1658 11.1774 17.6302 11.2419 15.7644 11.8946C15.7769 11.9233 15.786 11.9538 15.7951 11.9841C15.8002 12.0011 15.8053 12.0181 15.811 12.0348C17.67 12.1406 19.3516 12.9033 20.1856 14.4708C20.4172 14.9061 20.3743 15.4249 20.1126 15.8455C19.4215 16.9552 18.3867 17.8728 17.1007 18.4561C16.9947 18.5044 16.8744 18.4196 16.8834 18.3102C17.024 16.6811 16.4833 15.3387 15.2372 13.8841C15.2266 13.8925 15.2162 13.901 15.2058 13.9094C15.1762 13.9335 15.1469 13.9574 15.1146 13.9787C15.5786 15.6576 15.3199 17.3821 13.9798 18.6047C13.6068 18.9447 13.0646 19.0673 12.5547 18.965C11.2086 18.6951 9.95269 18.0621 8.96001 17.1017C8.87879 17.0232 8.92767 16.8893 9.04198 16.8641C10.7461 16.4855 11.9486 15.5917 13.0473 14.039C13.0022 14.013 12.9601 13.985 12.9172 13.9556C11.3477 14.8865 9.50673 15.19 7.84475 14.3797C7.383 14.1546 7.09046 13.7116 7.03707 13.2279C6.89644 11.9514 7.15513 10.6419 7.82745 9.46627C7.88235 9.36883 8.03351 9.37094 8.09517 9.46487C9.00738 10.8592 10.2911 11.6485 12.2148 12.1427C12.2255 12.1027 12.2394 12.0642 12.2534 12.0254C12.2561 12.018 12.2588 12.0107 12.2614 12.0032C10.825 10.8991 9.94592 9.36042 10.2595 7.63593C10.3467 7.15644 10.7085 6.76036 11.1853 6.56338C12.4442 6.04393 13.8595 5.86798 15.268 6.10141C15.3846 6.12034 15.429 6.25493 15.3523 6.33836C14.2114 7.57845 13.8023 8.96224 13.8933 10.8213C13.9121 10.8199 13.9304 10.8176 13.9486 10.8152C13.9763 10.8116 14.0038 10.808 14.0324 10.808C14.0358 10.808 14.0392 10.8085 14.0426 10.8091C14.046 10.8096 14.0494 10.8101 14.0528 10.8101C14.7363 9.19849 16.0328 7.94578 17.8874 7.69131ZM13.0939 12.5563C13.0939 13.0393 13.5135 13.4305 14.0317 13.4305C14.5498 13.4305 14.9695 13.0393 14.9695 12.5563C14.9695 12.0733 14.5498 11.6822 14.0317 11.6822C13.5135 11.6822 13.0939 12.0733 13.0939 12.5563Z"
							fill={currentPath === '/my-gpu' ? '#23F784' : '#BBD0FF'}
						/>
					</svg>
					My GPU
				</a>
			</li>
			<li>
				<a
					class={currentPath === '/managed-training'
						? 'active-tab relative'
						: 'hover:text-[#23f784]'}
					href="/managed-training"
				>
					{#if currentPath === '/managed-training'}
						<ActiveAside />
					{/if}
					<svg width="16" height="16" viewBox="0 0 23 32" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M14.1231 13.6317C14.0126 13.6317 13.9231 13.5421 13.9231 13.4317V1.60383C13.9231 1.41125 13.6776 1.32993 13.5626 1.48444L1.59411 17.5699C1.34868 17.8997 1.58411 18.3683 1.99525 18.3683H8.87694C8.98739 18.3683 9.07694 18.4579 9.07694 18.5683V30.3962C9.07694 30.5888 9.32243 30.6701 9.43739 30.5156L21.4059 14.4301C21.6513 14.1003 21.4159 13.6317 21.0047 13.6317H14.1231Z"
							fill={currentPath === '/managed-training' ? '#23F784' : '#BBD0FF'}
							stroke={currentPath === '/managed-training' ? '#23F784' : '#BBD0FF'}
							stroke-width="1.5"
						/>
					</svg>
					Managed Training
				</a>
			</li>
		</ul>
	</nav>
	<!-- /sidebar menu -->
</aside>

<style>
	.active-tab {
		color: #23f784;
		background-color: transparent;
		font-weight: 700;
	}

	.active-tab:hover {
		color: #23f784;
		background-color: transparent;
	}

	/* Custom scrollbar styles for messages container */
	.messages-scrollbar {
		/* Firefox */
		scrollbar-width: thin;
		scrollbar-color: #444a61 transparent;
	}

	/* Webkit browsers (Chrome, Safari, Edge) */
	.messages-scrollbar::-webkit-scrollbar {
		width: 6px;
	}

	.messages-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}

	.messages-scrollbar::-webkit-scrollbar-thumb {
		background-color: #444a61;
		border-radius: 3px;
	}

	.messages-scrollbar::-webkit-scrollbar-thumb:hover {
		background-color: #5a6175;
	}
</style>
