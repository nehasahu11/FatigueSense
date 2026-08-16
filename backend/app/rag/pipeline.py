from typing import Any, Dict, List, Optional

from backend.app.rag.loaders.document_loader import load_documents
from backend.app.rag.preprocessing.document_preprocessor import preprocess_document
from backend.app.rag.chunking.fixed_chunking import fixed_chunk
from backend.app.rag.chunking.recursive_chunking import recursive_chunk
from backend.app.rag.chunking.sentence_window_chunking import sentence_window_chunk
from backend.app.rag.chunking.chunk_comparison import compare_chunks
from backend.app.rag.chunking.chunk_selector import select_chunking_strategy
from backend.app.rag.vector_store.vector_manager import VectorManager
from backend.app.rag.retrieval.retrieval_pipeline import RetrievalPipeline


class RAGPipeline:
    """
    End-to-end RAG pipeline.

    Ingestion:
        Documents
            ↓
        Preprocessing
            ↓
        Chunking
            ↓
        Embeddings
            ↓
        ChromaDB

    Retrieval:
        Query
            ↓
        Hybrid Search
            ↓
        Cross-Encoder Reranker
            ↓
        Final Results
    """

    def __init__(
        self,
        vector_manager: Optional[VectorManager] = None,
    ):
        self.vector_manager = vector_manager or VectorManager()

        self.retrieval_pipeline = RetrievalPipeline(
            vector_manager=self.vector_manager
        )

    def ingest_documents(
        self,
        directory: str,
        preferred_strategy: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Load, preprocess, chunk, and index documents.
        """

        documents = load_documents(directory)

        if not documents:
            return {
                "documents_processed": 0,
                "chunks_indexed": 0,
                "strategy": None,
            }

        total_chunks = 0
        selected_strategy = None

        for document in documents:
            processed = preprocess_document(document)

            text = processed["text"]
            metadata = processed["metadata"]

            fixed_chunks = fixed_chunk(text)
            recursive_chunks = recursive_chunk(text)
            sentence_chunks = sentence_window_chunk(text)

            comparison = compare_chunks(
                fixed_chunks,
                recursive_chunks,
                sentence_chunks,
            )

            chunks_by_strategy = {
                "fixed": fixed_chunks,
                "recursive": recursive_chunks,
                "sentence_window": sentence_chunks,
            }

            strategy = select_chunking_strategy(
                comparison,
                preferred_strategy=preferred_strategy,
            )

            selected_strategy = strategy

            selected_chunks = chunks_by_strategy[strategy]

            if not selected_chunks:
                continue

            chunk_texts: List[str] = []
            chunk_metadatas: List[Dict[str, Any]] = []

            for index, chunk in enumerate(selected_chunks):
                chunk_texts.append(chunk)

                chunk_metadata = dict(metadata)
                chunk_metadata["chunk_index"] = index
                chunk_metadata["chunking_strategy"] = strategy

                chunk_metadatas.append(chunk_metadata)

            self.vector_manager.add_chunks(
                chunks=chunk_texts,
                metadatas=chunk_metadatas,
            )

            total_chunks += len(chunk_texts)

        return {
            "documents_processed": len(documents),
            "chunks_indexed": total_chunks,
            "strategy": selected_strategy,
            "total_indexed_chunks": self.vector_manager.count(),
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve the most relevant chunks for a query.
        """

        return self.retrieval_pipeline.search(
            query=query,
            top_k=top_k,
            candidate_k=candidate_k,
        )

    def count(self) -> int:
        """
        Return the number of indexed chunks.
        """

        return self.vector_manager.count()