import { json } from '@sveltejs/kit';

export async function POST({ request }) {
    try {
        const { text, voice } = await request.json();

        if (!text || !text.trim()) {
            return json({ error: 'Text is required' }, { status: 400 });
        }

        // Prepare request body for backend API
        const requestBody = {
            text: text.trim()
        };

        // Add voice parameter if provided
        if (voice) {
            requestBody.voice = voice;
        }

        console.log('TTS Request:', requestBody);

        const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Backend TTS API error:', response.status, errorText);
            throw new Error(`Backend API error: ${response.status}`);
        }

        // The backend returns audio/mpeg, we need to stream it back
        const audioBuffer = await response.arrayBuffer();
        
        return new Response(audioBuffer, {
            headers: {
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': 'attachment; filename="generated_speech.mp3"'
            }
        });
    } catch (error) {
        console.error('TTS error:', error);
        return json({ error: 'Failed to generate speech' }, { status: 500 });
    }
}