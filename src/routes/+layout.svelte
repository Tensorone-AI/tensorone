<script>
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { wallet } from '$lib/stores/wallet';
	import { cleanup } from '$lib/auth/reown';
	import { browser } from '$app/environment';
	import '../app.css';
	import Background from './Background.svelte';
	import Aside from './Aside.svelte';
	import { get } from 'svelte/store';

	let unsubscribe;

	onMount(() => {
		if (browser) {
			unsubscribe = wallet.subscribe(({ address, isLoading }) => {
				if (isLoading) return; // Don't navigate while loading

				const path = get(page).url.pathname;

				if (!address && path !== '/login') {
					goto('/login');
				} else if (address && path === '/login') {
					goto('/');
				} else if (address && path !== '/login') {
					goto(path);
				}
			});
		}
	});

	onDestroy(() => {
		unsubscribe?.();
		cleanup();
	});
</script>

{#if $wallet.isLoading}
	<div class="h-screen flex items-center justify-center">
		<span class="text-lg">Loading...</span>
	</div>
{:else if $page.url.pathname === '/login'}
	<div class="min-h-screen font-dm-sans flex justify-center items-center">
		<main>
			<slot />
		</main>
	</div>
{:else}
	<div class="drawer min-h-screen lg:drawer-open font-dm-sans">
		<input id="my-drawer" type="checkbox" class="drawer-toggle" />
		<main class="drawer-content">
			<Background />
			<slot />
		</main>
		<Aside />
	</div>
{/if}
