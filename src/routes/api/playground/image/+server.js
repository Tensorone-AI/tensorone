import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	try {
		const { prompt, width, height, model } = await request.json();

		if (!prompt || !prompt.trim()) {
			return json({ error: 'Prompt is required' }, { status: 400 });
		}

		const newPrompt = prompt.trim() + ` ${model}`;
		console.log('Received prompt:', newPrompt);

		// Prepare request body for backend API
		const requestBody = {
			prompt: newPrompt,
			width,
			height
		};

		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/text-to-image`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error('Backend Text-to-Image API error:', response.status, errorText);
			throw new Error(`Backend API error: ${response.status}`);
		}

		// The backend returns image/jpeg, we need to stream it back
		const imageBuffer = await response.arrayBuffer();

		return new Response(imageBuffer, {
			headers: {
				'Content-Type': 'image/jpeg',
				'Content-Disposition': 'attachment; filename="generated_image.jpg"'
			}
		});
	} catch (error) {
		console.error('Text-to-Image error:', error);
		return json({ error: 'Failed to generate image' }, { status: 500 });
	}
}
