import streamlit as st
from core.parser import extract_resume_text
from core.jd_analyzer import analyze_job_description
from core.matcher import match_resume_to_jd
from core.optimizer import optimize_resume
from core.scorer import calculate_score
from core.validator import validate_optimization
from generators.docx_generator import create_docx
from generators.pdf_generator import create_pdf

st.set_page_config(page_title="AI Resume Optimizer", page_icon="📄", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 2.5rem; font-weight: 800;}
.sub {color:#666; font-size:1.05rem;}
.score {font-size:3rem; font-weight:800;}
.card {padding:1rem; border:1px solid #ddd; border-radius:12px; margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📄 AI Resume Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Tailor your existing resume to a specific job while protecting against fabricated claims.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Groq model", value="llama-3.3-70b-versatile")
    max_iterations = st.slider("Optimization iterations", 1, 3, 2)
    st.info("Your Groq API key is read from Streamlit Secrets. Never put it in GitHub.")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
with col2:
    jd = st.text_area("📋 Paste Complete Job Description", height=300, placeholder="Paste the full job description here...")

if st.button("🔍 Analyze & Optimize", type="primary", use_container_width=True):
    if not resume_file:
        st.error("Please upload a PDF or DOCX resume.")
        st.stop()
    if not jd.strip():
        st.error("Please paste the complete job description.")
        st.stop()

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
        st.stop()

    with st.status("Processing your resume...", expanded=True) as status:
        st.write("Extracting resume text...")
        resume_text = extract_resume_text(resume_file)

        if len(resume_text.strip()) < 100:
            st.error("Could not extract enough text. Try a text-based PDF or DOCX.")
            st.stop()

        st.write("Analyzing job description with Groq...")
        job_data = analyze_job_description(jd, api_key, model)

        st.write("Calculating initial match...")
        match_data = match_resume_to_jd(resume_text, job_data)
        initial_score = calculate_score(match_data)

        current_resume = resume_text
        optimization_history = []

        for i in range(max_iterations):
            st.write(f"AI optimization pass {i+1}/{max_iterations}...")
            candidate = optimize_resume(current_resume, job_data, match_data, api_key, model)
            validation = validate_optimization(resume_text, candidate, job_data, api_key, model)
            if not validation["safe"]:
                candidate = validation["safe_resume"]
            new_match = match_resume_to_jd(candidate, job_data)
            new_score = calculate_score(new_match)
            optimization_history.append({
                "iteration": i + 1,
                "score": new_score,
                "validation": validation
            })
            if new_score <= calculate_score(match_data):
                break
            current_resume = candidate
            match_data = new_match

        final_score = calculate_score(match_data)
        status.update(label="Optimization complete!", state="complete")

    st.session_state.result = {
        "initial_score": initial_score,
        "final_score": final_score,
        "job": job_data,
        "match": match_data,
        "resume": current_resume,
        "history": optimization_history
    }

if "result" in st.session_state:
    r = st.session_state.result
    st.divider()
    st.subheader("📊 ATS Match Analysis")

    a, b, c = st.columns(3)
    a.metric("Before", f"{r['initial_score']}/100")
    b.metric("After", f"{r['final_score']}/100", delta=f"{r['final_score']-r['initial_score']}")
    c.metric("Improvement", f"{r['final_score']-r['initial_score']} points")

    st.progress(r["final_score"] / 100)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Matched")
        for x in r["match"]["matched"]:
            st.write("•", x)
        st.markdown("### ⚠️ Partial / Weak")
        for x in r["match"]["partial"]:
            st.write("•", x)
    with col2:
        st.markdown("### ❌ Missing")
        for x in r["match"]["missing"]:
            st.write("•", x)
        st.markdown("### 📌 Job Requirements")
        st.write("**Title:**", r["job"].get("job_title", "Not detected"))
        st.write("**Experience:**", r["job"].get("experience", "Not specified"))
        st.write("**Education:**", r["job"].get("education", "Not specified"))

    st.divider()
    st.subheader("📝 Optimized Resume")
    st.text_area("Resume text", r["resume"], height=600)

    docx_bytes = create_docx(r["resume"])
    pdf_bytes = create_pdf(r["resume"])

    d1, d2 = st.columns(2)
    with d1:
        st.download_button("⬇ Download DOCX", docx_bytes, "optimized_resume.docx",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
    with d2:
        st.download_button("⬇ Download PDF", pdf_bytes, "optimized_resume.pdf",
                           "application/pdf", use_container_width=True)

    with st.expander("🔎 Optimization history"):
        for item in r["history"]:
            st.write(f"Pass {item['iteration']}: {item['score']}/100")
