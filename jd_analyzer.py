import json
from llm.groq_client import ask_groq

PROMPT = """Analyze the following job description. Return ONLY valid JSON with:
job_title, experience, education, certifications, required_skills, preferred_skills,
responsibilities, keywords. Arrays must contain strings. Do not invent requirements.

JOB DESCRIPTION:
{jd}
"""

def analyze_job_description(jd, api_key, model):
    raw = ask_groq(PROMPT.format(jd=jd), api_key, model, json_mode=True)
    return json.loads(raw)
