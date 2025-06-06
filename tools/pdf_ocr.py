import re
import pytesseract
from pdf2image import convert_from_path
from llama_index.core.schema import Document

def needs_ocr(text):
    return len(re.findall(r"[A-Za-z0-9]", text)) < 30

def run_ocr_on_file(file_path):
    pages = convert_from_path(file_path, 600)

    documents = []
    page_number = 1
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_document = Document(text=text, metadata={"source": file_path, "page_label": str(page_number)})
        documents.append(text_document)
        page_number += 1
    
    return documents

# if __name__ == "__main__":
#     file_path = "data/FLsample.pdf"
#     run_ocr_on_file(file_path)