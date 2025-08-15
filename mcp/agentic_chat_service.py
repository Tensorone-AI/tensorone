from supabase_service import SupabaseService
from chat_service import ChatService
from search_agent_service import SearchAgentService

class AgenticChatService:
    def __init__(self):
        self.supabase_service = SupabaseService()
        self.chat_service = ChatService()
        self.search_agent_service = SearchAgentService()

    async def agentic_chat_completion(self, messages, slug, call=False):
        """
        Handle agentic chat completion with slug-based configuration
        If call=True, enhances system prompt for audio-optimized responses
        """
        try:
            # Check if slug starts with 'prebuilt-'
            if slug.startswith('prebuilt-'):
                # Get config from prebuilt-mcp table
                config = self.get_prebuilt_config(slug)
                if not config:
                    raise Exception(f"No prebuilt configuration found for slug: {slug}")
                
                # Extract system prompt and tools from config
                system_prompt = config.get('system_prompt', '')
                tools = config.get('tools', [])
                
                # Enhance system prompt for audio responses if call=True
                if call:
                    system_prompt = self._enhance_system_prompt_for_audio(system_prompt)
                
                # Check if web_search is in tools
                has_web_search = 'web_search' in tools

                # Get the latest user message for processing
                if messages and messages[-1].get('role') == 'user':
                    latest_message = messages[-1]['content']
                    
                    if has_web_search:
                        # Use search agent that can decide when to search
                        search_result = await self.search_agent_service.process_message(
                            latest_message,
                            system_prompt=system_prompt
                        )
                        
                        # Add assistant response to messages
                        updated_messages = messages.copy()
                        updated_messages.append({
                            'role': 'assistant',
                            'content': search_result['response']
                        })
                        
                        return {
                            'messages': updated_messages,
                            'config': config,
                            'has_web_search': has_web_search,
                            'search_performed': search_result.get('search_performed', False),
                            'search_results': search_result.get('search_results', [])
                        }
                    else:
                        # Use regular chat service
                        if system_prompt:
                            # Add system message at the beginning if not already present
                            if not messages or messages[0].get('role') != 'system':
                                messages.insert(0, {'role': 'system', 'content': system_prompt})
                        
                        result_messages = self.chat_service.chat_completion(messages)
                        
                        return {
                            'messages': result_messages,
                            'config': config,
                            'has_web_search': has_web_search,
                            'search_performed': False
                        }
                else:
                    # No user message to process
                    return {
                        'messages': messages,
                        'config': config,
                        'has_web_search': has_web_search,
                        'search_performed': False
                    }
            else:
                # Handle non-prebuilt slugs (regular chat)
                if call:
                    # Enhance system prompt for audio responses
                    messages_copy = messages.copy()
                    if not messages_copy or messages_copy[0].get('role') != 'system':
                        # No system prompt exists, create one
                        enhanced_prompt = self._enhance_system_prompt_for_audio("")
                        messages_copy.insert(0, {'role': 'system', 'content': enhanced_prompt})
                    else:
                        # Enhance existing system prompt
                        messages_copy[0]['content'] = self._enhance_system_prompt_for_audio(messages_copy[0]['content'])
                    
                    result_messages = self.chat_service.chat_completion(messages_copy)
                else:
                    result_messages = self.chat_service.chat_completion(messages)
                
                return {
                    'messages': result_messages,
                    'config': None,
                    'has_web_search': False,
                    'search_performed': False
                }
                
        except Exception as e:
            raise Exception(f"Error in agentic chat completion: {str(e)}")
    

    def get_prebuilt_config(self, slug):
        """
        Get configuration from prebuilt-mcp table by slug
        """
        try:
            response = self.supabase_service.client.table('prebuilt-mcp').select('config').eq('slug', slug).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]['config']
            else:
                return None
                
        except Exception as e:
            raise Exception(f"Error fetching prebuilt config: {str(e)}")
        
    def get_user_config(self, slug):
        """
        Get configuration from mcp table by slug
        """
        try:
            response = self.supabase_service.client.table('mcp').select('config').eq('slug', slug).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]['config']
            else:
                return None
                
        except Exception as e:
            raise Exception(f"Error fetching user config: {str(e)}")
    
    def _enhance_system_prompt_for_audio(self, original_prompt):
        """
        Enhance system prompt for audio responses - keep responses short and conversational
        Prevents double-enhancement if already enhanced
        """
        enhancement = "\n\nIMPORTANT: You are responding to audio input and your response will be converted to speech. Keep your responses extremely brief - maximum 1-2 sentences. Be direct, conversational, and natural. Avoid explanations, lists, or complex details."
        
        if original_prompt and "converted to speech" in original_prompt:
            return original_prompt
        
        if original_prompt:
            return original_prompt + enhancement
        else:
            return "You are a helpful AI assistant." + enhancement