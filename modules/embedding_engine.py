import ollama
import chromadb
from data_ingestion import PDFTextExtractor

class DocumentProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.documents = []
        self.collection = None

    def extract_documents(self):
        extractor = PDFTextExtractor(self.pdf_path)
        self.documents = extractor.extract_text()
        extractor.close()

    def store_documents(self):
        client = chromadb.Client()
        
        # Try to get the existing collection, or create a new one if it doesn't exist
        try:
            self.collection = client.get_collection(name="carss")
            print("Using existing collection 'carss'")
        except ValueError:
            self.collection = client.create_collection(name="carss")
            print("Created new collection 'carss'")

        # Get existing document IDs
        existing_ids = set(self.collection.get()['ids'])

        for i, d in enumerate(self.documents):
            doc_id = str(i)
            if doc_id not in existing_ids:
                response = ollama.embeddings(model="nomic-embed-text", prompt=d)
                embedding = response["embedding"]
                
                self.collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[d]
                )
                print(f"{i}: adding")
            else:
                print(f"{i}: already exists, skipping")

    def get_collection(self):
        return self.collection

