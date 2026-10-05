
import streamlit as st

from theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResumeIQ",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# APPLY GLOBAL THEME
# =========================================================

apply_theme()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📄 ResumeIQ")

    st.caption("AI-powered Resume Analysis")

    st.divider()

    st.write(
        "Use the pages above to analyze your resume, "
        "match jobs, check ATS score, and improve your resume."
    )

    st.divider()

    st.caption("Analyze • Match • Improve")


# =========================================================
# MAIN PAGE
# =========================================================

st.title("📄 ResumeIQ")

st.subheader(
    "AI-powered resume analysis, job matching & ATS scoring"
)

st.write(
    "Analyze your resume, identify skills, match it with job descriptions, "
    "check ATS compatibility, and get actionable improvement suggestions."
)

st.divider()


# =========================================================
# HOW IT WORKS
# =========================================================

st.subheader("🚀 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1️⃣")
    st.write("**Upload Resume**")
    st.caption("PDF or DOCX")

with col2:
    st.subheader("2️⃣")
    st.write("**Analyze Skills**")
    st.caption("NLP & NER")

with col3:
    st.subheader("3️⃣")
    st.write("**Match Jobs**")
    st.caption("BERT + TF-IDF")

with col4:
    st.subheader("4️⃣")
    st.write("**Get Score**")
    st.caption("ATS Analysis")


st.divider()


# =========================================================
# FEATURES
# =========================================================

st.subheader("✨ Features")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.subheader("📊 Resume Analyzer")
        st.write(
            "Extract skills, contact information, organizations, "
            "and important resume sections using NLP."
        )

    with st.container(border=True):
        st.subheader("🎯 ATS Scorer")
        st.write(
            "Evaluate your resume based on keywords, sections, "
            "skills coverage, and ATS-friendly formatting."
        )


with col2:

    with st.container(border=True):
        st.subheader("💼 Job Matcher")
        st.write(
            "Compare your resume with job descriptions using "
            "semantic similarity and keyword matching."
        )

    with st.container(border=True):
        st.subheader("💡 Improvements")
        st.write(
            "Find missing skills, keywords, and areas where "
            "your resume can be improved."
        )


st.divider()


# =========================================================
# GET STARTED
# =========================================================

st.subheader("👈 Get Started")

st.info(
    "Select **Resume Analyzer** from the sidebar to upload "
    "your resume and begin the analysis."
)


# =========================================================
# TECH STACK
# =========================================================

with st.expander("🛠️ Tech Stack"):

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Frontend**")
        st.write("• Streamlit")

        st.write("**NLP**")
        st.write("• spaCy")
        st.write("• Named Entity Recognition")

        st.write("**Resume Processing**")
        st.write("• pdfplumber")
        st.write("• python-docx")

    with col2:

        st.write("**Matching**")
        st.write("• BERT")
        st.write("• TF-IDF")
        st.write("• Cosine Similarity")

        st.write("**Analysis**")
        st.write("• ATS Scoring")
        st.write("• Skill Matching")
        st.write("• Resume Suggestions")
