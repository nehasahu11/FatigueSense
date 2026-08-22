from typing import Any, Dict, Optional

from backend.app.rag.retrieval.hybrid_search import HybridSearch
from backend.app.rag.retrieval.reranker import Reranker
from backend.app.rag.vector_store.vector_manager import VectorManager


class RetrievalPipeline:
    """
    Complete retrieval pipeline:

    Query
        ↓
    Hybrid Search
        ↓
    Cross-Encoder Reranker
        ↓
    Final Ranked Results
    """

    def __init__(
        self,
        vector_manager: Optional[VectorManager] = None,
        semantic_weight: float = 0.6,
        bm25_weight: float = 0.4,
        reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        """
        Initialize the retrieval pipeline.

        Args:
            vector_manager: Optional shared VectorManager instance.
            semantic_weight: Weight for semantic search.
            bm25_weight: Weight for BM25 search.
            reranker_model: Cross-encoder model used for reranking.
        """

        self.vector_manager = vector_manager or VectorManager()

        self.hybrid_search = HybridSearch(
            vector_manager=self.vector_manager,
            semantic_weight=semantic_weight,
            bm25_weight=bm25_weight,
        )

        self.reranker = Reranker(
            model_name=reranker_model
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Perform hybrid retrieval followed by reranking.

        Args:
            query: User's search query.
            top_k: Number of final results.
            candidate_k: Number of candidates retrieved before reranking.

        Returns:
            Final reranked retrieval results.
        """

        if not query or not query.strip():
            return {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "scores": [],
            }

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        if candidate_k is None:
            candidate_k = max(top_k * 3, 10)

        if candidate_k < top_k:
            candidate_k = top_k

        # ---------------------------------------------------------
        # Step 1: Hybrid Search
        # ---------------------------------------------------------

        hybrid_results = self.hybrid_search.search(
            query=query,
            top_k=candidate_k,
        )

        if not hybrid_results.get("documents"):
            return {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "scores": [],
            }

        # ---------------------------------------------------------
        # Step 2: Reranking
        # ---------------------------------------------------------

        reranked_results = self.reranker.rerank_results(
            query=query,
            results=hybrid_results,
            top_k=top_k,
        )

        return reranked_results

    def count(self) -> int:
        """
        Return the number of indexed documents.
        """

        return self.vector_manager.count()