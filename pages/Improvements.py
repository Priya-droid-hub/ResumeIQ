
import streamlit as st
import sys
import os

from theme import apply_theme


# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from analyzer.ner import extract_sections, extract_skills
from analyzer.scorer import get_total_score, score_format
from analyzer.suggester import get_improvement_report


st.set_page_config(
    page_title="Improvements",
    page_icon="✦",
    layout="wide"
)

apply_theme()


st.title("✦ Improvements")

st.markdown(
    "Actionable suggestions to improve your resume and beat the ATS."
)

st.divider()


# ── Check session state ────────────────────────────────────────────────────────
if "resume_text" not in st.session_state:

    st.warning(
        "⚠ Please upload your resume on the **Resume Analyzer** page first."
    )

    st.stop()


resume_text = st.session_state["resume_text"]


# ── Job description input ──────────────────────────────────────────────────────
st.subheader("☷ Job Description")

default_job = st.session_state.get(
    "job_text",
    ""
)

job_text = st.text_area(
    "Paste the job description you're targeting:",
    value=default_job,
    height=150,
    placeholder="Paste a job description to get tailored improvement suggestions..."
)


if not job_text.strip():

    job_text = """
    Looking for a Python developer with experience in machine learning, TensorFlow,
    data analysis, SQL, REST APIs, and cloud platforms like AWS.
    Strong communication, teamwork, and problem-solving skills required.
    Experience with Docker, Git, and Agile methodologies is a plus.
    """

    st.info(
        "Using a default sample job description. "
        "Paste your own for tailored suggestions."
    )


if st.button(
        "✦ Generate Suggestions",
        type="primary"
):

    with st.spinner(
            "Analyzing gaps and generating suggestions..."
    ):

        result_data = st.session_state.get(
            "resume_result",
            {}
        )

        sections = (
                result_data.get("sections")
                or extract_sections(resume_text)
        )

        resume_skills = (
                result_data.get("skills")
                or extract_skills(resume_text)
        )

        score_result = (
                st.session_state.get("score_result")
                or get_total_score(
            resume_text,
            job_text,
            sections,
            resume_skills
        )
        )

        format_result = score_result["format_score"]
        total_score = score_result["total_score"]

        report = get_improvement_report(
            resume_text,
            job_text,
            sections,
            resume_skills,
            format_result,
            total_score
        )


    st.divider()


    # ── Suggestions ───────────────────────────────────────────────────────────
    st.subheader("▤ Improvement Suggestions")

    if report["suggestions"]:

        for suggestion in report["suggestions"]:

            st.markdown(
                f"> {suggestion}"
            )

            st.write("")

    else:

        st.success(
            "Your resume looks great! No major improvements needed."
        )


    st.divider()


    # ── Missing Skills ────────────────────────────────────────────────────────
    st.subheader("⚙ Missing Skills")

    missing_skills = report["missing_skills"]

    if missing_skills:

        st.warning(
            f"Found **{len(missing_skills)}** skills in the job description "
            "that are missing from your resume:"
        )

        skills_html = " ".join([
            f'<span style="background:#fff3cd; color:#856404; '
            f'padding:4px 10px; border-radius:20px; margin:3px; '
            f'display:inline-block; font-size:0.85rem; font-weight:600; '
            f'border:1px solid #ffc107;">{skill}</span>'
            for skill in missing_skills
        ])

        st.markdown(
            skills_html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "Great! Your resume covers all the key skills "
            "from the job description."
        )


    st.divider()


    # ── Missing Keywords ──────────────────────────────────────────────────────
    st.subheader("⌕ Missing Keywords")

    missing_keywords = report["missing_keywords"][:20]

    if missing_keywords:

        st.info(
            "These keywords from the job description are not in your "
            "resume (top 20):"
        )

        kw_html = " ".join([
            f'<span style="background:#f8d7da; color:#721c24; '
            f'padding:4px 10px; border-radius:20px; margin:3px; '
            f'display:inline-block; font-size:0.85rem; font-weight:600; '
            f'border:1px solid #f5c6cb;">{kw}</span>'
            for kw in missing_keywords
        ])

        st.markdown(
            kw_html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "Your resume contains all the key terms "
            "from the job description."
        )


    st.divider()


    # ── Current Skills ────────────────────────────────────────────────────────
    st.subheader("✓ Skills Already in Your Resume")

    if resume_skills:

        skills_html = " ".join([
            f'<span style="background:#d4edda; color:#155724; '
            f'padding:4px 10px; border-radius:20px; margin:3px; '
            f'display:inline-block; font-size:0.85rem; font-weight:600; '
            f'border:1px solid #c3e6cb;">{skill}</span>'
            for skill in resume_skills
        ])

        st.markdown(
            skills_html,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No skills detected in your resume."
        )


    st.divider()


    # ── Quick Tips ────────────────────────────────────────────────────────────
    with st.expander("⚙ General ATS Tips"):

        st.markdown("""
        **Format Tips:**
        - Use standard section headings: Experience, Education, Skills, Projects
        - Avoid tables, columns, text boxes — ATS can't parse them
        - Save as PDF (not DOCX) when submitting online

        **Content Tips:**
        - Tailor your resume for each job — use the job's exact keywords
        - Quantify achievements: "Improved API performance by 40%"
        - Start bullet points with strong action verbs
        - Include both acronyms and full forms: "NLP (Natural Language Processing)"

        **Skills Tips:**
        - List skills explicitly in a dedicated Skills section
        - Mirror the exact terminology from the job description
        - Include tools, languages, frameworks, and methodologies separately
        """)

