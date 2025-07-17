import { json } from '@sveltejs/kit';

const MCP_API_BASE_URL = `${import.meta.env.VITE_MCP_BACKEND_URL}/api`;

export async function POST({ request }) {
	try {
		const { id } = await request.json();

		if (!id) {
			return json({
				success: false,
				error: 'Missing required field: id is required'
			}, { status: 400 });
		}

		const response = await fetch(`${MCP_API_BASE_URL}/get-my-agent`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				id
			})
		});

		const data = await response.json();

		if (!response.ok) {
			return json({
				success: false,
				error: data.error || 'Failed to get agent'
			}, { status: response.status });
		}

		return json({
			success: true,
			data
		});

	} catch (error) {
		console.error('Error getting agent:', error);
		return json({
			success: false,
			error: 'Internal server error'
		}, { status: 500 });
	}
}