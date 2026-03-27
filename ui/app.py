import streamlit as st
import base64
import os
import sys
from dotenv import load_dotenv

# --- FIX FOR CLOUD DEPLOYMENT ---
# This adds the main project folder to the "search path" so 'src' can be found.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --------------------------------

from src.ingestion.parser import DocumentParser
from src.retrieval.engine import RetrievalEngine
from src.generation.chain import RAGChain

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="NexusDocs - AI Document Assistant", layout="wide", page_icon="📄")

# Initialize Logic (Cloud-Ready)
@st.cache_resource
def init_components():
    return DocumentParser(), RetrievalEngine(), RAGChain()

parser, engine, rag = init_components()

# App UI
st.title("📄 NexusDocs: AI Document Assistant")
st.markdown("---")

# Sidebar for Uploads
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF to start chatting", type="pdf")
    
    if uploaded_file:
        if st.button("Analyze Document"):
            with st.spinner("Processing document..."):
                try:
                    # Save temporary file
                    os.makedirs("data", exist_ok=True)
                    temp_path = os.path.join("data", uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process
                    chunks = parser.process_pdf(temp_path)
                    if chunks:
                        st.session_state.active_retriever = engine.get_hybrid_retriever(chunks)
                        st.success("✅ Analysis Complete! You can now ask questions.")
                    else:
                        st.error("No text could be extracted from this PDF.")
                except Exception as e:
                    st.error(f"Error: {e}")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "engine" in m:
            st.caption(f"Engine: {m['engine']}")

# User Input
if prompt := st.chat_input("Ask me anything about your document..."):
    if "active_retriever" not in st.session_state:
        st.warning("Please upload and analyze a PDF first!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = rag.ask(st.session_state.active_retriever, prompt)
                    st.markdown(result["answer"])
                    st.caption(f"Engine: {result['engine']}")
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result["answer"],
                        "engine": result["engine"]
                    })
                except Exception as e:
                    st.error(f"An error occurred: {e}")
