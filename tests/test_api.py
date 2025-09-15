"""Tests for Chat API"""

import json
from unittest.mock import patch
from chat_function import main

class MockRequest:
    """Mimics HttpRequest for testing"""
    def __init__(self, body: dict):
        self._body = body

    def get_json(self):
        return self._body

    def get_body(self):
        return json.dumps(self._body).encode()

@patch("portfolio_assistant.agent_client.AgentClient.ask")
def test_api_success(mock_ask, monkeypatch):
    monkeypatch.setenv("AZURE_CHAT_AGENT_ENDPOINT", "https://test-endpoint")
    monkeypatch.setenv("AZURE_CHAT_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://test-endpoint")
    monkeypatch.setenv("AZURE_SEARCH_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_SEARCH_INDEX_NAME", "test-index")
    monkeypatch.setenv("AZURE_SEARCH_API_VERSION", "test-version")


    mock_ask.return_value = {"reply": "Hmmm, I hear she is pretty bad at sports!"}

    req = MockRequest({"message": "Is there anything Victoria can't do?"})
    response = main(req)
    data = json.loads(response.get_body())


    assert response.status_code == 200
    assert data["reply"] == "Hmmm, I hear she is pretty bad at sports!"

@patch("portfolio_assistant.agent_client.AgentClient.ask")
def test_api_error(monkeypatch):
    monkeypatch.setenv("AZURE_CHAT_AGENT_ENDPOINT", "https://test-endpoint")
    monkeypatch.setenv("AZURE_CHAT_API_KEY", "test-key")

    req = MockRequest({"message": None})
    response = main(req)
    data = json.loads(response.get_body())

    assert response.status_code == 400
    assert "Missing user message" in data["error"]

@patch("portfolio_assistant.agent_client.AgentClient.ask")
def test_api_exception(mock_ask):
    # a little redundant since no env vars set triggers 
    # exception anyway, but...
    mock_ask.side_effect = Exception("Test error!")

    req = MockRequest({"message": "Trigger exception"})
    response = main(req)

    assert response.status_code == 500


