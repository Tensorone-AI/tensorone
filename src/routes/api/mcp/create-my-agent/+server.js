import { json } from '@sveltejs/kit';

const MCP_API_BASE_URL = `${import.meta.env.VITE_MCP_BACKEND_URL}/api`;

export async function POST({ request }) {
	try {
		const { address, agent_name, description, total_cu, config, call } = await request.json();

		// total_cu are cost, agent_description is characterDetails and call is voice

		if (!address || !agent_name || !description || !total_cu || !config) {
			return json(
				{
					success: false,
					error:
						'Missing required fields: address, agent_name, total_cu, config, and description are required'
				},
				{ status: 400 }
			);
		}

		const requestBody = {
			address: address,
			agent_name: agent_name,
			description: description,
			total_cu: total_cu,
			config: config,
			call: call || null
		};

		const response = await fetch(`${MCP_API_BASE_URL}/create-my-agent`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		});

		const data = await response.json();

		if (!response.ok) {
			return json(
				{
					success: false,
					error: data.error || 'Failed to create agent'
				},
				{ status: response.status }
			);
		}

		return json({
			success: true,
			data
		});
	} catch (error) {
		console.error('Error creating agent:', error);
		return json(
			{
				success: false,
				error: 'Internal server error'
			},
			{ status: 500 }
		);
	}
}
