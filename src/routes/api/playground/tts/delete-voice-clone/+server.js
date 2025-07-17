import { json } from '@sveltejs/kit';

export async function DELETE({ request }) {
    try {
        const { address } = await request.json();

        if (!address) {
            return json({ error: 'Missing address' }, { status: 400 });
        }

        const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/delete-voice-clone`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address })
        });

        if (!response.ok) {
            throw new Error(`Backend API error: ${response.status}`);
        }

        const data = await response.json();
        
        return json(data);
    } catch (error) {
        console.error('Delete voice clone error:', error);
        return json({ error: 'Failed to delete voice clone' }, { status: 500 });
    }
}