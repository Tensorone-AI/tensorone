import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const WALLET_STORAGE_KEY = 'tensorone_wallet_address';

function createWalletStore() {
	// Initialize with loading state - don't restore from localStorage initially
	const initialState = {
		address: null,
		isConnected: false,
		isLoading: true
	};

	const { subscribe, set, update } = writable(initialState);

	return {
		subscribe,
		set,
		update,
		setAddress: (address) => {
			const newState = { 
				address,
				isConnected: !!address,
				isLoading: false
			};
			set(newState);
			
			// Persist to localStorage
			if (browser) {
				if (address) {
					localStorage.setItem(WALLET_STORAGE_KEY, address);
				} else {
					localStorage.removeItem(WALLET_STORAGE_KEY);
				}
			}
		},
		disconnect: () => {
			const newState = { 
				address: null,
				isConnected: false,
				isLoading: false
			};
			set(newState);
			
			// Clear from localStorage
			if (browser) {
				localStorage.removeItem(WALLET_STORAGE_KEY);
			}
		},
		setLoading: (isLoading) => {
			update(state => ({ ...state, isLoading }));
		}
	};
}

export const wallet = createWalletStore();
