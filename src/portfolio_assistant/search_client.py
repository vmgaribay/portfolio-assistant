"""
Client for searching documents in Azure AI Search to build response context.

"""
import logging
import requests
import re
from typing import Iterable, List, Tuple, Sequence, Optional, Dict
from portfolio_assistant.config import Config


class SearchClient:
    """
    Handle communication with Azure AI Search.
    """
    def __init__(self, endpoint: str = None, index_name: str = None,
                 api_key: str = None, api_version: str = None):
        self.endpoint = endpoint or Config.get_search_endpoint()
        self.api_key = api_key or Config.get_search_api_key()
        self.index_name = index_name or Config.get_search_index_name()
        self.api_version = api_version or Config.get_search_api_version()

        if not self.endpoint or not self.index_name or not self.api_key \
           or not self.api_version:
            raise ValueError("Azure AI Search endpoint, index name, API key, "
                             "and API version are required.")

        self._url = f"{self.endpoint}/indexes/{self.index_name}/docs/search?" \
                    f"api-version={self.api_version}"
        self._headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
        select: Optional[Sequence[str]] = None,
        filter: Optional[str] = None,
        semantic: bool = False,
        semantic_config: Optional[str] = None,
    ) -> List[Dict]:
        body: Dict = {"search": query or "*", "top": top_k}
        if select:
            body["select"] = ",".join(select)
        if filter:
            body["filter"] = filter
        if semantic:
            body["queryType"] = "semantic"
            if semantic_config:
                body["semanticConfiguration"] = semantic_config
            body["captions"] = "extractive"
            body["answers"] = "extractive"
        logging.info(f"Search request body: {body}")
        try:
            resp = requests.post(self._url, headers=self._headers,
                                 json=body, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
            values = payload.get("value", [])
            items: List[Dict] = []
            for v in values:
                d = dict(v)
                d["_score"] = v.get("@search.score")
                d["_captions"] = v.get("@search.captions", [])
                d["_answers"] = v.get("@search.answers", [])
                items.append(d)
            return items
        except requests.RequestException as e:
            logging.error(f"Search request failed: {e}")
            return []

    def build_context(
        self,
        docs: Iterable[Dict],
        content_fields: Sequence[str] = ("topics", "notes", "content"),
        max_chars: int = 80000,
    ) -> Tuple[str, List[Dict]]:
        parts: List[str] = []
        citations: List[Dict] = []
        total = 0

        sorted_results = sorted(docs, key=lambda d: d.get("_score", 0),
                                reverse=True)
        logging.info(f"Top search results: {sorted_results[:3]}")
        for i, d in enumerate(sorted_results, start=1):
            answer_text = (d.get("_answers")[0]["text"] if
                           d.get("_answers") and
                           isinstance(d.get("_answers")[0], dict) and
                           "text" in d.get("_answers")[0] else None)
            caption_text = (d.get("_captions")[0]["text"] if
                            d.get("_captions") and
                            isinstance(d.get("_captions")[0], dict) and
                            "text" in d.get("_captions")[0] else None)
            texts = [t for t in [answer_text, caption_text] if t]
            text = " | ".join(texts) if texts else self._extract_text(
                   d, content_fields) or None
            if not text:
                continue
            source = d.get("path") or ""
            clean_text = re.sub(r"\s+", " ", text).strip()
            snippet = f"Source: {source}\n{clean_text}"
            if total + len(snippet) > max_chars:
                snippet = f"{snippet[: max(0, max_chars - total)]}..."
            if not snippet:
                break
            parts.append(f"[{i}] {snippet}")
            citations.append({
                "label": i,
                "id": d.get("id") or d.get("key") or d.get("document_id"),
                "source": d.get("source") or d.get("url") or d.get("path"),
                "score": d.get("_score"),
            })
            total += len(snippet)
            if total >= max_chars:
                break
        return "\n".join(parts), citations

    @staticmethod
    def _extract_text(d: Dict, fields: Sequence[str]) -> Optional[str]:
        for f in fields:
            v = d.get(f)
            if isinstance(v, str) and v.strip():
                return v
        return None
