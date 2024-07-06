
# This file is just same as streamlit on it doesnt have frontend but can interact with terminal

import ollama
import chromadb
from embedding_engine import DocumentProcessor

class QueryProcessor:
    def __init__(self, pdf_path):
        self.processor = DocumentProcessor(pdf_path)
        self.collection = None

    def initialize(self):
        self.processor.extract_documents()
        self.processor.store_documents()
        self.collection = self.processor.get_collection()

    def query_loop(self):
        while True:
            prompt = input("Enter your query (or 'E' to exit): ").strip()
            
            if prompt.upper() == 'E':
                break
            
            response = self.query_document(prompt)
            print(response)
    
    def query_document(self, prompt):
        response = ollama.embeddings(prompt=prompt, model="nomic-embed-text")
        results = self.collection.query(query_embeddings=[response["embedding"]], n_results=1)
        data = results['documents'][0][0]

        output = ollama.generate(
            model="gemma:2b",
            prompt=f"Using this data: {data}. Respond to this prompt: {prompt} but if you don't find relevant answers just respond as can you please repeat your question?"
        )
        return output['response']

# Example usage
if __name__ == "__main__":
    pdf_path = "../data/file.pdf"
    query_processor = QueryProcessor(pdf_path)
    query_processor.initialize()
    query_processor.query_loop()

