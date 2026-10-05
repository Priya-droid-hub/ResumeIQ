
import streamlit as st
import sys
import os

from theme import apply_theme


@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')


# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from analyzer.matcher import match_single_job, get_top_matches


st.set_page_config(
    page_title="Job Matcher",
    page_icon="▰",
    layout="wide"
)

apply_theme()


st.title("▰ Job Matcher")

st.markdown(
    "Match your resume against job descriptions using BERT + TF-IDF similarity."
)

st.divider()


# ── Check session state ────────────────────────────────────────────────────────
if "resume_text" not in st.session_state:
    st.warning(
        "⚠ Please upload your resume on the **Resume Analyzer** page first."
    )
    st.stop()

resume_text = st.session_state["resume_text"]

st.success("✓ Resume loaded from previous page.")

st.divider()


# ── Match Mode ─────────────────────────────────────────────────────────────────
st.subheader("⌁ Choose Matching Mode")

mode = st.radio(
    "How would you like to match?",
    [
        "Match against sample job database",
        "Paste your own job description"
    ],
    horizontal=True
)

st.divider()


# ── Mode 1: Match against job database ────────────────────────────────────────
if mode == "Match against sample job database":

    top_n = st.slider(
        "Number of top matches to show",
        min_value=1,
        max_value=8,
        value=5
    )

    if st.button("⌁ Find Best Matches", type="primary"):

        with st.spinner(
                "Matching resume against job database..."
        ):
            matches = get_top_matches(
                resume_text,
                top_n=top_n
            )

        st.subheader(
            f"Top {top_n} Job Matches"
        )

        for i, job in enumerate(matches, 1):

            match_pct = job["match_percent"]

            # Color based on score
            if match_pct >= 70:
                color = "#28a745"
            elif match_pct >= 50:
                color = "#ffc107"
            else:
                color = "#dc3545"

            with st.container():

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.markdown(
                        f"### #{i} {job['title']} — *{job['company']}*"
                    )

                    st.progress(
                        match_pct / 100
                    )

                    col_a, col_b, col_c = st.columns(3)

                    col_a.metric(
                        "Combined Match",
                        f"{match_pct}%"
                    )

                    col_b.metric(
                        "BERT Score",
                        f"{round(job['bert_score'] * 100, 1)}%"
                    )

                    col_c.metric(
                        "TF-IDF Score",
                        f"{round(job['tfidf_score'] * 100, 1)}%"
                    )

                with col2:

                    st.markdown(
                        f'<div style="background:{color}; color:white; '
                        f'border-radius:50%; width:80px; height:80px; '
                        f'display:flex; align-items:center; justify-content:center; '
                        f'font-size:1.4rem; font-weight:800; margin:auto;">'
                        f'{match_pct}%</div>',
                        unsafe_allow_html=True
                    )

                with st.expander(
                        "View Job Description"
                ):
                    st.write(
                        job["description"]
                    )

                st.divider()


# ── Mode 2: Paste custom job description ──────────────────────────────────────
else:

    job_input = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Copy and paste the full job description here..."
    )

    if st.button(
            "⌁ Match My Resume",
            type="primary"
    ):

        if not job_input.strip():

            st.error(
                "Please paste a job description first."
            )

        else:

            with st.spinner(
                    "Computing similarity..."
            ):

                scores = match_single_job(
                    resume_text,
                    job_input
                )

            st.subheader(
                "Match Results"
            )

            combined_pct = round(
                scores["combined_score"] * 100,
                1
            )

            bert_pct = round(
                scores["bert_score"] * 100,
                1
            )

            tfidf_pct = round(
                scores["tfidf_score"] * 100,
                1
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Combined Match",
                f"{combined_pct}%"
            )

            col2.metric(
                "BERT Score",
                f"{bert_pct}%"
            )

            col3.metric(
                "TF-IDF Score",
                f"{tfidf_pct}%"
            )

            st.progress(
                combined_pct / 100
            )

            if combined_pct >= 70:

                st.success(
                    "Strong match! Your resume aligns well with this job."
                )

            elif combined_pct >= 50:

                st.warning(
                    "Moderate match. Consider tailoring your resume to this job."
                )

            else:

                st.error(
                    "Low match. Check the Improvements page for suggestions."
                )

            # Save job text for other pages
            st.session_state["job_text"] = job_input

            st.info(
                "→ Go to **ATS Scorer** to see a detailed score breakdown."
            )
