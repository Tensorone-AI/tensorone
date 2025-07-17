import { json } from '@sveltejs/kit';

export async function DELETE({ request }) {
	try {
		const { id } = await request.json();

		if (!id) {
			return json({ error: 'ID is required' }, { status: 400 });
		}

		// Ensure ID is a string
		const chatId = String(id);

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/delete-title`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				id: chatId
			})
		});

		if (!response.ok) {
			throw new Error(`Backend API returned ${response.status}`);
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Delete title API error:', error);
		return json({ error: 'Failed to delete chat' }, { status: 500 });
	}
}
