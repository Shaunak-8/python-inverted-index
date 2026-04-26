import string
from typing import Dict, List, Tuple


class InvertedIndex:
    """
    DBMS-Oriented Inverted Index

    This implementation mimics how database indexes work internally:

    - Dictionary (term → postings list pointer)
    - Postings List (sorted by doc_id for efficient merging)
    - Document Frequency (DF) tracking for query optimization
    """

    def __init__(self):
        # Dictionary: term → postings list
        self.index: Dict[str, List[Tuple[int, int, List[int]]]] = {}
        self._trans_table = str.maketrans("", "", string.punctuation)

        # Document Frequency: term → number of documents containing term
        self.doc_freq: Dict[str, int] = {}

        # Total number of indexed documents
        self.total_docs: int = 0

    def _preprocess(self, text: str) -> List[str]:
        """
        Preprocesses text by lowercasing, removing punctuation, and tokenizing.
        """
        # Lowercase text
        text = text.lower()
        # Remove punctuation
        text = text.translate(self._trans_table)
        # Tokenize by splitting on whitespace
        tokens = text.split()
        return tokens

    def add_document(self, doc_id: int, text: str):
        """
        Adds a document to the index.

        DBMS Concept:
        This simulates inserting a record and updating secondary indexes.
        """
        tokens = self._preprocess(text)
        self.total_docs += 1

        # term → positions
        term_positions: Dict[str, List[int]] = {}

        for pos, term in enumerate(tokens):
            term_positions.setdefault(term, []).append(pos)

        for term, positions in term_positions.items():
            term_frequency = len(positions)

            if term not in self.index:
                self.index[term] = []
                self.doc_freq[term] = 0

            # Append posting
            self.index[term].append((doc_id, term_frequency, positions))

            # Update document frequency
            self.doc_freq[term] += 1

        # 🔥 IMPORTANT: Keep postings sorted (DB-style)
        for term in term_positions:
            self.index[term].sort(key=lambda x: x[0])

    def get_postings(self, term: str) -> List[Tuple[int, int, List[int]]]:
        """
        Returns postings list for a term.

        DBMS Concept:
        Equivalent to index lookup instead of full table scan.
        """
        term = term.lower()
        return self.index.get(term, [])

    def get_document_frequency(self, term: str) -> int:
        """
        Returns number of documents containing the term.
        """
        return self.doc_freq.get(term, 0)

    def get_vocabulary(self) -> List[str]:
        """
        Returns sorted vocabulary (like index keys in DB)
        """
        return sorted(self.index.keys())

    def __len__(self):
        """
        Total number of indexed documents
        """
        return self.total_docs