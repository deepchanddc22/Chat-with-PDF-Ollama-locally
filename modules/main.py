import streamlit as st
import os
from embedding_engine import DocumentProcessor
import ollama

# Function to handle document processing and querying
class QueryProcessor:
    def __init__(self, pdf_path):
        self.processor = DocumentProcessor(pdf_path)
        self.collection = None
    
    def initialize(self):
        self.processor.extract_documents()
        self.processor.store_documents()
        self.collection = self.processor.get_collection()
    
    def query_document(self, prompt):
        response = ollama.embeddings(prompt=prompt, model="nomic-embed-text")
        results = self.collection.query(query_embeddings=[response["embedding"]], n_results=10)
        data = results['documents'][0][0]
        print(data)
        
        output = ollama.generate(
            model="gemma:2b",
            #  model="llama3",
            prompt=f" You are very kind and helful AI assistant  explain the content asked about: {prompt} from this data: {data}."
        )
        return output['response']

# Main Streamlit app
def main():
    st.title("Document Q&A will LLM")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        
        # Save the uploaded file locally
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        local_file_path = os.path.join("uploads", uploaded_file.name)
        
        # Process the uploaded PDF file
        processor = QueryProcessor(local_file_path)
        processor.initialize()
        
        # Chat interface
        st.header("Chat Interface")
        
        # Initialize conversation history
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is your question?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            response = processor.query_document(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()