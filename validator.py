import json
from llm.groq_client import ask_groq

PROMPT = """Audit whether the candidate resume contains fabricated claims compared with the ORIGINAL.
Return ONLY JSON:
{"safe": true/false, "issues": ["..."], "safe_resume": "complete resume text"}

If unsafe, remove or rewrite unsupported claims while keeping the resume useful.
ORIGINAL:
{original}

CANDIDATE:
{candidate}

JOB:
{job}
"""

def validate_optimization(original, candidate, job, api_key, model):
    raw = ask_groq(PROMPT.format(original=original, candidate=candidate, job=job),
                   api_key, model, json_mode=True)
    return json.loads(raw)
