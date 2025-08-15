import requests
from supabase_service import SupabaseService

class VoiceCloneService:
    def __init__(self):
        self.api_key = "API_KEY"
        self.user_id = "USER_ID"
        self.supabase_service = SupabaseService()
        self.supabase_client = self.supabase_service.client

    def create_voice_clone(self, audio_file, address):
        """
        Create a voice clone using PlayHT API and store in Supabase
        Returns response containing id, name, and type
        """
        url = "https://api.play.ht/api/v2/cloned-voices/instant"

        headers = {
            "accept": "application/json",
            "AUTHORIZATION": self.api_key,
            "X-USER-ID": self.user_id
        }

        files = {
            "sample_file": ("audio.mp3", audio_file, "audio/mpeg")
        }

        data = {
            "voice_name": address
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 201:
            voice_clone_data = response.json()
            voice_clone_id = voice_clone_data.get('id')

            self.update_voice_clone_id(address, voice_clone_id)

            return voice_clone_data
        else:
            response.raise_for_status()

    def update_voice_clone_id(self, address, voice_clone_id):
        """
        Update voice_clone_id for a user with the given address
        If user doesn't exist, create a new record
        """
        try:
            # First, check if user exists
            result = self.supabase_client.table('user').select('*').eq('address', address).execute()

            if result.data:
                # User exists, update the voice_clone_id
                response = self.supabase_client.table('user').update({
                    'voice_clone_id': voice_clone_id
                }).eq('address', address).execute()
            else:
                # User doesn't exist, create new record
                response = self.supabase_client.table('user').insert({
                    'address': address,
                    'voice_clone_id': voice_clone_id
                }).execute()

            return response.data
        except Exception as e:
            raise Exception(f"Supabase operation failed: {str(e)}")

    def get_voice_clone_id(self, address):
        """
        Get voice_clone_id for a user with the given address
        """
        try:
            result = self.supabase_client.table('user').select('voice_clone_id').eq('address', address).execute()
            if result.data:
                return result.data[0]['voice_clone_id']
            return None
        except Exception as e:
            raise Exception(f"Supabase query failed: {str(e)}")

    def delete_voice_clone(self, address):
        """
        Delete a voice clone using PlayHT API and remove from Supabase
        Returns response from PlayHT API
        """
        try:
            # First, get the voice clone ID for this address
            voice_clone_id = self.get_voice_clone_id(address)

            if not voice_clone_id:
                raise Exception("No voice clone found for this address")

            # Delete from PlayHT API
            url = "https://api.play.ht/api/v2/cloned-voices/"

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "AUTHORIZATION": self.api_key,
                "X-USER-ID": self.user_id
            }

            payload = {
                "voice_id": voice_clone_id
            }

            response = requests.delete(url, json=payload, headers=headers)

            if response.status_code == 200:
                # If PlayHT deletion successful, remove from Supabase
                try:
                    self.supabase_client.table('user').update({
                        'voice_clone_id': None
                    }).eq('address', address).execute()
                except Exception as e:
                    print(f"Warning: Failed to remove voice clone ID from Supabase: {str(e)}")

                return {"message": "Voice clone deleted successfully", "voice_id": voice_clone_id}
            else:
                response.raise_for_status()

        except Exception as e:
            raise Exception(f"Failed to delete voice clone: {str(e)}")
