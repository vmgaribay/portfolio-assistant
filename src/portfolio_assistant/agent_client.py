"""
Interactions with the Azure AI Foundry chat agent
"""
import requests
import logging
from portfolio_assistant.config import Config


class AgentClient:
    """
    Handle communication with the Azure AI Foundry chat agent.
    """

    def __init__(self, endpoint: str = None, api_key: str = None):
        self.endpoint = endpoint or Config.get_endpoint()
        self.api_key = api_key or Config.get_api_key()

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure chat agent endpoint and API key are required.")

    def ask(self, user_message: str, conversation_id: str = "default") -> dict:
        """
        Send a prompt to the AI agent and return the response.

        Args:
            user_message (str) - The question or input from the user.
            conversation_id (str) - Optional conversation thread ID.

        Returns:
            dict -  JSON response from the AI agent parsed into a dictionary.
        """

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        payload = {
            "messages": [
                {"role": "user", "content": user_message}
            ],
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
                    return {"reply": content}

            return data
        except requests.RequestException as e:
            logging.error(f"Request to AI agent failed: {e}")
            return {"error": str(e)}
