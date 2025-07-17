import { Resend } from 'resend';

const resend = new Resend(import.meta.env.VITE_RESEND_API_KEY);

export async function POST({ request }) {
	try {
		const { subject, html, to } = await request.json();
		const { data, error } = await resend.emails.send({
			from: 'Support <support@tensorone.ai>',
			to: [to],
			subject: subject,
			html: html
		});

		return json({ status: 'ok' });
	} catch (error) {
		console.error('There was an error:', error);
		return json({ status: 'error' });
	}
}
