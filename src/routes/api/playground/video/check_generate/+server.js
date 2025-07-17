import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { address } = await request.json();

		if (!address) {
			return json({ error: 'Address is required' }, { status: 400 });
		}

		const requestBody = {
			address
		};

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/check-generate`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error('Backend check-generate API error:', response.status, errorText);
			throw new Error(`Backend API error: ${response.status}`);
		}

		const result = await response.json();
		return json(result);
	} catch (error) {
		console.error('Check generate error:', error);
		return json({ error: 'Failed to check generation status' }, { status: 500 });
	}
}