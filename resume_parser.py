import os
import pymupdf  # Replaces 'import fitz' to remove warning
from docx import Document

def extract_pdf_text(file_path):
    document = pymupdf.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text

def extract_docx_text(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text

def extract_text(file_path):
    """Detects file extension and extracts raw text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_text(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_docx_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")