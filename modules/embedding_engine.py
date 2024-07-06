
# import ollama
# import chromadb
# from data_ingestion import PDFTextExtractor

# # Example usage
# pdf_path = "../data/file.pdf"
# extractor = PDFTextExtractor(pdf_path)
# extracted_documents = extractor.extract_text()
# extractor.close()


# documents = extracted_documents
# # print(documents)

# print("document extracted")
# client = chromadb.Client()
# collection = client.create_collection(name="cars")

# print("stored in DB")


# # store each document in a vector embedding database
# for i, d in enumerate(documents):
#   response = ollama.embeddings(model="nomic-embed-text", prompt=d)
#   embedding = response["embedding"]
#   print(str(i)+ "adding collection")
#   collection.add(
#     ids=[str(i)],
#     embeddings=[embedding],
#     documents=[d]

#   )

# prompt = "What is price of cybertruck"

# print("prompt read")

# # generate an embedding for the prompt and retrieve the most relevant doc
# response = ollama.embeddings(
#   prompt=prompt,
#   model="nomic-embed-text"
# )
# results = collection.query(
#   query_embeddings=[response["embedding"]],
#   n_results=1
# )
# data = results['documents'][0][0]

# print("results fetched")

# output = ollama.generate(
#   model="llama3",
#   prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
# )

# print(output['response'])



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

# # Example usage
# pdf_path = "../data/file.pdf"
# processor = DocumentProcessor(pdf_path)
# processor.extract_documents()
# processor.store_documents()
# collection = processor.get_collection()

# Now you can use `collection` in another module or part of your application
