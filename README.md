# AI Resume Optimizer

A Streamlit + Groq application that analyzes a resume against a complete job description, calculates a transparent ATS-style match score, tailors the resume, validates against fabricated claims, and generates DOCX/PDF output.

## Features

- PDF and DOCX resume upload
- Full job-description analysis
- Required/preferred skill extraction
- Transparent ATS-style match score
- Missing/partial/matched keyword analysis
- Groq-powered resume tailoring
- Truth/fabrication protection
- Iterative optimization
- ATS-friendly DOCX and PDF downloads

## Local setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Run:

```bash
streamlit run app.py
```

## Streamlit Community Cloud

1. Push this folder to GitHub.
2. Create a Streamlit Community Cloud app from the repository.
3. Set the main file to `app.py`.
4. In App Settings / Secrets, add:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Do NOT commit `.streamlit/secrets.toml`.

## Important

The ATS score is an application-specific estimate, not a universal ATS score. Different ATS products and employers use different ranking methods.

The optimizer is instructed not to fabricate experience, credentials, dates, employers, projects, or skills.
