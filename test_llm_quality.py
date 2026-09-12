"""Test LLM response quality across various healthcare queries"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database.connection import get_db_session
from services.rag_service import RAGService

test_queries = [
    "What are the symptoms of diabetes?",
    "How can I lower my blood pressure naturally?",
    "What is the difference between flu and common cold?",
    "How to prevent heart disease?",
    "What cholesterol levels are healthy?",
    "How much sleep do adults need?",
    "Which vaccines should adults get?",
    "Tips for good nutrition and healthy diet",
]

print("=" * 60)
print("HEALTHAWARE AI - LLM RESPONSE QUALITY TEST")
print("=" * 60)

for query in test_queries:
    print(f"\nQUERY: {query}")
    print("-" * 50)
    with get_db_session() as db:
        result = RAGService.process_query(
            db=db,
            query=query,
            user_id=1,
            conversation_id=None,
            language='en'
        )
    resp = result.get('response', '')
    # Print first 500 chars
    preview = resp[:500].replace('\n', ' | ')
    print(f"PREVIEW: {preview}")
    print(f"[Length: {len(resp)} chars | Sources: {len(result.get('sources', []))}]")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
