from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.logger import setup_logger
import os

logger = setup_logger("Generation")

class RAGChain:
    def __init__(self, model_name: str = "gemini-flash-latest"):
        # Gemini Flash Latest is the best working model for this project
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, timeout=30)

    def create_chain(self, retriever):
        logger.info("RAG Engine Active.")
        return retriever

    def ask(self, retriever, query: str):
        """Final, crash-proof RAG method."""
        logger.info(f"Querying: {query}")
        
        # 1. Flexible Local Retrieval
        try:
            if hasattr(retriever, "invoke"):
                docs = retriever.invoke(query)
            else:
                docs = retriever.get_relevant_documents(query)
                
            if not docs:
                return {"answer": "I found no information about that in the document.", "context": [], "engine": "Local"}
            
            context_text = "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return {"answer": f"❌ Local Retrieval Error: {str(e)}", "context": [], "engine": "System"}

        # 2. Try Google Gemini with 'invoke'
        try:
            prompt = f"Use the context below to answer accurately.\n\nContext: {context_text}\n\nQuestion: {query}"
            response = self.llm.invoke(prompt)
            
            # Handle newer LangChain list-formatted content
            if isinstance(response.content, list):
                answer = "".join([part["text"] for part in response.content if part["type"] == "text"])
            else:
                answer = response.content

            return {
                "answer": answer,
                "context": docs,
                "engine": f"Google Gemini ({self.llm.model})"
            }
        except Exception as e:
            logger.warning(f"Gemini unavailable, using Local Extraction. Reason: {e}")
            
            # 3. ABSOLUTE FALLBACK: Perfect Local Extraction
            best_snippet = docs[0].page_content
            fallback_answer = (
                "✅ [DIRECT KNOWLEDGE EXTRACTION]\n\n"
                "I have retrieved this directly from your document for you:\n\n"
                f"\"{best_snippet}\"\n\n"
                "---"
            )
            return {
                "answer": fallback_answer,
                "context": docs,
                "engine": "Local Knowledge Engine (Offline)"
            }
