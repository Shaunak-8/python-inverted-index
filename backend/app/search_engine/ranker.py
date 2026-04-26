import math
from typing import Dict, List
from collections import defaultdict

class BM25Ranker:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0.0
        self.total_docs = 0
        self.doc_lengths: Dict[str, int] = {}
        
    def calculate_idf(self, doc_freq: int) -> float:
        """
        Calculate Inverse Document Frequency (IDF) for a term.
        """
        # Smooth IDF to prevent negative values
        return math.log(1 + (self.total_docs - doc_freq + 0.5) / (doc_freq + 0.5))

    def score(self, query_terms: List[str], doc_postings: Dict[str, Dict[str, List[int]]]) -> Dict[str, float]:
        """
        Score documents based on query terms using the BM25 formula.
        Returns a mapping of document ID to score.
        """
        scores = defaultdict(float)
        
        for term in query_terms:
            postings = doc_postings.get(term, {})
            doc_freq = len(postings)
            idf = self.calculate_idf(doc_freq)
            
            for doc_id, positions in postings.items():
                term_freq = len(positions)
                doc_len = self.doc_lengths.get(doc_id, self.avg_doc_length)
                
                # BM25 term frequency normalization
                numerator = term_freq * (self.k1 + 1)
                denominator = term_freq + self.k1 * (1 - self.b + self.b * (doc_len / max(1.0, self.avg_doc_length)))
                
                scores[doc_id] += idf * (numerator / denominator)
                
        return scores
