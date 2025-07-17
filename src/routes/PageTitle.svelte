<script>
	import { goto } from '$app/navigation';
	import { disconnectWallet } from '$lib/auth/reown';
	import { fade } from 'svelte/transition';

	// Props
	export let subtitle = '';
	export let title = '';
	export let address = '';
	export let showBackButton = false;
	export let onBack = null;
	export let backTo = null;

	$: modifiedAddress = address ? `${address.slice(0, 10)}...${address.slice(-4)}` : '';

	function handleClick(event) {
		if (address) {
			navigator.clipboard.writeText(address);
		}
	}

	async function handleLogout() {
		const success = await disconnectWallet();
		if (success) {
			goto('/login');
		}
	}

	function handleBack() {
		if (onBack) {
			onBack();
		} else if (backTo) {
			goto(backTo);
		}
	}
</script>

<div
	class="mb-8 md:mb-12"
	in:fade|global={{ delay: 300, duration: 500 }}
	out:fade|global={{ duration: 300 }}
>
	<div class="flex justify-between items-center">
		<div class="flex items-center gap-8">
			{#if showBackButton}
				<button
					class="w-10 h-10 rounded-full flex justify-center items-center transition-all text-[#D9E4FF] hover:text-[#23f784] bg-[#1F222D] hover:bg-[#2A2F3E]"
					on:click={handleBack}
				>
					<svg
						width="26"
						height="26"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M19 12H5"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M12 19L5 12L12 5"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</button>
			{/if}
			<div>
				<h2 class="text-utama text-lg font-tasa font-medium uppercase">{subtitle}</h2>
				<h3 class="text-[#ECF2FF] text-4xl font-medium">{title}</h3>
			</div>
		</div>
		<div class="flex items-center justify-end gap-6">
			<div class="flex gap-2 justify-center">
				<a
					href="https://t.me/tpoone"
					target="_blank"
					class="w-8 h-8 rounded-lg flex justify-center items-center transition-all text-[#D9E4FF] hover:text-[#23f784] bg-[#1F222D]"
					><svg
						role="img"
						width="18"
						class="fill-current"
						viewBox="0 0 34 29"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M0.539233 12.9591C6.15975 10.4052 22.5278 3.01394 30.535 0.137957C31.7431 -0.293807 33.069 0.320907 33.5036 1.52106C33.6362 1.88697 33.6731 2.27482 33.6141 2.65536L30.0267 25.8682C29.8131 27.2586 28.5092 28.2172 27.1023 28.005C26.7413 27.9538 26.4025 27.8221 26.0931 27.6245L15.7139 20.9578C14.4837 20.1674 14.1375 18.5428 14.9257 17.3207C15.0436 17.1377 15.1909 16.9621 15.3603 16.8157L24.9292 7.7048C25.3344 7.31694 24.8113 6.68028 24.3473 7.00227L10.7122 16.4791C9.43041 17.3719 7.78772 17.5549 6.33655 16.9767L0.576064 14.6496C0.104618 14.4593 -0.123739 13.9251 0.0677865 13.4568C0.156183 13.2299 0.325609 13.0543 0.539233 12.9591Z"
						/>
					</svg>
				</a>
				<a
					href="https://x.com/tensor_one"
					target="_blank"
					class="w-8 h-8 rounded-lg flex justify-center items-center transition-all text-[#D9E4FF] hover:text-[#23f784] bg-[#1F222D]"
					><svg
						width="18"
						class="fill-current"
						viewBox="0 0 24 24"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"
						/>
					</svg>
				</a>
			</div>
			{#if address}
				<label
					class="input input-sm tooltip w-full py-1 px-3 bg-[#1F222D] flex items-center justify-between rounded-xl"
					data-tip="Copy Address"
				>
					<svg
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
							stroke="#23F784"
							style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
							stroke="#23F784"
							style="stroke:#23F784;stroke:color(display-p3 0.1373 0.9686 0.5176);stroke-opacity:1;"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
					<input
						type="text"
						value={modifiedAddress}
						class=" w-full bg-[#1F222D] text-center text-[#ECF2FF] text-xs font-medium"
						readonly
						on:click={handleClick}
					/>
				</label>
				<div class="tooltip" data-tip="Log Out">
					<button
						class="btn btn-ghost btn-sm bg-[#1F222D] p-2 hover:opacity-80 hover:text-opacity-100 transition-all rounded-lg"
						on:click={handleLogout}
					>
						<svg
							width="16"
							height="16"
							viewBox="0 0 27 27"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M25.976 13.8893C25.9711 13.9037 25.9711 13.9183 25.9648 13.9321C25.9648 13.934 25.9648 13.9362 25.964 13.9376C25.9182 14.0529 25.8479 14.1506 25.7696 14.239C25.7605 14.2487 25.7573 14.2615 25.7481 14.2711L21.732 18.4329C21.3392 18.8385 20.7044 18.8391 20.3117 18.4323C19.9202 18.0258 19.9202 17.3665 20.3117 16.9597L22.614 14.5754H12.9892C12.4336 14.5754 11.9841 14.1093 11.9841 13.5344C11.9841 12.9595 12.4337 12.4934 12.9892 12.4934H22.6454L20.3158 10.0323C19.9271 9.62253 19.9333 8.96287 20.33 8.56022C20.5242 8.36192 20.7798 8.26241 21.033 8.26241C21.2861 8.26241 21.5518 8.36617 21.7503 8.57441L25.7556 12.8049C25.842 12.8948 25.8999 13 25.9498 13.1108C25.962 13.1433 25.9712 13.1754 25.9822 13.2089C26.0087 13.2939 26.0248 13.3797 26.0311 13.4691C26.033 13.5051 26.0373 13.5392 26.0351 13.5754C26.0311 13.6816 26.0117 13.7863 25.976 13.889V13.8893Z"
								fill="#23F784"
							/>
							<path
								d="M13.052 2.08205C10.1272 2.08205 7.37547 3.26427 5.30217 5.41337C1.00097 9.87193 1.00097 17.1283 5.30217 21.5879C7.37547 23.7354 10.1263 24.9181 13.052 24.9181C15.977 24.9181 18.7287 23.7352 20.7999 21.5879L22.2995 23.0324C19.8325 25.5906 16.5486 26.9995 13.052 27C9.55669 27 6.27066 25.5911 3.80276 23.0322C-1.26759 17.7762 -1.26759 9.22432 3.80276 3.96757C6.27066 1.40891 9.55562 -1.90735e-06 13.052 -1.90735e-06C16.5486 -1.90735e-06 19.8325 1.40891 22.2995 3.96757L20.7999 5.4132C18.7287 3.26516 15.9768 2.08187 13.052 2.08187V2.08205Z"
								fill="#23F784"
							/>
						</svg>
					</button>
				</div>
			{/if}
		</div>
	</div>
</div>
