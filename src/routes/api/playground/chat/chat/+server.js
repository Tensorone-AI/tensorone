import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { id, message } = await request.json();

		if (!message || !id) {
			return json({ error: 'Message and ID is required' }, { status: 400 });
		}

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				id: id,
				message: message
			})
		});

		if (!response.ok) {
			throw new Error(`Backend API returned ${response.status}`);
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Chat API error:', error);
		return json({ error: 'Failed to process chat message' }, { status: 500 });
	}
}
