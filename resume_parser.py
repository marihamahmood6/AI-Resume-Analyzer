import os
import io
import pymupdf  # PyMuPDF
from docx import Document


def extract_pdf_bytes(file_bytes):
    document = pymupdf.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text


def extract_docx_bytes(file_bytes):
    docx_file = io.BytesIO(file_bytes)
    document = Document(docx_file)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text


def extract_text_from_file(uploaded_file):
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_bytes(file_bytes)
    elif filename.endswith(".docx") or filename.endswith(".doc"):
        return extract_docx_bytes(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or Word document.")