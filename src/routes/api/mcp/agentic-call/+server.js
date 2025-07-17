import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		// Parse multipart form data
		const formData = await request.formData();
		const audioFile = formData.get('audio');
		const agentSlug = formData.get('slug');

		if (!audioFile || !agentSlug) {
			return json({ error: 'Audio file and agent slug are required' }, { status: 400 });
		}

		// Ensure slug starts with 'prebuilt-' for MCP backend compatibility
		const mcpSlug = agentSlug.startsWith('prebuilt-') ? agentSlug : `prebuilt-${agentSlug}`;

		// Create form data for MCP backend
		const mcpFormData = new FormData();
		mcpFormData.append('audio', audioFile);
		mcpFormData.append('slug', mcpSlug);

		// Call MCP backend agentic-call endpoint
		const response = await fetch(`${import.meta.env.VITE_MCP_BACKEND_URL}/api/agentic-call`, {
			method: 'POST',
			body: mcpFormData
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error(`MCP Backend API returned ${response.status}:`, errorText);
			throw new Error(`MCP Backend API returned ${response.status}`);
		}

		// Get the audio response
		const audioBuffer = await response.arrayBuffer();

		// Return the audio response with proper headers
		return new Response(audioBuffer, {
			headers: {
				'Content-Type': 'audio/mpeg',
				'Content-Length': audioBuffer.byteLength.toString()
			}
		});

	} catch (error) {
		console.error('MCP Agentic Call API error:', error);
		return json({ error: 'Failed to process agentic call' }, { status: 500 });
	}
}