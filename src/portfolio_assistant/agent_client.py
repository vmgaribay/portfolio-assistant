"""
Interactions with the Azure AI Foundry chat agent
"""
import requests
import logging
from portfolio_assistant.config import Config
from typing import Optional, List, Tuple, Dict
from portfolio_assistant.search_client import SearchClient


class AgentClient:
    """
    Handle communication with the Azure AI Foundry chat agent.
    """

    def __init__(self, endpoint: str = None, api_key: str = None,
                 search_client: Optional[SearchClient] = None):
        self.endpoint = endpoint or Config.get_chat_endpoint()
        self.api_key = api_key or Config.get_chat_api_key()
        self.search_client = search_client

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure chat agent endpoint and API key are required.")
        if self.search_client is None:
            logging.info("Azure AI Search functionality not enabled.")

    def _build_informed_messages(self, user_message: str) -> Tuple[
                                                    List[Dict], List[Dict]]:
        """
        Attempt to inform the user message with relevant document context.
        Args:
            user_message (str): The user's input message.
        Returns:
            Tuple[List[Dict], List[Dict]]: A tuple containing:
                - List of messages and a system prompt if context was found.
                - List of citations for the context used.
        """
        citations: List[Dict] = []
        if not self.search_client:
            return ([{"role": "user", "content": user_message}], citations)

        try:
            docs = self.search_client.search(user_message, top_k=5,
                                             semantic=True,
                                             semantic_config="searchConfig")
            context, citations = self.search_client.build_context(docs)
            if context:
                system = ("It is permitted to request clarification from "
                          "the user if there is very high ambiguity in the "
                          "user message meaning or intent. "
                          "Use only the context below to answer. "
                          "If the answer pertains to Victoria, specifically, "
                          "but is not in the context, specify "
                          "that there is uncertainty about "
                          "the response, and simply suggest contacting "
                          "Victoria for clarification. If the question is "
                          "basic or factual and can be reasonably answered "
                          "from general knowledge or context, it is permitted "
                          "to answer directly.\n\n"
                    f"Context:\n{context}"
                )
                return [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ], citations
        except Exception as e:
            logging.warning(f"Search retrieval failed; continuing without "
                            f"relevant document context: {e}")
        return ([{"role": "user", "content": user_message}], citations)

    def ask(self, user_message: str, conversation_id: str = "default") -> dict:
        """
        Send a prompt to the AI agent and return the response.

        Args:
            user_message (str) - The question or input from the user.
            conversation_id (str) - Optional conversation thread ID.

        Returns:
            dict -  JSON response from the AI agent parsed into a dictionary.
        """
        messages, citations = self._build_informed_messages(user_message)

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        payload = {
            "messages": messages,
            "max_tokens": 256
        }

        logging.info(f"POSTing to endpoint: {self.endpoint}")
        logging.info(f"Payload: {payload}")
        try:
            response = requests.post(self.endpoint, json=payload,
                                     headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if isinstance(
                    data, dict) and "choices" in data and data["choices"]:
                msg = data["choices"][0].get("message", {})
                content = msg.get("content") or data["choices"][0].get("text")
                if content:
                    result = {"reply": content}
                    if citations:
                        result["citations"] = citations
                    return result

            return data
        except requests.RequestException as e:
            logging.error(f"Request to AI agent failed: {e}")
            return {"error": str(e)}
