import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { id } = await request.json();

		if (!id) {
			return json({ error: 'ID is required' }, { status: 400 });
		}

		console.log('Retrieving chat with ID:', id, 'Type:', typeof id);

		// Ensure ID is a string
		const chatId = String(id);

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/retrieve-chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				id: chatId
			})
		});

		console.log('Backend response status:', response.status);

		if (!response.ok) {
			const errorText = await response.text();
			console.error('Backend error response:', errorText);
			return json({ error: `Backend API returned ${response.status}: ${errorText}` }, { status: response.status });
		}

		const data = await response.json();
		console.log('Retrieved data:', data);
		return json(data);
	} catch (error) {
		console.error('Retrieve chat API error:', error);
		return json({ error: 'Failed to retrieve chat', details: error.message }, { status: 500 });
	}
}
