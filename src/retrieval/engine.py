import os
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from src.utils.logger import setup_logger

logger = setup_logger("Retrieval")

class RetrievalEngine:
    def __init__(self, persist_directory: str = "vector_store/faiss_index"):
        self.persist_directory = persist_directory
        # Use FREE Local Embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def create_vector_store(self, documents: List):
        """Creates and persists a FAISS vector store from documents."""
        logger.info("Creating FAISS vector store...")
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.persist_directory), exist_ok=True)
        self.vector_store.save_local(self.persist_directory)
        logger.info(f"FAISS index saved to {self.persist_directory}")
        return self.vector_store

    def get_hybrid_retriever(self, documents: List):
        """Always creates a FRESH hybrid retriever from the provided documents."""
        # Force create a new vector store every time to clear old document memory
        self.create_vector_store(documents)
        
        # Semantic Retriever (FAISS)
        vector_retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        # Keyword Retriever (BM25)
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 5
        
        # Ensemble Retriever
        ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[0.7, 0.3]
        )
        
        logger.info("System Reset: Fresh Hybrid Retriever ready for new document.")
        return ensemble_retriever

    def load_vector_store(self):
        """Loads an existing FAISS index."""
        if os.path.exists(self.persist_directory):
            try:
                self.vector_store = FAISS.load_local(
                    self.persist_directory, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Loaded existing FAISS index.")
                return self.vector_store
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
        return None
