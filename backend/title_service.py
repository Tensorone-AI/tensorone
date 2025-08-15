import requests
from typing import List, Dict
from supabase_service import SupabaseService


class TitleService:
    def __init__(self):
        # LemonFox configuration for title generation
        self.lemonfox_api_key = "API_KEY"
        self.lemonfox_base_url = "https://api.lemonfox.ai/v1"
        self.lemonfox_headers = {
            "Authorization": f"Bearer {self.lemonfox_api_key}",
            "Content-Type": "application/json"
        }
        self.supabase_service = SupabaseService()
        self.supabase_client = self.supabase_service.client


    def generate_conversation_title(self, conversation_text: str, address: str) -> dict:
        """
        Generate a conversation title using LemonFox API and store it in Supabase.
        Returns a title with maximum 4 words and the Supabase record ID.

        Args:
            conversation_text: The conversation text to generate title for
            address: The user address to store the title for

        Returns:
            Dict containing the generated title (4 words max) and Supabase ID
        """
        url = f"{self.lemonfox_base_url}/chat/completions"

        # Prepare the messages for title generation
        messages = [
            {
                "role": "system",
                "content": "You are a title generator. Given a conversation text, create a concise title that captures the main topic or theme. Respond with exactly 4 words maximum. Do not include any punctuation or extra text, just the title words."
            },
            {
                "role": "user",
                "content": f"Generate a title for this conversation (4 words max): {conversation_text}"
            }
        ]

        data = {
            "messages": messages,
            "model": "llama-8b-chat",
            "max_tokens": 10,
            "temperature": 0.3
        }

        response = requests.post(url, json=data, headers=self.lemonfox_headers)

        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                title = result["choices"][0]["message"]["content"].strip()
                # Ensure it's 4 words max
                words = title.split()
                if len(words) > 4:
                    title = " ".join(words[:4])

                # Store title in Supabase chat table
                try:
                    result = self.supabase_client.table('chat').insert({
                        'address': address,
                        'title': title
                    }).execute()

                    record_id = result.data[0]['id'] if result.data else None
                    return {"title": title, "id": record_id}
                except Exception as e:
                    # Log error but don't fail the title generation
                    print(f"Failed to store title in Supabase: {str(e)}")
                    return {"title": title, "id": None}
            else:
                # Store default title
                default_title = "Conversation Title"
                try:
                    result = self.supabase_client.table('chat').insert({
                        'address': address,
                        'title': default_title
                    }).execute()

                    record_id = result.data[0]['id'] if result.data else None
                    return {"title": default_title, "id": record_id}
                except Exception as e:
                    print(f"Failed to store default title in Supabase: {str(e)}")
                    return {"title": default_title, "id": None}
        else:
            # Store default title for failed requests
            default_title = "Conversation Title"
            try:
                result = self.supabase_service.client.table('chat').insert({
                    'address': address,
                    'title': default_title
                }).execute()

                record_id = result.data[0]['id'] if result.data else None
                return {"title": default_title, "id": record_id}
            except Exception as e:
                print(f"Failed to store default title in Supabase: {str(e)}")
                return {"title": default_title, "id": None}

    def list_titles_by_address(self, address: str) -> List[Dict[str, str]]:
        """
        Get all titles, IDs, and created_at timestamps from the chat table for a given address.

        Args:
            address: The address to filter conversations by

        Returns:
            List of dictionaries containing 'id', 'title', and 'created_at' keys
        """
        try:
            response = self.supabase_client.table('chat').select('id, title, created_at').eq('address', address).order('created_at', desc=True).execute()

            if response.data:
                return response.data
            else:
                return []

        except Exception as e:
            raise Exception(f"Error retrieving titles: {str(e)}")

    def delete_title_by_id(self, title_id: str) -> bool:
        """
        Delete a chat record from the chat table by ID.

        Args:
            title_id: The ID of the chat record to delete

        Returns:
            True if deleted successfully, False if record not found
        """
        try:
            response = self.supabase_client.table('chat').delete().eq('id', title_id).execute()

            if response.data and len(response.data) > 0:
                return True
            else:
                return False

        except Exception as e:
            raise Exception(f"Error deleting title: {str(e)}")
