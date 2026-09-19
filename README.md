An AI-powered web app built with Python and Streamlit that evaluates candidate resumes against job descriptions using Google Gemini.
-File Parsing: In-memory text extraction for PDF and DOCX files.
-ATS Analytics: Generates match scores, summaries, missing keywords, and recommendations using `gemini-3.6-flash`.
-Rate-Limit Resilience: Automatic retry backoff handling for API quota limits.
-Export: One-click download for full analysis reports in JSON format.

## Tech Stack
Streamlit, Google GenAI SDK, PyMuPDF, `python-docx`

## Quickstart
```bash
# 1. Install dependencies
pip install streamlit google-genai pymupdf python-docx python-dotenv

# 2. Set environment variable in .env
GEMINI_API_KEY=your_key_here

# 3. Run application
streamlit run app.py