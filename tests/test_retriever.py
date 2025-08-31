import unittest
from src.knowledge_graph import build_knowledge_graph
from src.retriever import setup_query_engine

class TestRetriever(unittest.TestCase):
    def test_query(self):
        try:
            index, storage_context = build_knowledge_graph()
            self.assertIsNotNone(index, "Knowledge graph failed to initialize")
            query_engine = setup_query_engine(index, storage_context)
            self.assertIsNotNone(query_engine, "Query engine failed to initialize")
            response = query_engine.query("What is dyslexia?")
            self.assertIn("learning difference", str(response).lower(), "Unexpected response")
        except Exception as e:
            self.fail(f"Test failed: {e}")

if __name__ == "__main__":
    unittest.main()