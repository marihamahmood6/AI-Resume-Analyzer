import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert HR Manager and ATS (Applicant Tracking System) optimizer.
    
    Target Job Description:
    {job_description}
    
    Candidate Resume Text:
    {resume_text}
    
    Please analyze the resume against the job description and provide:
    1. Overall Match Score (0-100%)
    2. Missing Keywords & Critical Skills
    3. Strong Points
    4. Actionable Suggestions for Improvement
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text