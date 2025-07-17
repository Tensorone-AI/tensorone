import { error, json } from '@sveltejs/kit';

export async function POST({ request }) {
	const { product, description, amount, currency, producttype, email, address } =
		await request.json();

	try {
		const response = await fetch('https://api.commerce.coinbase.com/charges', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CC-Api-Key': import.meta.env.VITE_COINBASE_API_KEY
			},
			body: JSON.stringify({
				name: product,
				description: description,
				local_price: {
					amount: amount,
					currency: currency
				},
				pricing_type: 'fixed_price',
				metadata: {
					producttype: producttype,
					email: email,
					address: address
				}
			})
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const charge = await response.json();
		return json({ chargeId: charge.data.id, hostedUrl: charge.data.hosted_url });
	} catch (err) {
		console.error('Error creating charge:', err);
		throw error(500, 'Failed to create charge');
	}
}
