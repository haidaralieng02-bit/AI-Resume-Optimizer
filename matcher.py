import re

def norm(x):
    return re.sub(r"[^a-z0-9+#.\- ]+", " ", x.lower()).strip()

def match_resume_to_jd(resume, job):
    text = norm(resume)
    required = job.get("required_skills", []) or []
    preferred = job.get("preferred_skills", []) or []
    keywords = job.get("keywords", []) or []
    all_terms = []
    for x in required + preferred + keywords:
        if x and x not in all_terms:
            all_terms.append(x)

    matched, partial, missing = [], [], []
    for term in all_terms:
        t = norm(term)
        if not t:
            continue
        if re.search(r"\b" + re.escape(t) + r"\b", text):
            matched.append(term)
        else:
            words = [w for w in t.split() if len(w) > 2]
            hits = sum(1 for w in words if re.search(r"\b"+re.escape(w)+r"\b", text))
            if words and hits >= max(1, len(words)//2):
                partial.append(term)
            else:
                missing.append(term)

    return {
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "required_total": len(required),
        "required_matched": sum(1 for x in required if x in matched)
    }
