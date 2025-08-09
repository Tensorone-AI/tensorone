<script>
	import { fade, scale } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let isOpen = false;
	export let imageSrc;

	function closeModal() {
		dispatch('close');
	}

	function handleKeydown(event) {
		if (event.key === 'Escape') {
			closeModal();
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
	<div
		class="fixed inset-0 z-[200] flex items-center justify-center p-4 sm:p-6 md:p-8"
		transition:fade={{ duration: 100 }}
	>
		<button
			class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
			on:click={closeModal}
			transition:fade={{ duration: 100 }}
		>
			<div
				class="w-full h-full backdrop-blur-sm transition-all duration-300 ease-in-out"
				style="backdrop-filter: blur(4px);"
			></div>
		</button>
		<div
			class="relative z-10 bg-transparent sm:h-full max-w-[90vw] max-h-[90vh] flex items-center justify-center"
			transition:scale={{ duration: 100, easing: cubicOut, start: 0.95 }}
		>
			<img src={imageSrc} alt="Zoomed" class="max-w-full max-h-full object-contain rounded-3xl" />
		</div>
		<button class="fixed top-6 right-6 z-20 btn btn-ghost btn-circle" on:click={closeModal}>
			<svg
				width="20"
				height="20"
				viewBox="0 0 12 12"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M7.40994 6L11.7099 1.71C11.8982 1.5217 12.004 1.2663 12.004 1C12.004 0.733701 11.8982 0.478306 11.7099 0.290002C11.5216 0.101699 11.2662 -0.00408936 10.9999 -0.00408936C10.7336 -0.00408936 10.4782 0.101699 10.2899 0.290002L5.99994 4.59L1.70994 0.290002C1.52164 0.101699 1.26624 -0.00408936 0.999939 -0.00408936C0.733637 -0.00408935 0.478243 0.101699 0.289939 0.290002C0.101635 0.478306 -0.00415277 0.733701 -0.00415277 1C-0.00415278 1.2663 0.101635 1.5217 0.289939 1.71L4.58994 6L0.289939 10.29C0.196211 10.383 0.121816 10.4936 0.0710478 10.6154C0.0202791 10.7373 -0.00585938 10.868 -0.00585938 11C-0.00585938 11.132 0.0202791 11.2627 0.0710478 11.3846C0.121816 11.5064 0.196211 11.617 0.289939 11.71C0.382902 11.8037 0.493503 11.8781 0.615362 11.9289C0.737221 11.9797 0.867927 12.0058 0.999939 12.0058C1.13195 12.0058 1.26266 11.9797 1.38452 11.9289C1.50638 11.8781 1.61698 11.8037 1.70994 11.71L5.99994 7.41L10.2899 11.71C10.3829 11.8037 10.4935 11.8781 10.6154 11.9289C10.7372 11.9797 10.8679 12.0058 10.9999 12.0058C11.132 12.0058 11.2627 11.9797 11.3845 11.9289C11.5064 11.8781 11.617 11.8037 11.7099 11.71C11.8037 11.617 11.8781 11.5064 11.9288 11.3846C11.9796 11.2627 12.0057 11.132 12.0057 11C12.0057 10.868 11.9796 10.7373 11.9288 10.6154C11.8781 10.4936 11.8037 10.383 11.7099 10.29L7.40994 6Z"
					fill="white"
				/>
			</svg>
		</button>
	</div>
{/if}
