"""Tests for search_client.py"""
import pytest
from requests import RequestException
from unittest.mock import patch, Mock
from portfolio_assistant.search_client import SearchClient


def test_init_with_args():
    client = SearchClient(endpoint="https://test-endpoint", api_key="test-key", index_name="test-index", api_version="test-version")
    assert client.endpoint == "https://test-endpoint"
    assert client.api_key == "test-key"
    assert client.index_name == "test-index"
    assert client.api_version == "test-version"

def test_init_missing_key():
    with pytest.raises(ValueError):
        SearchClient(endpoint="https://test-endpoint", api_key=None, index_name="test-index", api_version="test-version")

def test_search_request_exception(monkeypatch):
    client = SearchClient(endpoint="http://test-endpoint", index_name="test-index", api_key="test-key", api_version="test-version")
    with patch("requests.post") as mock_post:
        mock_post.side_effect = RequestException("fail")
        results = client.search("test")
        assert results == []

def test_search_valid_response():
    client = SearchClient(endpoint="http://test-endpoint", index_name="test-index", api_key="test-key", api_version="test-version")
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "value": [
            {"id": "1", "content": "test", "@search.score": 1},
            {"id": "2", "content": "test", "@search.score": 2}
        ]
    }
    with patch("requests.post", return_value=mock_response):
        results = client.search("test")
        assert len(results) == 2
        assert results[0]["id"] == "1"
        assert results[0]["_score"] == 1


def test_build_context():
    docs = [
        {"id": "1", "content": "test", "path": "/a", "_score": 1, "_answers": [{"text": "answer1"}], "_captions": [{"text": "caption1"}]},
        {"id": "2", "content": "test", "path": "/b", "_score": 2, "_captions": [{"text": "caption2"}]}
    ]
    client = SearchClient(endpoint="http://test-endpoint", index_name="test-index", api_key="test-key", api_version="test-version")
    context, citations = client.build_context(docs)
    print(context)

    assert "[2] Source: /a\nanswer1 | caption1" in context
    assert "[1] Source: /b\ncaption2" in context
    assert citations[0]["id"] == "2"
    assert citations[0]["source"] == "/b"

# weird edge cases that aren't really represented in the current index,but best to be robust
def test_extract_text_content():
    doc = {"content": "text", "title": "head"}
    assert SearchClient._extract_text(doc, ["content", "title"]) == "text"

def test_extract_text_only_option():
    doc = {"title": "head"}
    assert SearchClient._extract_text(doc, ["content", "title"]) == "head"

def test_extract_no_resource():
    doc = {}
    assert SearchClient._extract_text(doc, ["content", "title"]) is None