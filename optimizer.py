from llm.groq_client import ask_groq

PROMPT = """You are an expert resume writer. Tailor the ORIGINAL resume to the JOB REQUIREMENTS.

Rules:
1. Never invent employers, dates, degrees, certifications, projects, tools, achievements, metrics, or years of experience.
2. Never claim a skill merely because it appears in the job description.
3. You may rewrite existing truthful experience, reorder sections, improve wording, and emphasize evidence already present.
4. Add a keyword only when the original resume provides reasonable evidence for it.
5. Keep the resume ATS-friendly: standard headings, simple text, no tables, no icons, no graphics.
6. Preserve all important truthful information from the original resume.
7. Return ONLY the complete optimized resume text.

JOB REQUIREMENTS:
{job}

MATCH ANALYSIS:
{match}

ORIGINAL RESUME:
{resume}
"""

def optimize_resume(resume, job, match, api_key, model):
    return ask_groq(PROMPT.format(job=job, match=match, resume=resume), api_key, model)
