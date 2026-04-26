import json
import os
from typing import List, Dict, Any

from search_engine.inverted_index import InvertedIndex

class Indexer:
    """
    Indexer is responsible for reading documents from a data source 
    and systematically populating the Inverted Index.
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.index = InvertedIndex()
        
    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Loads document objects from a JSON file.
        Expects documents to have at least 'id' and 'text' keys.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at: {self.data_path}")
            
        with open(self.data_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
            
        return docs
        
    def build_index(self) -> InvertedIndex:
        """
        Loads documents, iterates over them, and delegates to the 
        InvertedIndex module to add them. 
        Returns the populated index object.
        """
        documents = self.load_documents()
        
        for doc in documents:
            doc_id = doc.get("id")
            text = doc.get("text", "")
            
            if doc_id is not None:
                self.index.add_document(doc_id, text)
                
        return self.index


if __name__ == "__main__":
    # Small example of how indexing works
    # Define paths relative to this module
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "sample_docs.json")
    
    try:
        print(f"Building reverse index based on data from '{data_file}'...")
        indexer = Indexer(data_file)
        idx = indexer.build_index()
        
        vocab = idx.get_vocabulary()
        print(f"\nVocabulary populated with {len(vocab)} unique terms.")
        
        sample_term = "search"
        print(f"\nRetrieving postings for query: '{sample_term}'")
        postings = idx.get_postings(sample_term)
        
        if postings:
            for doc_id, tf, positions in postings:
                print(f" -> Found in Document ID: {doc_id} | Term Frequency (TF): {tf} | Positions: {positions}")
        else:
            print(" -> Term not found exactly in the dataset.")
            
    except Exception as e:
        print(f"Error during indexing execution: {e}")
