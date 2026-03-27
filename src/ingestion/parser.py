import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.logger import setup_logger

logger = setup_logger("Ingestion")

class DocumentParser:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # Purely local text splitting logic
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )

    def process_pdf(self, file_path: str) -> List:
        """Loads a PDF and returns a list of chunked documents."""
        try:
            logger.info(f"Loading PDF: {file_path}")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            logger.info(f"Splitting documents into chunks...")
            chunks = self.splitter.split_documents(documents)
            
            logger.info(f"Generated {len(chunks)} chunks from {file_path}")
            return chunks
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            return []

    def process_directory(self, data_dir: str) -> List:
        """Processes all PDFs in a directory."""
        all_chunks = []
        for filename in os.listdir(data_dir):
            if filename.endswith(".pdf"):
                file_path = os.path.join(data_dir, filename)
                all_chunks.extend(self.process_pdf(file_path))
        return all_chunks
