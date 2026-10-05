import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
JOBS_PATH = os.path.join(ROOT, "data", "job_descriptions.json")


def load_job_descriptions() -> list:
    """
    Load all job descriptions from JSON.
    """
    with open(JOBS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_job_skills(job_description: str) -> list:
    """
    Extract known skills from the job description.

    Uses the same skill database as the resume analyzer,
    so resume and job skill extraction remain consistent.
    """
    from analyzer.ner import extract_skills

    return extract_skills(job_description)


def calculate_skill_match(resume_skills: list, job_skills: list) -> dict:
    """
    Compare resume skills against skills required by the job.
    """

    if not job_skills:
        return {
            "skill_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "job_skill_count": 0
        }

    # Normalize skills for comparison
    resume_normalized = {
        skill.strip().lower(): skill
        for skill in resume_skills
    }

    job_normalized = {
        skill.strip().lower(): skill
        for skill in job_skills
    }

    matched = []
    missing = []

    for skill_key, original_skill in job_normalized.items():

        if skill_key in resume_normalized:
            matched.append(original_skill)
        else:
            missing.append(original_skill)

    skill_score = len(matched) / len(job_skills)

    return {
        "skill_score": round(skill_score, 4),
        "matched_skills": matched,
        "missing_skills": missing,
        "job_skill_count": len(job_skills)
    }


def match_single_job(resume_text: str, job_description: str) -> dict:
    """
    Match one resume against one job.

    Combines:
    - TF-IDF similarity
    - BERT semantic similarity
    - Required skill matching
    """

    from analyzer.vectorizer import get_combined_score
    from analyzer.ner import extract_skills

    # Semantic + keyword similarity
    similarity = get_combined_score(
        resume_text,
        job_description
    )

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_job_skills(job_description)

    # Compare required skills
    skill_result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    # Semantic score
    semantic_score = similarity["combined_score"]

    # Required skill score
    skill_score = skill_result["skill_score"]

    # Final match
    #
    # 60% semantic similarity
    # 40% required skill match
    final_score = (
            (0.60 * semantic_score) +
            (0.40 * skill_score)
    )

    return {
        "tfidf_score": similarity["tfidf_score"],
        "bert_score": similarity["bert_score"],
        "semantic_score": round(semantic_score, 4),

        "skill_score": round(skill_score, 4),
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "job_skill_count": skill_result["job_skill_count"],

        "combined_score": round(final_score, 4),
        "match_percent": round(final_score * 100, 1)
    }


def match_with_all_jobs(resume_text: str) -> list:
    """
    Match the resume against every job description.
    """

    jobs = load_job_descriptions()
    results = []

    for job in jobs:

        job_description = job.get("description", "")

        scores = match_single_job(
            resume_text,
            job_description
        )

        results.append({
            "title": job.get("title", "Unknown"),
            "company": job.get("company", "Unknown"),
            "description": job_description,

            "tfidf_score": scores["tfidf_score"],
            "bert_score": scores["bert_score"],
            "semantic_score": scores["semantic_score"],

            "skill_score": scores["skill_score"],
            "matched_skills": scores["matched_skills"],
            "missing_skills": scores["missing_skills"],
            "job_skill_count": scores["job_skill_count"],

            "combined_score": scores["combined_score"],
            "match_percent": scores["match_percent"]
        })

    # Highest match first
    results.sort(
        key=lambda x: x["combined_score"],
        reverse=True
    )

    return results


def get_top_matches(resume_text: str, top_n: int = 5) -> list:
    """
    Return the top N matching jobs.
    """
    return match_with_all_jobs(resume_text)[:top_n]


if __name__ == "__main__":

    import sys

    sys.path.insert(0, ROOT)

    from analyzer.parser import extract_text_from_pdf

    pdf_path = os.path.join(
        ROOT,
        "sample_resume.pdf"
    )

    resume_text = extract_text_from_pdf(pdf_path)

    top = get_top_matches(
        resume_text,
        top_n=3
    )

    for i, job in enumerate(top, 1):

        print(
            f"\n#{i} "
            f"{job['title']} "
            f"at {job['company']}"
        )

        print(
            f"Match: "
            f"{job['match_percent']}%"
        )

        print(
            f"Semantic: "
            f"{round(job['semantic_score'] * 100, 1)}%"
        )

        print(
            f"Skill Match: "
            f"{round(job['skill_score'] * 100, 1)}%"
        )

        print(
            f"Matched Skills: "
            f"{', '.join(job['matched_skills'])}"
        )

        print(
            f"Missing Skills: "
            f"{', '.join(job['missing_skills'])}"
        )

        print()