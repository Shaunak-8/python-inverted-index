import time
import os
import sys
import string

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_engine.inverted_index import InvertedIndex
from search_engine.query_processor import QueryProcessor


# 🔴 Toggle this
USE_DB = False  # True → use MySQL, False → use synthetic data


def generate_synthetic_documents(num_docs: int) -> list:
    """
    Generates synthetic documents to simulate large-scale database.
    """
    documents = []
    base_texts = [
        "A search engine is a software system designed to carry out web searches.",
        "Search engine optimization significantly improves web visibility.",
        "The index mapping term positions helps the search process perform at high speed.",
        "Unlike full scan queries, advanced database systems use a specialized B-Tree index.",
        "Data structures like hash tables and trees are fundamental to computer science.",
        "Information retrieval systems process queries against a large collection of documents.",
        "Machine learning algorithms can enhance the ranking of search results."
    ]

    for i in range(1, num_docs + 1):
        text = base_texts[i % len(base_texts)]
        documents.append({"id": i, "text": text})

    # Inject controlled matches
    for i in range(min(100, len(documents)), min(200, len(documents))):
        documents[i]["text"] += " We need a strong database indexing implementation."

    return documents


def naive_search(query: str, documents: list) -> list:
    """
    Simulates Full Table Scan.
    Equivalent to: SELECT * WHERE content LIKE '%term%'
    """
    doc_ids = []

    query_tokens = [t.lower() for t in query.strip().split() if t.upper() != "AND"]
    trans_table = str.maketrans("", "", string.punctuation)

    for doc in documents:
        text = doc["text"].lower()
        text = text.translate(trans_table)
        tokens = set(text.split())

        if all(token in tokens for token in query_tokens):
            doc_ids.append(doc["id"])

    return doc_ids


def run_benchmark(query: str, documents: list, processor: QueryProcessor):
    """
    Compare naive vs indexed search
    """
    print("=" * 50)
    print(f"Query: \"{query}\"")

    print("\n[DBMS ANALOGY]")
    print("Naive Search → Full Table Scan (LIKE '%term%')")
    print("Indexed Search → Using Inverted Index\n")

    print("Naive: O(N)")
    print("Indexed: O(1) lookup + O(M) merge\n")

    # Naive
    start = time.perf_counter()
    naive_results = naive_search(query, documents)
    naive_time = (time.perf_counter() - start) * 1000

    # Indexed
    start = time.perf_counter()
    indexed_results = processor.process_query(query)
    indexed_time = (time.perf_counter() - start) * 1000

    # Validate correctness
    assert set(naive_results) == set(indexed_results), "Mismatch in results!"

    print(f"Naive Search Time: {naive_time:.4f} ms")
    print(f"Indexed Search Time: {indexed_time:.4f} ms")

    if indexed_time > 0:
        print(f"Speedup: {naive_time / indexed_time:.1f}x")
    else:
        print("Speedup: extremely high")

    print(f"Documents found: {len(indexed_results)}\n")


if __name__ == "__main__":
    print("\n=== SEARCH ENGINE BENCHMARK ===\n")

    # 🟢 Mode Selection
    if USE_DB:
        print("Using MySQL dataset (small-scale demo)\n")
        from db.fetch_documents import fetch_documents
        documents = fetch_documents()
    else:
        num_docs = 20000
        print(f"Using synthetic dataset ({num_docs:,} documents)\n")
        documents = generate_synthetic_documents(num_docs)

    # Build Index
    print("Building Inverted Index...\n")
    index = InvertedIndex()

    for doc in documents:
        index.add_document(doc["id"], doc["text"])

    processor = QueryProcessor(index)

    print("=" * 50)
    print("       PERFORMANCE RESULTS")
    print("=" * 50 + "\n")

    # Run tests
    run_benchmark("database", documents, processor)
    run_benchmark("database AND indexing", documents, processor)
    run_benchmark("search", documents, processor)
    query = "database AND indexing"
    results = processor.process_query(query)

    query = "database AND indexing"
results = processor.process_query(query)

print("\n=== SEARCH RESULTS ===")
print(f"Query: {query}\n")

count = 0
for doc in documents:
    if doc["id"] in results:
        print(f"Doc {doc['id']}: {doc['text']}")
        count += 1
        if count == 5:
            break

print(f"\n...and {len(results) - 5} more results")