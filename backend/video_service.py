from flask import jsonify
from supabase import create_client, Client

class VideoService:
    def __init__(self):
        self.url = 'SUPABASE_URL'
        self.key = 'SUPABASE_KEY'
        self.client_second: Client = create_client(self.url, self.key)


    def generate_video(self, address: str, request_id: str, prompt: str) -> str:
        """
        Inserts a new row into the vid_queue table with the given address as user_id,
        request_id and prompt.
        Returns the request_id upon success.
        """
        payload = {
            'user_id': address,
            'request_id': request_id,
            'prompt': prompt,
        }
        try:
            response = self.client_second.from_('vid_queue').insert(payload).execute()
        except Exception as e:
            return jsonify({"error": f"Error inserting row into Supabase: {e}"})

        status_code = getattr(response, 'status_code', None)
        if status_code is not None and status_code >= 300:
            status_text = getattr(response, 'status_text', '')
            return jsonify({"error": f"Supabase returned error {status_code}: {status_text}"})
        else:
            return request_id

    def check_generate(self, address: str) -> dict:
        """
        Checks the latest video generation status for a given address.
        Returns 'nothing' if no rows found, 'waiting' if result_video_path is None,
        or 'complete' with result_video_path if available.
        """
        try:
            response = self.client_second.from_('vid_queue').select('*').eq('user_id', address).order('added_at', desc=True).limit(1).execute()
        except Exception as e:
            return {"error": f"Error querying Supabase: {e}"}

        status_code = getattr(response, 'status_code', None)
        if status_code is not None and status_code >= 300:
            status_text = getattr(response, 'status_text', '')
            return {"error": f"Supabase returned error {status_code}: {status_text}"}

        if not response.data:
            return {"status": "nothing"}

        row = response.data[0]
        result_video_path = row.get('result_video_path')

        if result_video_path is None:
            return {"status": "waiting"}
        else:
            return {"status": "complete", "result_video_path": result_video_path}
