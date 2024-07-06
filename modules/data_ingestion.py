# import fitz  # PyMuPDF

# class PDFTextExtractor:
#     def __init__(self, pdf_path):
#         self.pdf_path = pdf_path
#         self.document = fitz.open(pdf_path)
#         self.text = ""

#     def extract_text(self):
#         for page_num in range(self.document.page_count):
#             page = self.document.load_page(page_num)
#             self.text += page.get_text()
#         return self.text

#     def close(self):
#         self.document.close()

# # # Example usage
# pdf_path = "../data/file.pdf"
# extractor = PDFTextExtractor(pdf_path)
# extracted_text = extractor.extract_text()
# extractor.close()

# # # The extracted text can now be used in another module
# print(extracted_text)

import fitz  # PyMuPDF

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.document = fitz.open(pdf_path)
        self.documents = []

    def extract_text(self):
        for page_num in range(self.document.page_count):
            page = self.document.load_page(page_num)
            page_text = page.get_text()
            # Clean up the text: remove extra spaces, newlines, etc., if needed
            cleaned_text = " ".join(page_text.split())
            self.documents.append(cleaned_text)
        return self.documents

    def close(self):
        self.document.close()

# Example usage

# print(extracted_documents)
# Print the formatted list
# print("documents = [")
# for doc in extracted_documents:
#     print(f"'''{doc}''',")
# print("]")
