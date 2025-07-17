export async function GET({ url }) {
	const address = url.searchParams.get('address');
	
	if (!address) {
		return new Response(JSON.stringify({ error: 'Address parameter is required' }), {
			status: 400,
			headers: { 'Content-Type': 'application/json' }
		});
	}

	try {
		const response = await fetch(`${import.meta.env.VITE_DAPP_BACKEND_URL}/api/get-voice-clone?address=${encodeURIComponent(address)}`);
		
		if (!response.ok) {
			if (response.status === 404) {
				return new Response(JSON.stringify({ 
					address, 
					voice_clone_id: null, 
					message: 'No voice clone found for this address' 
				}), {
					status: 200,
					headers: { 'Content-Type': 'application/json' }
				});
			}
			throw new Error(`Backend API error: ${response.status}`);
		}
		
		const data = await response.json();
		
		return new Response(JSON.stringify(data), {
			status: 200,
			headers: { 'Content-Type': 'application/json' }
		});
	} catch (error) {
		console.error('Error fetching voice clone:', error);
		return new Response(JSON.stringify({ error: 'Failed to fetch voice clone data' }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' }
		});
	}
}