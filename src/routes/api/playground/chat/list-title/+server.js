import { json } from '@sveltejs/kit';

export async function GET({ url }) {
	try {
		const address = url.searchParams.get('address');
		
		if (!address) {
			return json({ error: 'address is required' }, { status: 400 });
		}

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/list-title`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				address: address
			})
		});

		if (!response.ok) {
			throw new Error(`Backend API returned ${response.status}`);
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('List titles API error:', error);
		return json({ error: 'Failed to list titles' }, { status: 500 });
	}
}
