import re
import os


def get_missing_keywords(resume_text: str, job_text: str) -> list:
    stop_words = {
        "the", "and", "for", "with", "that", "this", "have", "will",
        "are", "you", "our", "your", "from", "they", "been", "their",
        "has", "not", "but", "what", "all", "were", "when", "we",
        "there", "can", "an", "or", "do", "if", "in", "of", "to",
        "a", "is", "as", "at", "be", "by", "on", "it", "its"
    }

    job_words = re.findall(r'\b[a-zA-Z][a-zA-Z+#.]*\b', job_text)
    job_words = [w for w in job_words if w.lower() not in stop_words and len(w) > 3]

    seen      = set()
    job_words = [w for w in job_words if not (w.lower() in seen or seen.add(w.lower()))]

    resume_lower = resume_text.lower()
    return [word for word in job_words if word.lower() not in resume_lower]


def get_missing_skills(resume_skills: list, job_text: str, all_skills: list) -> list:
    job_lower        = job_text.lower()
    resume_lower_set = {s.lower() for s in resume_skills}
    return [
        skill for skill in all_skills
        if skill.lower() in job_lower
           and skill.lower() not in resume_lower_set
    ]


def generate_suggestions(
        resume_text   : str,
        job_text      : str,
        sections      : dict,
        resume_skills : list,
        format_score  : dict,
        total_score   : int
) -> list:
    from analyzer.ner import load_skills

    suggestions = []

    important_sections = {
        "summary"   : "Add a professional Summary or Objective section at the top of your resume.",
        "experience": "Add a Work Experience section with your job history.",
        "education" : "Add an Education section with your degrees and institutions.",
        "skills"    : "Add a dedicated Skills section listing your technical and soft skills.",
        "projects"  : "Add a Projects section to showcase your practical work.",
    }

    for section, suggestion in important_sections.items():
        if not sections.get(section, False):
            suggestions.append(f"⚠️  {suggestion}")

    format_details = format_score.get("details", {})

    if not format_details.get("email", {}).get("present", True):
        suggestions.append("⚠️  Add your email address — it's missing from the resume.")

    if not format_details.get("phone", {}).get("present", True):
        suggestions.append("⚠️  Add your phone number — it's missing from the resume.")

    word_count = format_details.get("length", {}).get("word_count", 0)
    if word_count < 300:
        suggestions.append(
            f"📝  Your resume is too short ({word_count} words). "
            "Aim for 300-700 words with more detail in your experience and projects."
        )
    elif word_count > 1000:
        suggestions.append(
            f"✂️  Your resume is quite long ({word_count} words). "
            "Try to keep it concise — 1 page is ideal for most roles."
        )

    verbs_found = format_details.get("action_verbs", {}).get("found", [])
    if len(verbs_found) < 3:
        suggestions.append(
            "💡  Use more action verbs in your experience section. "
            "Examples: Developed, Built, Led, Improved, Implemented, Delivered."
        )

    all_skills     = load_skills()
    missing_skills = get_missing_skills(resume_skills, job_text, all_skills)

    if missing_skills:
        top_missing = missing_skills[:8]
        suggestions.append(
            f"🔧  Add these in-demand skills that appear in the job description: "
            f"{', '.join(top_missing)}."
        )

    has_numbers = bool(re.search(r'\d+%|\d+x|\$\d+|\d+ (users|customers|projects|teams)', resume_text))
    if not has_numbers:
        suggestions.append(
            "📊  Quantify your achievements. "
            "For example: 'Improved performance by 30%' or 'Led a team of 5 engineers'."
        )

    if total_score < 40:
        suggestions.append(
            "🚨  Your ATS score is low. Focus on adding missing sections, "
            "matching job keywords, and including relevant skills first."
        )
    elif total_score < 60:
        suggestions.append(
            "📈  Your resume is decent but needs improvement. "
            "Focus on tailoring keywords to match the job description."
        )
    elif total_score >= 80:
        suggestions.append(
            "✅  Great resume! Just make sure to tailor it slightly for each job application."
        )

    return suggestions


def get_improvement_report(
        resume_text   : str,
        job_text      : str,
        sections      : dict,
        resume_skills : list,
        format_score  : dict,
        total_score   : int
) -> dict:
    from analyzer.ner import load_skills
    all_skills = load_skills()

    return {
        "missing_keywords": get_missing_keywords(resume_text, job_text),
        "missing_skills"  : get_missing_skills(resume_skills, job_text, all_skills),
        "suggestions"     : generate_suggestions(
            resume_text, job_text, sections,
            resume_skills, format_score, total_score
        )
    }


if __name__ == "__main__":
    import sys
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT     = os.path.abspath(os.path.join(BASE_DIR, ".."))
    sys.path.insert(0, ROOT)

    from analyzer.parser import extract_text_from_pdf
    from analyzer.ner    import extract_sections, extract_skills
    from analyzer.scorer import get_total_score

    pdf_path      = os.path.join(ROOT, "sample_resume.pdf")
    resume_text   = extract_text_from_pdf(pdf_path)
    job_text      = "Python developer with machine learning, TensorFlow, Docker, AWS, REST APIs."
    sections      = extract_sections(resume_text)
    resume_skills = extract_skills(resume_text)
    score_result  = get_total_score(resume_text, job_text, sections, resume_skills)
    report        = get_improvement_report(
        resume_text, job_text, sections,
        resume_skills, score_result["format_score"], score_result["total_score"]
    )

    print("===== MISSING SKILLS =====")
    print(report["missing_skills"])
    print("\n===== SUGGESTIONS =====")
    for s in report["suggestions"]:
        print(s)