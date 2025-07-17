import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { address, request_id, prompt } = await request.json();

		if (!address || !request_id || !prompt) {
			return json({ error: 'Address, request_id, and prompt are required' }, { status: 400 });
		}

		if (!prompt.trim()) {
			return json({ error: 'Prompt cannot be empty' }, { status: 400 });
		}

		const requestBody = {
			address,
			request_id,
			prompt: prompt.trim()
		};

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/generate-video`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error('Backend generate-video API error:', response.status, errorText);
			throw new Error(`Backend API error: ${response.status}`);
		}

		const result = await response.json();
		return json(result);
	} catch (error) {
		console.error('Generate video error:', error);
		return json({ error: 'Failed to generate video' }, { status: 500 });
	}
}