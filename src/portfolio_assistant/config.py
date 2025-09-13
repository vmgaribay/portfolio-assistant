"""
Set variables for endpoint and key.
"""
import os

AZURE_CHAT_AGENT_ENDPOINT = os.getenv("AZURE_CHAT_AGENT_ENDPOINT")
AZURE_CHAT_API_KEY = os.getenv("AZURE_CHAT_API_KEY")


class Config:
    """
    Mainly for testing, update env vars if needed
    """
    @staticmethod
    def get_endpoint() -> str:
        return os.getenv("AZURE_CHAT_AGENT_ENDPOINT",
                         AZURE_CHAT_AGENT_ENDPOINT)

    @staticmethod
    def get_api_key() -> str:
        return os.getenv("AZURE_CHAT_API_KEY",
                         AZURE_CHAT_API_KEY)
