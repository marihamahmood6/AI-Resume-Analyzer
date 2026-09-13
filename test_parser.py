from resume_parser import extract_pdf_text


file_path = "sample_resume.pdf"

text = extract_pdf_text(file_path)

print(text)