import sys
import os
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

def get_pdf_content(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    integrated_content = ""
    for page in pages:
        integrated_content += page.page_content + "\n"
    return integrated_content


if  __name__ == "__main__":

    paf_target_path = os.getenv("PDF_SAVE_PATH")
    doc_name = "example"
    doc =  paf_target_path +  f"/{doc_name}.pdf"

    text = get_pdf_content(doc)
    print(text)

