import { json } from '@sveltejs/kit';

export async function POST({ request }) {
    try {
        const formData = await request.formData();
        const file = formData.get('file');
        const address = formData.get('address');

        if (!file || !address) {
            return json({ error: 'Missing file or address' }, { status: 400 });
        }

        const backendFormData = new FormData();
        backendFormData.append('file', file);
        backendFormData.append('address', address);

        const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/voice-clone`, {
            method: 'POST',
            body: backendFormData
        });

        if (!response.ok) {
            throw new Error(`Backend API error: ${response.status}`);
        }

        const data = await response.json();
        
        return json(data);
    } catch (error) {
        console.error('Voice clone error:', error);
        return json({ error: 'Failed to create voice clone' }, { status: 500 });
    }
}