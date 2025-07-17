import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { prompt, conversation, agent, agentSlug, isTemplate } = await request.json();

		if (!prompt || !agentSlug) {
			return json({ error: 'Prompt and agent slug are required' }, { status: 400 });
		}

		// Ensure slug starts with 'prebuilt-' for MCP backend compatibility
		const mcpSlug = agentSlug.startsWith('prebuilt-') ? agentSlug : `prebuilt-${agentSlug}`;

		// Build messages array from conversation history
		const messages = [];
		
		// Add conversation history
		if (conversation && Array.isArray(conversation)) {
			conversation.forEach(item => {
				if (item.type === 'user') {
					messages.push({
						role: 'user',
						content: item.message
					});
				} else if (item.type === 'assistant') {
					messages.push({
						role: 'assistant',
						content: item.message
					});
				}
			});
		}

		// Add current user message
		messages.push({
			role: 'user',
			content: prompt
		});

		// Call MCP backend agentic-chat endpoint
		const response = await fetch(`${import.meta.env.VITE_MCP_BACKEND_URL}/api/agentic-chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				messages: messages,
				slug: mcpSlug
			})
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error(`MCP Backend API returned ${response.status}:`, errorText);
			throw new Error(`MCP Backend API returned ${response.status}`);
		}

		const data = await response.json();

		// Extract only the assistant response (don't duplicate the entire conversation)
		let assistantMessage = '';
		
		if (data.messages && data.messages.length > 0) {
			// Get the last assistant message from the response
			const lastAssistantMessage = data.messages
				.filter(msg => msg.role === 'assistant')
				.pop();

			if (lastAssistantMessage) {
				// Remove leading newlines and whitespace from the response
				assistantMessage = lastAssistantMessage.content.replace(/^\s+/, '');
			}
		}

		return json({
			assistantMessage: assistantMessage,
			config: data.config || null,
			has_web_search: data.has_web_search || false,
			search_performed: data.search_performed || false,
			search_results: data.search_results || []
		});

	} catch (error) {
		console.error('MCP Agentic Chat API error:', error);
		return json({ error: 'Failed to process agentic chat message' }, { status: 500 });
	}
}