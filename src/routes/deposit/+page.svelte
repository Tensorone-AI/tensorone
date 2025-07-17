<script>
	// ================================
	// IMPORTS & EXPORTS
	// ================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import DepositForm from './DepositForm.svelte';
	import RecentDeposits from './RecentDeposits.svelte';
	import { fade } from 'svelte/transition';
	import { wallet } from '$lib/stores/wallet';
	import { createEventDispatcher } from 'svelte';

	// Props
	export let data = {};

	// Event dispatcher for backend communication
	const dispatch = createEventDispatcher();

	// ================================
	// 1. FETCHING FROM DATABASE
	// ================================

	// Mock data for recent deposits (will be replaced by backend data)
	const mockDeposits = [
		{
			id: '1',
			txHash: '0x833d2265adcf7e73235122f82fa3c9e55e52f2c237a54736ac6afe5b2ac14164',
			amount: 3,
			timestamp: new Date().toISOString()
		},
		{
			id: '2',
			txHash: '0xac6afe523837365122f82fa643d2265adcf72c237a5b252fc1414ae733c9e55e',
			amount: 5,
			timestamp: new Date().toISOString()
		},
		{
			id: '3',
			txHash: '0x55e52f2c237a54736ac6afe5b2ac1416833d2265adcf7e73235122f82fa3c9e4',
			amount: 20,
			timestamp: new Date().toISOString()
		}
	];

	// TODO: Database fetch functions to be implemented
	async function fetchUserDeposits(userAddress) {
		// Fetch user's deposit history from database
		// const response = await fetch(`/api/deposits/${userAddress}`);
		// return await response.json();
		return mockDeposits;
	}

	async function fetchPlaygroundCredits(userAddress) {
		// Fetch user's current playground credits from database
		// const response = await fetch(`/api/credits/${userAddress}`);
		// return await response.json();
		return 3;
	}

	async function fetchDepositStats(userAddress) {
		// Fetch user's deposit statistics (total deposits, last deposit, etc.)
		// const response = await fetch(`/api/deposit-stats/${userAddress}`);
		// return await response.json();
		return {
			totalDeposits: 0,
			lastDepositDate: null,
			totalAmount: 0
		};
	}

	async function validateTransaction(txHash) {
		// Validate transaction hash on blockchain
		// const response = await fetch(`/api/validate-transaction/${txHash}`);
		// return await response.json();
		return { isValid: true, confirmed: true };
	}

	// ================================
	// 2. REACTIVITY ONLY
	// ================================

	// Form state variables
	let depositAmount = '';
	let isSubmitting = false;

	// Reactive assignments from props/store
	$: address = data?.address || $wallet?.address || '';
	$: deposits = data?.deposits || [];
	$: playgroundCredits = data?.playgroundCredits || 3;

	// Computed reactive values
	$: recentDeposits = deposits.length > 0 ? deposits : mockDeposits;
	$: isFormValid = depositAmount && parseFloat(depositAmount) > 0;
	$: canSubmit = isFormValid && !isSubmitting && address;

	// Input validation and formatting functions
	function handleInput(event) {
		const value = event.target.value;
		// Allow only numbers and one decimal point
		const filtered = value.replace(/[^0-9.]/g, '');

		// Prevent multiple decimal points
		const parts = filtered.split('.');
		if (parts.length > 2) {
			event.target.value = parts[0] + '.' + parts.slice(1).join('');
		} else {
			event.target.value = filtered;
		}

		// Update the bound value
		depositAmount = event.target.value;
	}

	function handleKeydown(event) {
		const allowedKeys = [
			'Backspace',
			'Delete',
			'Tab',
			'Escape',
			'Enter',
			'ArrowLeft',
			'ArrowRight',
			'ArrowUp',
			'ArrowDown',
			'Home',
			'End'
		];

		const isNumber = event.key >= '0' && event.key <= '9';
		const isDecimal = event.key === '.';
		const isAllowedKey = allowedKeys.includes(event.key);
		const isCtrlA = event.ctrlKey && event.key === 'a';
		const isCtrlC = event.ctrlKey && event.key === 'c';
		const isCtrlV = event.ctrlKey && event.key === 'v';
		const isCtrlX = event.ctrlKey && event.key === 'x';

		if (!isNumber && !isDecimal && !isAllowedKey && !isCtrlA && !isCtrlC && !isCtrlV && !isCtrlX) {
			event.preventDefault();
		}

		// Handle Enter key for form submission
		if (event.key === 'Enter') {
			handleDeposit();
		}
	}

	// ================================
	// 3. DATA INPUT TO DATABASE
	// ================================

	// Main deposit handling function
	async function handleDeposit() {
		if (!canSubmit) return;

		isSubmitting = true;

		try {
			const depositData = {
				amount: parseFloat(depositAmount),
				address,
				timestamp: new Date().toISOString()
			};

			// TODO: Process deposit transaction
			await processDeposit(depositData);

			// Dispatch event for backend handling
			dispatch('deposit', depositData);

			// Clear form on success
			depositAmount = '';

			// TODO: Refresh user data after successful deposit
			await refreshUserData();
		} catch (error) {
			console.error('Deposit failed:', error);

			// Log error to database
			await logDepositError({
				address,
				amount: depositAmount,
				error: error.message,
				timestamp: new Date().toISOString()
			});

			// Handle error (could dispatch error event)
			dispatch('error', { type: 'deposit', message: error.message });
		} finally {
			isSubmitting = false;
		}
	}

	// Database operation functions
	async function processDeposit(depositData) {
		// TODO: Save deposit to database and process blockchain transaction
		// const response = await fetch('/api/deposits', {
		//     method: 'POST',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify(depositData)
		// });
		//
		// if (!response.ok) {
		//     throw new Error('Deposit processing failed');
		// }
		//
		// return await response.json();

		console.log('Processing deposit:', depositData);

		// Simulate processing delay
		await new Promise((resolve) => setTimeout(resolve, 2000));

		return { success: true, txHash: '0x' + Math.random().toString(16).slice(2) };
	}

	async function logDepositError(errorData) {
		// TODO: Log deposit errors to database for debugging
		// await fetch('/api/deposit-errors', {
		//     method: 'POST',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify(errorData)
		// });

		console.log('Deposit error logged:', errorData);
	}

	async function updatePlaygroundCredits(address, newAmount) {
		// TODO: Update user's playground credits in database
		// await fetch(`/api/credits/${address}`, {
		//     method: 'PUT',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify({ credits: newAmount })
		// });

		console.log('Playground credits updated:', { address, newAmount });
	}

	async function logDepositActivity(activityData) {
		// TODO: Log user deposit activity for analytics
		// await fetch('/api/user-activity', {
		//     method: 'POST',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify({
		//         type: 'deposit',
		//         ...activityData
		//     })
		// });

		console.log('Deposit activity logged:', activityData);
	}

	async function refreshUserData() {
		// TODO: Refresh user's deposits and credits after successful operation
		try {
			const [updatedDeposits, updatedCredits] = await Promise.all([
				fetchUserDeposits(address),
				fetchPlaygroundCredits(address)
			]);

			// Update reactive state
			deposits = updatedDeposits;
			playgroundCredits = updatedCredits;

			// Dispatch update event
			dispatch('dataRefresh', {
				deposits: updatedDeposits,
				credits: updatedCredits
			});
		} catch (error) {
			console.error('Failed to refresh user data:', error);
		}
	}

	async function saveDepositDraft(draftData) {
		// TODO: Save incomplete deposit as draft
		// await fetch('/api/deposit-drafts', {
		//     method: 'POST',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify(draftData)
		// });

		console.log('Deposit draft saved:', draftData);
	}

	async function deleteDepositRecord(depositId) {
		// TODO: Delete deposit record (admin function)
		// await fetch(`/api/deposits/${depositId}`, {
		//     method: 'DELETE'
		// });

		console.log('Deposit record deleted:', depositId);
	}

	async function updateDepositStatus(depositId, status) {
		// TODO: Update deposit status (pending, confirmed, failed)
		// await fetch(`/api/deposits/${depositId}/status`, {
		//     method: 'PUT',
		//     headers: { 'Content-Type': 'application/json' },
		//     body: JSON.stringify({ status })
		// });

		console.log('Deposit status updated:', { depositId, status });
	}
</script>

<svelte:head>
	<title>Deposit</title>
	<meta
		name="description"
		content="Stay tuned for Tensorone's upcoming staking feature. Soon you'll be able to stake $TPO tokens and earn rewards. More details coming soon!"
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-10 flex flex-col">
	<PageTitle subtitle="Deposits" title="My Deposits" {address} />

	<div
		class="bg-black rounded-xl border border-[#444A61] p-7 flex flex-col flex-1 overflow-y-auto content-start"
		in:fade|global={{ delay: 300, duration: 500 }}
		out:fade|global={{ duration: 300 }}
	>
		<!-- Deposit Form Component -->
		<DepositForm
			bind:depositAmount
			{isSubmitting}
			{playgroundCredits}
			{handleInput}
			{handleKeydown}
			{handleDeposit}
		/>

		<!-- Recent Deposits Component -->
		<RecentDeposits {recentDeposits} />
	</div>
</section>

<style>
	/* Smooth transitions */
	:global(input) {
		transition:
			border-color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out;
	}
</style>
