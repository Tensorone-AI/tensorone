import { createAppKit } from '@reown/appkit';
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi';
import { mainnet } from '@reown/appkit/networks';
import { wallet } from '$lib/stores/wallet';
import { supabase } from '$lib/db/supabaseClient';
import { browser } from '$app/environment';

const projectId = import.meta.env.PUBLIC_REOWN_PROJECT_ID || 'default_project_id';
let appKit = undefined;
const networks = [mainnet];

let isDisconnecting = false;
let unsubscribeState = null;

if (browser) {
	const wagmiAdapter = new WagmiAdapter({
		networks,
		projectId
	});

	appKit = createAppKit({
		adapters: [wagmiAdapter],
		networks: [mainnet],
		projectId,
		metadata: {
			name: 'TensorOne DApp',
			description: 'AI infrastructure services with blockchain technology',
			url: 'https://dapp.tensorone.ai',
			icons: ['https://tensorone.ai/logo.webp']
		},
		features: {
			email: false,
			socials: false,
			emailShowWallets: true
		}
	});

	// Subscribe to state changes
	unsubscribeState = appKit.subscribeState((state) => {
		if (isDisconnecting) return;

		const account = appKit.getAccount();
		if (account?.address && account.isConnected) {
			wallet.setAddress(account.address);
			handleSupabaseUser(account.address);
		} else {
			wallet.disconnect();
		}
	});

	// Initialize wallet state
	initializeWalletState();
}

export { appKit };

export function openModal() {
	if (!appKit || isDisconnecting) return;
	if (!appKit.getWalletInfo()) appKit.open({ view: 'Connect' });
	else initializeWalletState();
}

export function closeModal() {
	if (!appKit) return;
	appKit.close();
}

async function initializeWalletState() {
	if (!appKit) return;

	try {
		const account = appKit.getAccount();

		// Check if AppKit has an active connection
		if (account?.address && account.isConnected) {
			wallet.setAddress(account.address);
			await handleSupabaseUser(account.address);
		} else {
			// If AppKit doesn't have a connection, clear everything
			wallet.disconnect();

			// Also clear any stale localStorage data
			if (typeof window !== 'undefined') {
				localStorage.removeItem('tensorone_wallet_address');
			}
		}
	} catch (error) {
		console.error('Failed to initialize wallet state:', error);
		wallet.disconnect();
	}
}

export async function disconnectWallet() {
	if (!appKit) return false;
	try {
		isDisconnecting = true;

		// Use AppKit's built-in disconnect method
		try {
			await appKit.adapter?.connectionControllerClient?.disconnect();
			await AppKit.disconnect();
		} catch (error) {
			console.warn('Adapter disconnect failed:', error);
		}

		// Clear wallet store first (this will clear localStorage)
		wallet.disconnect();

		// Clear any additional AppKit related storage
		if (typeof window !== 'undefined') {
			// Clear WalletConnect and AppKit related storage
			const keysToRemove = [];
			for (let i = 0; i < localStorage.length; i++) {
				const key = localStorage.key(i);
				if (
					key &&
					(key.startsWith('wc@2:') ||
						key.startsWith('@appkit') ||
						key.startsWith('reown:') ||
						key.startsWith('wagmi.') ||
						key.startsWith('tensorone_wallet_address') ||
						key.includes('connector'))
				) {
					keysToRemove.push(key);
				}
			}
			keysToRemove.forEach((key) => {
				try {
					localStorage.removeItem(key);
				} catch (e) {
					console.warn('Failed to remove storage key:', key, e);
				}
			});
		}

		// Force a small delay to ensure state is updated
		await new Promise((resolve) => setTimeout(resolve, 100));

		isDisconnecting = false;
		return true;
	} catch (error) {
		console.error('Failed to disconnect wallet:', error);
		isDisconnecting = false;
		return false;
	}
}

export function getWalletAddress() {
	if (!appKit || isDisconnecting) return null;
	try {
		const account = appKit.getAccount();
		return account?.address || null;
	} catch (error) {
		console.error('Error getting wallet address:', error);
		return null;
	}
}

export function cleanup() {
	if (unsubscribeState) {
		unsubscribeState();
		unsubscribeState = null;
	}
}

async function handleSupabaseUser(address) {
	try {
		// Check if user exists
		const { data, error } = await supabase
			.from('user')
			.select('address')
			.eq('address', address)
			.single();

		if (error && error.code !== 'PGRST116') {
			console.error('Error fetching address:', error);
			return;
		}

		// If user doesn't exist, create new record
		if (!data) {
			const { error: insertError } = await supabase.from('user').insert([{ address }]);

			if (insertError) {
				console.error('Error inserting address:', insertError);
			}
		}
	} catch (error) {
		console.error('Error handling Supabase user:', error);
	}
}
