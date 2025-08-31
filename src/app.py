import streamlit as st
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.knowledge_graph import build_knowledge_graph
from src.retriever import setup_query_engine
from src.text_to_speech import text_to_speech

# Page config
st.set_page_config(page_title="Dyslexia-Friendly Chatbot", layout="wide")

# Dyslexia-friendly CSS
st.markdown("""
    <style>
    .stApp { font-family: Arial, sans-serif; background-color: #f5f5f5; color: #000; }
    .stTextInput > div > input { font-size: 18px; padding: 10px; }
    .stButton > button { background-color: #4CAF50; color: white; font-size: 16px; }
    .stMarkdown { font-size: 18px; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

st.title("Dyslexia-Friendly Chatbot")

# Cache init
@st.cache_resource
def init_graph_and_engine():
    index, storage_context = build_knowledge_graph()
    query_engine = setup_query_engine(index, storage_context)
    return query_engine

query_engine = init_graph_and_engine()
if not query_engine:
    st.error("Failed to initialize query engine. Check your Neo4j/LLM setup.")
    st.stop()

# Chat input
user_input = st.text_input("Ask a question:", placeholder="E.g., What is dyslexia?")
if user_input:
    try:
        response = query_engine.query(user_input)
        st.write("**Answer**: " + str(response))

        # Audio
        audio_file = text_to_speech(str(response))
        if audio_file:
            st.audio(audio_file)
        else:
            st.warning("Could not generate audio.")
    except Exception as e:
        st.error(f"Error processing query: {e}")
