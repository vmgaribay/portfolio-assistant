"""
Set variables for endpoint and key.
"""
import os

AZURE_CHAT_AGENT_ENDPOINT = os.getenv("AZURE_CHAT_AGENT_ENDPOINT")
AZURE_CHAT_API_KEY = os.getenv("AZURE_CHAT_API_KEY")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION")


class Config:
    """
    Mainly for testing, update env vars if needed
    """
    @staticmethod
    def get_chat_endpoint() -> str:
        return os.getenv("AZURE_CHAT_AGENT_ENDPOINT",
                         AZURE_CHAT_AGENT_ENDPOINT)

    @staticmethod
    def get_chat_api_key() -> str:
        return os.getenv("AZURE_CHAT_API_KEY",
                         AZURE_CHAT_API_KEY)

    @staticmethod
    def get_search_endpoint() -> str:
        return os.getenv("AZURE_SEARCH_ENDPOINT",
                         AZURE_SEARCH_ENDPOINT)

    @staticmethod
    def get_search_api_key() -> str:
        return os.getenv("AZURE_SEARCH_API_KEY",
                         AZURE_SEARCH_API_KEY)

    @staticmethod
    def get_search_index_name() -> str:
        return os.getenv("AZURE_SEARCH_INDEX_NAME",
                         AZURE_SEARCH_INDEX_NAME)

    @staticmethod
    def get_search_api_version() -> str:
        return os.getenv("AZURE_SEARCH_API_VERSION",
                         AZURE_SEARCH_API_VERSION)
