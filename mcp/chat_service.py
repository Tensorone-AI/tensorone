from openai import OpenAI
from typing import Dict, List
from supabase_service import SupabaseService

class ChatService:
    def __init__(self):
        self.deepinfra_api_key = 'API_KEY'
        self.deepinfra_model = "meta-llama/Meta-Llama-3-8B-Instruct"

        self.openai_client = OpenAI(
            api_key=self.deepinfra_api_key,
            base_url="https://api.deepinfra.com/v1/openai"
        )

        self.supabase_service = SupabaseService()
        self.supabase_client = self.supabase_service.client

    def chat_completion(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Generate chat completion using DeepInfra with OpenAI compatible API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            List of all messages including the assistant's response
        """
        try:
            chat_completion = self.openai_client.chat.completions.create(
                model=self.deepinfra_model,
                messages=messages
            )

            assistant_message = chat_completion.choices[0].message.content

            updated_messages = messages.copy()
            updated_messages.append({
                "role": "assistant",
                "content": assistant_message
            })

            return updated_messages

        except Exception as e:
            raise Exception(f"DeepInfra chat error: {str(e)}")
