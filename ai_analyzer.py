import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text, job_description, max_retries=3):
    prompt = f"""
    You are an expert HR Manager and ATS optimizer.
    Analyze the resume against the job description and return the output ONLY in valid raw JSON format without markdown code blocks.

    JSON Structure:
    {{
        "match_score": 78,
        "summary": "Brief 2-sentence executive summary.",
        "missing_keywords": ["Keyword 1", "Keyword 2", "Keyword 3"],
        "strong_points": ["Strength 1", "Strength 2", "Strength 3"],
        "actionable_suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
    }}

    Target Job Description:
    {job_description}
    
    Candidate Resume Text:
    {resume_text}
    """

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            return json.loads(raw_text.strip())

        except Exception as e:
            # If hit by 429 Rate Limit, wait and retry automatically
            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt < max_retries - 1:
                time.sleep(10)  # Wait 10 seconds before trying again
                continue
            raise 