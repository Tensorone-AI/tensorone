import requests
from typing import Dict, List, Optional
from supabase_service import SupabaseService

class ChatService:
    def __init__(self):
        # Venice AI configuration
        self.venice_api_key = "API_KEY"
        self.venice_base_url = "https://api.venice.ai/api/v1/chat/completions"
        self.venice_headers = {
            "Authorization": f"Bearer {self.venice_api_key}",
            "Content-Type": "application/json"
        }
        self.venice_model = "venice-uncensored"

        self.supabase_service = SupabaseService()
        self.supabase_client = self.supabase_service.client


    def chat_completion(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Generate chat completion using Venice AI's venice-uncensored model.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            List of all messages including the assistant's response
        """
        try:
            # Limit messages to 6 dicts maximum for Venice AI
            messages_to_send = messages[-6:] if len(messages) > 6 else messages

            payload = {
                "messages": messages_to_send,
                "model": self.venice_model
            }

            response = requests.post(
                self.venice_base_url,
                json=payload,
                headers=self.venice_headers
            )

            if response.status_code == 200:
                result = response.json()
                assistant_message = result["choices"][0]["message"]["content"]

                # Always keep all original messages and add the new assistant message
                updated_messages = messages.copy()
                updated_messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })

                return updated_messages
            else:
                raise Exception(f"Venice AI API error: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"Venice AI chat error: {str(e)}")

    def get_messages(self, conversation_id: str) -> Optional[List[Dict[str, str]]]:
        """
        Get messages from the chat table for a given conversation ID.

        Args:
            conversation_id: The conversation ID to retrieve messages for

        Returns:
            List of message dictionaries or None if no conversation exists
        """
        try:
            response = self.supabase_client.table('chat').select('messages').eq('id', conversation_id).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['messages']
            else:
                return None

        except Exception as e:
            raise Exception(f"Error retrieving messages: {str(e)}")

    def store_messages(self, conversation_id: str, messages: List[Dict[str, str]]) -> bool:
        """
        Store or update messages in the chat table for a given conversation ID.

        Args:
            conversation_id: The conversation ID to store messages for
            messages: List of message dictionaries to store

        Returns:
            True if successful
        """
        try:
            # Check if conversation exists
            existing = self.supabase_client.table('chat').select('id').eq('id', conversation_id).execute()

            if existing.data and len(existing.data) > 0:
                # Update existing conversation
                self.supabase_client.table('chat').update({
                    'messages': messages
                }).eq('id', conversation_id).execute()
            else:
                # Insert new conversation
                self.supabase_client.table('chat').insert({
                    'id': conversation_id,
                    'messages': messages
                }).execute()

            return True

        except Exception as e:
            raise Exception(f"Error storing messages: {str(e)}")
