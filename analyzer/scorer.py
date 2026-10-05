import re


# ---------------------------------------------------------
# KEYWORD SCORE
# ---------------------------------------------------------

def score_keywords(resume_text: str, job_text: str) -> dict:
    """
    Measure semantic similarity between resume and job description.

    Uses the existing TF-IDF + BERT implementation.
    """

    from analyzer.vectorizer import get_combined_score

    result = get_combined_score(
        resume_text,
        job_text
    )

    similarity = result["combined_score"]

    points = round(similarity * 35)

    return {
        "score": points,
        "max": 35,
        "tfidf_score": result["tfidf_score"],
        "bert_score": result["bert_score"],
        "similarity": similarity,
        "details": (
            f"Semantic similarity: "
            f"{round(similarity * 100, 1)}%"
        )
    }


# ---------------------------------------------------------
# SECTION SCORE
# ---------------------------------------------------------
def score_sections(sections: dict) -> dict:
    """
    Score important resume sections.

    Total = 25 points.
    """

    section_weights = {
        "experience": 7,
        "education": 6,
        "skills": 5,
        "projects": 3,
        "summary": 2,
        "achievements": 2
    }

    details = {}
    total = 0

    for section, weight in section_weights.items():

        present = sections.get(
            section,
            False
        )

        earned = weight if present else 0

        total += earned

        details[section] = {
            "present": present,
            "points": earned,
            "max": weight
        }

    return {
        "score": total,
        "max": 25,
        "details": details
    }
# ---------------------------------------------------------
# FORMAT SCORE
# ---------------------------------------------------------

def score_format(resume_text: str) -> dict:
    """
    Check basic resume formatting signals.

    Total = 20 points.
    """

    details = {}
    total = 0

    text_lower = resume_text.lower()

    # -------------------------
    # EMAIL
    # -------------------------

    email_pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+\."
        r"[a-zA-Z]{2,}"
    )

    has_email = bool(
        re.search(
            email_pattern,
            resume_text
        )
    )

    email_points = 5 if has_email else 0

    total += email_points

    details["email"] = {
        "present": has_email,
        "points": email_points,
        "max": 5
    }

    # -------------------------
    # PHONE
    # -------------------------

    phone_pattern = (
        r"(?:\+91[\s-]?)?"
        r"[6-9]\d{9}"
    )

    has_phone = bool(
        re.search(
            phone_pattern,
            resume_text
        )
    )

    phone_points = 5 if has_phone else 0

    total += phone_points

    details["phone"] = {
        "present": has_phone,
        "points": phone_points,
        "max": 5
    }

    # -------------------------
    # RESUME LENGTH
    # -------------------------

    word_count = len(
        resume_text.split()
    )

    good_length = (
            300 <= word_count <= 1000
    )

    if good_length:
        length_points = 5

    elif word_count >= 150:
        length_points = 3

    else:
        length_points = 0

    total += length_points

    details["length"] = {
        "word_count": word_count,
        "ideal": good_length,
        "points": length_points,
        "max": 5
    }

    # -------------------------
    # ACTION VERBS
    # -------------------------

    action_verbs = [
        "developed",
        "built",
        "designed",
        "implemented",
        "led",
        "managed",
        "created",
        "improved",
        "increased",
        "reduced",
        "launched",
        "delivered",
        "collaborated",
        "architected",
        "optimized",
        "automated",
        "deployed",
        "analyzed",
        "researched",
        "trained",
        "mentored",
        "streamlined"
    ]

    # Use word boundaries instead of substring matching
    verbs_found = []

    for verb in action_verbs:

        pattern = (
                r"\b"
                + re.escape(verb)
                + r"\b"
        )

        if re.search(
                pattern,
                text_lower
        ):
            verbs_found.append(verb)

    if len(verbs_found) >= 3:
        verb_points = 5

    elif len(verbs_found) >= 1:
        verb_points = 3

    else:
        verb_points = 0

    total += verb_points

    details["action_verbs"] = {
        "found": verbs_found,
        "count": len(verbs_found),
        "points": verb_points,
        "max": 5
    }

    return {
        "score": total,
        "max": 20,
        "details": details
    }


# ---------------------------------------------------------
# SKILL SCORE
# ---------------------------------------------------------

def score_skills(
        resume_skills: list,
        job_text: str
) -> dict:
    """
    Compare resume skills against skills required
    by the job.

    IMPORTANT:
    The denominator is JOB skills, not resume skills.

    Example:

    Job requires:
        Java
        Spring Boot
        Docker
        AWS

    Resume has:
        Java
        Docker
        AWS

    Result:
        3 / 4 = 75%
    """

    from analyzer.ner import extract_skills

    # Extract skills from job description
    job_skills = extract_skills(
        job_text
    )

    # No skills found in job description
    if not job_skills:

        return {
            "score": 0,
            "max": 20,
            "matched_skills": [],
            "missing_skills": [],
            "job_skills": [],
            "details": (
                "No recognizable skills "
                "were found in the job description."
            )
        }

    # Normalize resume skills
    resume_skill_map = {
        skill.lower().strip(): skill
        for skill in resume_skills
    }

    matched_skills = []
    missing_skills = []

    for job_skill in job_skills:

        normalized = (
            job_skill.lower().strip()
        )

        if normalized in resume_skill_map:

            matched_skills.append(
                job_skill
            )

        else:

            missing_skills.append(
                job_skill
            )

    # Calculate percentage
    match_ratio = (
            len(matched_skills)
            / len(job_skills)
    )

    points = round(
        match_ratio * 20
    )

    return {
        "score": points,
        "max": 20,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "job_skills": job_skills,
        "match_ratio": round(
            match_ratio,
            4
        ),
        "details": (
            f"{len(matched_skills)} of "
            f"{len(job_skills)} required "
            f"job skills found in resume"
        )
    }


# ---------------------------------------------------------
# TOTAL ATS SCORE
# ---------------------------------------------------------

def get_total_score(
        resume_text: str,
        job_text: str,
        sections: dict,
        resume_skills: list
) -> dict:
    """
    Calculate complete ATS-style score.

    Total = 100 points.

    Keyword / Semantic Similarity = 35
    Sections                     = 25
    Formatting                   = 20
    Required Skills              = 20
    """

    # -------------------------
    # 1. KEYWORD / SEMANTIC
    # -------------------------

    keyword_result = score_keywords(
        resume_text,
        job_text
    )

    # -------------------------
    # 2. SECTIONS
    # -------------------------

    section_result = score_sections(
        sections
    )

    # -------------------------
    # 3. FORMAT
    # -------------------------

    format_result = score_format(
        resume_text
    )

    # -------------------------
    # 4. REQUIRED SKILLS
    # -------------------------

    skills_result = score_skills(
        resume_skills,
        job_text
    )

    # -------------------------
    # FINAL SCORE
    # -------------------------

    total = (
            keyword_result["score"]
            + section_result["score"]
            + format_result["score"]
            + skills_result["score"]
    )

    # -------------------------
    # GRADE
    # -------------------------

    if total >= 85:

        grade = "Excellent"

    elif total >= 70:

        grade = "Good"

    elif total >= 50:

        grade = "Fair"

    else:

        grade = "Needs Improvement"

    return {
        "total_score": total,
        "grade": grade,

        "keyword_score": keyword_result,

        "section_score": section_result,

        "format_score": format_result,

        "skills_score": skills_result
    }