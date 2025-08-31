from llama_index.core.retrievers import KnowledgeGraphRAGRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.base.llms import CustomLLM
from llama_index.core import PromptTemplate
from typing import Any
from litellm import completion
import os
from dotenv import load_dotenv
import logging

class LiteLLM(CustomLLM):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def complete(self, prompt: str, **kwargs: Any) -> str:
        try:
            response = completion(
                model="xai/grok-beta",
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"LiteLLM error: {e}")
            return "Sorry, I couldn’t generate an answer right now."

    async def acomplete(self, prompt: str, **kwargs: Any) -> str:
        return self.complete(prompt, **kwargs)

    def stream_complete(self, prompt: str, **kwargs: Any) -> Any:
        raise NotImplementedError("Streaming not supported yet")

    def metadata(self) -> dict:
        return {"model": "xai/grok-beta"}

def setup_query_engine(index, storage_context):
    try:
        load_dotenv()
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY not found in .env file")

        # Initialize LiteLLM
        llm = LiteLLM(api_key=api_key)

        # Set up retriever
        retriever = KnowledgeGraphRAGRetriever(
            index=index,
            storage_context=storage_context,
            llm=llm,
            verbose=True
        )

        # Dyslexia-friendly template
        prompt = PromptTemplate("Answer in short, clear sentences using simple words. Avoid jargon.")

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            text_qa_template=prompt
        )

        return query_engine
    except Exception as e:
        logging.error(f"Error setting up query engine: {e}")
        return None
