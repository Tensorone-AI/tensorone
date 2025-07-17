import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { text, address } = await request.json();

		if (!text || !address) {
			return json({ error: 'text and address is required' }, { status: 400 });
		}
		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/generate-title`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				text: text,
				address: address
			})
		});

		if (!response.ok) {
			throw new Error(`Backend API returned ${response.status}`);
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Generate title API error:', error);
		return json({ error: 'Failed to generate title' }, { status: 500 });
	}
}
