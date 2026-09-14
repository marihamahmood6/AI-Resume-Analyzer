from resume_parser import extract_text
from ai_analyzer import analyze_resume

# 1. Parse your test resume PDF (make sure sample_resume.pdf exists in your folder)
resume_file = "sample_resume.pdf" 
print(f"Extracting text from {resume_file}...")
resume_text = extract_text(resume_file)

# 2. Add a sample target Job Description
job_description = """
We are looking for a Python Developer experienced in AI integration, 
REST APIs, Git, PDF parsing, and natural language processing. 
The ideal candidate is proactive and familiar with LLM integrations.
"""

# 3. Analyze and print output
print("Analyzing resume with Gemini AI...\n")
results = analyze_resume(resume_text, job_description)

print("=" * 40)
print(results)
print("=" * 40)