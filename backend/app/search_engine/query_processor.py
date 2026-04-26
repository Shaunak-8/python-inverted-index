from typing import List
from search_engine.inverted_index import InvertedIndex

class QueryProcessor:
    """
    QueryProcessor Module for Inverted Index
    
    How this simulates DBMS Query Execution:
    In a standard database system (DBMS), when you query involving multiple conditions 
    e.g., SELECT * FROM docs WHERE text LIKE '%database%' AND text LIKE '%indexing%'
    without an index, the DBMS must do a Full Table Scan (check every term in every doc).
    
    With an inverted index (similar to B-Tree indexes in SQL), the DBMS does an index lookup
    to fetch the list of matching record IDs for each condition. For multiple conditions (AND, OR, NOT),
    the DBMS performs a "Merge Join" on the sorted record ID lists instead of scanning the table.
    
    Why sorted postings lists enable efficient merging:
    Because the document IDs are sorted, we can use two pointers to traverse both lists
    simultaneously in O(N + M) time, where N and M are the lengths of the two lists.
    We avoid O(N * M) nested loops and we avoid bringing all document data into memory!
    """
    def __init__(self, index: InvertedIndex):
        self.index = index
        
    def _intersect(self, list1: List[int], list2: List[int]) -> List[int]:
        """
        Merge-based intersection (AND operation).
        Traverses two sorted lists using pointers.
        """
        i, j = 0, 0
        result = []
        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i])
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                i += 1
            else:
                j += 1
        return result
        
    def _union(self, list1: List[int], list2: List[int]) -> List[int]:
        """
        Merge-based union (OR operation).
        Traverses two sorted lists avoiding duplicates.
        """
        i, j = 0, 0
        result = []
        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i])
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                result.append(list1[i])
                i += 1
            else:
                result.append(list2[j])
                j += 1
                
        # Append remaining elements
        while i < len(list1):
            result.append(list1[i])
            i += 1
        while j < len(list2):
            result.append(list2[j])
            j += 1
            
        return result
        
    def _difference(self, list1: List[int], list2: List[int]) -> List[int]:
        """
        Merge-based difference (NOT operation).
        Returns documents in list1 that are NOT in list2.
        """
        i, j = 0, 0
        result = []
        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                result.append(list1[i])
                i += 1
            else:
                j += 1
                
        # Append any remaining elements in list1
        while i < len(list1):
            result.append(list1[i])
            i += 1
            
        return result
        
    def process_query(self, query: str) -> List[int]:
        """
        Parses a simple query and routes it to the correct merge algorithm.
        Supports: "term", "term1 AND term2", "term1 OR term2", "term1 NOT term2"
        """
        tokens = query.strip().split()
        
        def get_doc_ids(term: str) -> List[int]:
            # Extract only the doc_id (index 0) from the form (doc_id, tf, positions)
            return [posting[0] for posting in self.index.get_postings(term)]
            
        if len(tokens) == 1:
            return get_doc_ids(tokens[0])
            
        elif len(tokens) == 3:
            term1, op, term2 = tokens[0], tokens[1].upper(), tokens[2]
            list1 = get_doc_ids(term1)
            list2 = get_doc_ids(term2)
            
            if op == "AND":
                return self._intersect(list1, list2)
            elif op == "OR":
                return self._union(list1, list2)
            elif op == "NOT":
                return self._difference(list1, list2)
            else:
                raise ValueError(f"Unsupported operator: {op}")
        else:
            raise ValueError("Query format must be 'term' or 'term1 OP term2'")


if __name__ == "__main__":
    from search_engine.indexer import Indexer
    import os
    
    # Resolve the path to the sample_docs.json natively
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "sample_docs.json")
    
    print(f"Building index from {data_file}...")
    try:
        indexer = Indexer(data_file)
        index = indexer.build_index()
        
        processor = QueryProcessor(index)
        
        # Test queries per requirements
        queries = [
            "database",
            "database AND indexing",
            "database OR search",
            "database NOT indexing"
        ]
        
        print("\nExecuting Queries:")
        print("-" * 40)
        for q in queries:
            results = processor.process_query(q)
            print(f"Query: '{q}'\nResults (Doc IDs): {results}\n")
            
    except Exception as e:
        print(f"Error during query execution: {e}")
