"""Tests for agent_client.py"""
import pytest
import requests
from portfolio_assistant.agent_client import AgentClient

def test_init_with_args():
    client = AgentClient(endpoint="https://custom-endpoint", api_key="custom-key")
    assert client.endpoint == "https://custom-endpoint"
    assert client.api_key == "custom-key"

def test_init_missing_key():
    with pytest.raises(ValueError):
        AgentClient(endpoint="https://test-endpoint", api_key=None)

def test_ask_success(monkeypatch):
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return {"reply": "Debateable..."}
    monkeypatch.setattr("requests.post", lambda *a, **kw: MockResponse())
    client = AgentClient(endpoint="https://test-endpoint", api_key="test-key")
    result = client.ask("Is anybody there?")
    assert result == {"reply": "Debateable..."}

def test_ask_failure(monkeypatch):
    class MockResponse:
        def raise_for_status(self): raise requests.RequestException("fail")
    monkeypatch.setattr("requests.post", lambda *a, **kw: MockResponse())
    client = AgentClient(endpoint="https://test-endpoint", api_key="test-key")
    result = client.ask("Is anybody there?")
    assert "error" in result

# Not used, but for robustness...
def test_init_with_env(monkeypatch):
    monkeypatch.setenv("AZURE_CHAT_AGENT_ENDPOINT", "https://test-endpoint")
    monkeypatch.setenv("AZURE_CHAT_API_KEY", "test-key")
    client = AgentClient()
    assert client.endpoint == "https://test-endpoint"
    assert client.api_key == "test-key"