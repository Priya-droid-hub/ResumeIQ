
import streamlit as st
import sys
import os

from theme import apply_theme


# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from analyzer.ner import extract_sections, extract_skills
from analyzer.scorer import get_total_score


st.set_page_config(
    page_title="ATS Scorer",
    page_icon="◎",
    layout="wide"
)

apply_theme()


st.title("◎ ATS Scorer")

st.markdown(
    "See how well your resume scores against an ATS system — "
    "broken down by category."
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

# Pre-fill if coming from Job Matcher page
default_job = st.session_state.get("job_text", "")

job_text = st.text_area(
    "Paste a job description to score against (or use the default sample):",
    value=default_job,
    height=150,
    placeholder="Paste a job description here for accurate ATS scoring..."
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
        "Paste your own above for better results."
    )


if st.button(
        "▦ Calculate ATS Score",
        type="primary"
):

    with st.spinner(
            "Calculating ATS score..."
    ):

        result_data = st.session_state.get(
            "resume_result",
            {}
        )

        sections = (
                result_data.get("sections")
                or extract_sections(resume_text)
        )

        skills = (
                result_data.get("skills")
                or extract_skills(resume_text)
        )

        score = get_total_score(
            resume_text,
            job_text,
            sections,
            skills
        )


    # Save for improvements page
    st.session_state["job_text"] = job_text
    st.session_state["score_result"] = score

    st.divider()


    # ── Total Score ───────────────────────────────────────────────────────────
    total = score["total_score"]
    grade = score["grade"]

    if grade == "Excellent":
        grade_color = "#28a745"
        grade_symbol = "✓"

    elif grade == "Good":
        grade_color = "#1f77b4"
        grade_symbol = "✓"

    elif grade == "Fair":
        grade_color = "#ffc107"
        grade_symbol = "!"

    else:
        grade_color = "#dc3545"
        grade_symbol = "×"


    col1, col2 = st.columns([2, 1])


    with col1:

        st.subheader("Overall ATS Score")

        st.progress(
            total / 100
        )

        st.markdown(
            f"<h1 style='color:{grade_color}; font-size:3rem;'>"
            f"{total} / 100"
            f"</h1>",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f'<div style="background:{grade_color}; color:white; '
            f'border-radius:12px; padding:2rem; text-align:center; '
            f'margin-top:1rem;">'
            f'<div style="font-size:2.5rem;">{grade_symbol}</div>'
            f'<div style="font-size:1.8rem; font-weight:800;">{grade}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


    st.divider()


    # ── Score Breakdown ───────────────────────────────────────────────────────
    st.subheader("Score Breakdown")

    col1, col2, col3, col4 = st.columns(4)

    kw = score["keyword_score"]
    sec = score["section_score"]
    fmt = score["format_score"]
    sk = score["skills_score"]


    with col1:

        st.metric(
            "Keywords",
            f"{kw['score']} / {kw['max']}"
        )

        st.progress(
            kw["score"] / kw["max"]
        )

        st.caption(
            kw["details"]
        )


    with col2:

        st.metric(
            "Sections",
            f"{sec['score']} / {sec['max']}"
        )

        st.progress(
            sec["score"] / sec["max"]
        )


    with col3:

        st.metric(
            "Format",
            f"{fmt['score']} / {fmt['max']}"
        )

        st.progress(
            fmt["score"] / fmt["max"]
        )


    with col4:

        st.metric(
            "Skills",
            f"{sk['score']} / {sk['max']}"
        )

        st.progress(
            sk["score"] / sk["max"]
        )

        st.caption(
            sk.get("details", "")
        )


    st.divider()


    # ── Section Details ───────────────────────────────────────────────────────
    st.subheader("☷ Section Details")

    sec_details = sec.get(
        "details",
        {}
    )

    cols = st.columns(
        len(sec_details)
    )


    for col, (section, info) in zip(
            cols,
            sec_details.items()
    ):

        with col:

            if info["present"]:

                st.success(
                    f"✓ {section.capitalize()}\n"
                    f"+{info['points']} pts"
                )

            else:

                st.error(
                    f"× {section.capitalize()}\n"
                    f"0 / {info['max']} pts"
                )


    st.divider()


    # ── Format Details ────────────────────────────────────────────────────────
    st.subheader("▤ Format Details")

    fmt_details = fmt.get(
        "details",
        {}
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        has_email = fmt_details.get(
            "email",
            {}
        ).get(
            "present",
            False
        )

        if has_email:
            st.success("✓ Email found")
        else:
            st.error("× Email missing")


    with col2:

        has_phone = fmt_details.get(
            "phone",
            {}
        ).get(
            "present",
            False
        )

        if has_phone:
            st.success("✓ Phone found")
        else:
            st.error("× Phone missing")


    with col3:

        wc = fmt_details.get(
            "length",
            {}
        ).get(
            "word_count",
            0
        )

        if fmt_details.get(
                "length",
                {}
        ).get(
            "ideal",
            False
        ):

            st.success(
                f"✓ Length: {wc} words"
            )

        else:

            st.warning(
                f"! Length: {wc} words"
            )


    with col4:

        verbs = fmt_details.get(
            "action_verbs",
            {}
        ).get(
            "found",
            []
        )

        if len(verbs) >= 3:

            st.success(
                f"✓ Action verbs: {len(verbs)}"
            )

        else:

            st.warning(
                f"! Action verbs: {len(verbs)}"
            )


    st.info(
        "→ Go to **Improvements** in the sidebar "
        "to see actionable suggestions."
    )

