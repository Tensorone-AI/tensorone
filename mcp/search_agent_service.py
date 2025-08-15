from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from typing import Dict, List, Optional, Any
import requests
from dataclasses import dataclass

@dataclass
class SearchContext:
    """Context for search operations"""
    query: str
    max_results: int = 5

class SearchResult(BaseModel):
    """Search result model"""
    title: str
    url: str
    content: str
    score: Optional[float] = None

class SearchResponse(BaseModel):
    """Search response model"""
    query: str
    results: List[SearchResult]
    total_results: int

class TavilySearchService:
    """Service for performing web searches using Tavily API"""

    def __init__(self):
        self.api_key = "API_KEY"  # Replace with actual Tavily API key
        self.base_url = "https://api.tavily.com/search"

    def search(self, query: str, max_results: int = 5) -> SearchResponse:
        """
        Perform web search using Tavily API

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            SearchResponse with search results
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "include_answer": False,
                "include_raw_content": False,
                "max_results": max_results
            }

            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()

            data = response.json()

            # Parse Tavily response
            search_results = []
            for result in data.get("results", []):
                search_results.append(SearchResult(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    content=result.get("content", ""),
                    score=result.get("score")
                ))

            return SearchResponse(
                query=query,
                results=search_results,
                total_results=len(search_results)
            )

        except Exception as e:
            # Return empty results on error
            return SearchResponse(
                query=query,
                results=[],
                total_results=0
            )

class SearchAgentService:
    """Service for managing search agent using pydantic-ai"""

    def __init__(self):
        self.tavily_service = TavilySearchService()

        # Configure DeepInfra model with OpenAI-compatible API
        self.deepinfra_model = OpenAIModel(
            'Qwen/Qwen3-235B-A22B',
            provider=OpenAIProvider(
                api_key='API_KEY',
                base_url='https://api.deepinfra.com/v1/openai'
            )
        )

        # Default system prompt (fallback)
        self.default_system_prompt = """You are a search assistant. Your job is to:
1. Analyze user queries to determine if they need web search
2. If search is needed, extract the best search query
3. Process search results and provide a comprehensive answer
4. If no search is needed, respond normally

You have access to a web search tool. Use it when:
- User asks for recent/current information
- User asks about news, events, or developments
- User asks about specific facts that might have changed
- User explicitly asks you to search

Do not search for:
- General knowledge questions
- Mathematical calculations
- Code explanations
- Personal opinions or advice
"""

    def create_search_agent(self, system_prompt: str = None):
        """Create a search agent with custom system prompt"""
        prompt = system_prompt or self.default_system_prompt

        # Add search tool instructions to the system prompt
        enhanced_prompt = f"""{prompt}

You have access to a web search tool. Use it when the user's query requires up-to-date information or when explicitly asked to search.

Available tool:
- web_search(query: str) -> str: Search the web for information
"""

        # Create agent with custom system prompt
        agent = Agent(
            model=self.deepinfra_model,
            system_prompt=enhanced_prompt,
            deps_type=SearchContext,
            retries=2
        )

        # Add search tool to agent
        @agent.tool
        def web_search(ctx: RunContext[SearchContext], query: str) -> str:
            """Search the web for information"""
            search_response = self.tavily_service.search(query, max_results=5)

            if not search_response.results:
                return "No search results found."

            # Format search results
            formatted_results = []
            for result in search_response.results:
                formatted_results.append(f"**{result.title}**\n{result.content}\nSource: {result.url}")

            return "\n\n".join(formatted_results)

        return agent

    async def process_message(self, message: str, user_query: str = None, system_prompt: str = None) -> Dict[str, Any]:
        """
        Process a message with the search agent

        Args:
            message: The user message
            user_query: Optional specific search query
            system_prompt: Optional custom system prompt

        Returns:
            Dict with response and search results
        """
        try:
            # Create context
            context = SearchContext(
                query=user_query or message,
                max_results=5
            )

            # Create agent with custom system prompt
            search_agent = self.create_search_agent(system_prompt)

            # Run the agent (await the coroutine)
            result = await search_agent.run(message, deps=context)

            # Extract search results if any were performed
            search_results = []
            search_performed = False

            if hasattr(result, 'all_messages'):
                for msg in result.all_messages():
                    if hasattr(msg, 'role') and msg.role == 'tool':
                        search_performed = True
                        # Extract search results from tool calls
                        if hasattr(msg, 'content'):
                            search_results.append(msg.content)

            return {
                'response': result.data,
                'search_performed': search_performed,
                'search_results': search_results
            }

        except Exception as e:
            return {
                'response': f"Error processing message: {str(e)}",
                'search_performed': False,
                'search_results': []
            }

    def manual_search(self, query: str) -> SearchResponse:
        """
        Perform a manual search without the agent

        Args:
            query: Search query

        Returns:
            SearchResponse with results
        """
        return self.tavily_service.search(query)
