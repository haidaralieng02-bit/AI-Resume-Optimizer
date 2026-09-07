def calculate_score(match):
    total = match.get("required_total", 0)
    req = match.get("required_matched", 0)
    required_score = (req / total * 100) if total else 50
    all_terms = len(match.get("matched", [])) + len(match.get("partial", [])) + len(match.get("missing", []))
    keyword_score = (len(match.get("matched", [])) / all_terms * 100) if all_terms else 50
    partial_bonus = (len(match.get("partial", [])) / all_terms * 20) if all_terms else 0
    return max(0, min(100, round(required_score * 0.65 + keyword_score * 0.25 + partial_bonus * 0.10)))
