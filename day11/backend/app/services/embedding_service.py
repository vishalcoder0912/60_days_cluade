import json
from typing import List, Dict, Any
from loguru import logger
from app.core.config import settings


class EmbeddingService:
    """Local ChromaDB + Ollama embeddings — 100% free."""

    def __init__(self):
        self._client = None
        self._collection = None

    def _get_client(self):
        if self._client is None:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_PATH,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        return self._client

    def _get_collection(self):
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    async def _embed(self, text: str) -> List[float]:
        """Get embeddings from Ollama nomic-embed-text."""
        import httpx
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/embeddings",
                json={"model": settings.OLLAMA_EMBED_MODEL, "prompt": text},
            )
            resp.raise_for_status()
            return resp.json().get("embedding", [])

    async def store_resume(self, resume_id: str, user_id: str, text: str, metadata: Dict) -> str:
        try:
            embedding = await self._embed(text[:2000])
            collection = self._get_collection()
            doc_id = f"resume_{resume_id}"
            collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text[:2000]],
                metadatas=[{"user_id": user_id, "resume_id": resume_id, **metadata}],
            )
            return doc_id
        except Exception as e:
            logger.warning(f"ChromaDB store failed (non-critical): {e}")
            return f"resume_{resume_id}"

    async def find_similar_resumes(self, query_text: str, user_id: str, top_k: int = 5) -> List[Dict]:
        try:
            embedding = await self._embed(query_text[:2000])
            collection = self._get_collection()
            results = collection.query(
                query_embeddings=[embedding],
                n_results=min(top_k, collection.count()),
                where={"user_id": user_id},
            )
            return results.get("metadatas", [[]])[0]
        except Exception as e:
            logger.warning(f"ChromaDB query failed: {e}")
            return []


embedding_service = EmbeddingService()
