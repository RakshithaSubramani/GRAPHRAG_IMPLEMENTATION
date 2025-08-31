# Dyslexia-Friendly Chatbot

A chatbot using GraphRAG to provide accessible, dyslexia-friendly responses with text-to-speech.

## Setup
1. Install Python 3.8+ and [Neo4j Community Edition](https://neo4j.com/download/).
2. Install dependencies: `pip install -r requirements.txt`
3. Add knowledge source to `data/dyslexia_faq.txt`.
4. Start Neo4j and update `src/knowledge_graph.py` with your Neo4j password.
5. Run the app: `streamlit run src/app.py`

## Requirements
- Neo4j Community Edition
- Internet for gTTS
- Optional: GPU for Hugging Face LLM or xAI API key for Grok

## Testing
Run tests: `python -m unittest tests/test_retriever.py`