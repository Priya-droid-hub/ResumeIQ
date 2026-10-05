
import streamlit as st
import sys
import os

from theme import apply_theme


# Path setup
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from analyzer.parser import parse_resume
from analyzer.ner import analyze_resume


st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="▤",
    layout="wide"
)

apply_theme()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("▤ Resume Analyzer")

st.caption(
    "Extract your skills, contact information, organizations "
    "and resume sections using NLP-powered analysis."
)

st.divider()


# ---------------------------------------------------------
# UPLOAD
# ---------------------------------------------------------

st.subheader("↑ Upload Your Resume")

st.write(
    "Upload your latest resume in PDF or DOCX format to begin the analysis."
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if uploaded_file is not None:

    with st.spinner("Parsing resume..."):

        try:
            resume_text = parse_resume(uploaded_file)

        except ValueError as e:
            st.error(str(e))
            st.stop()

    if not resume_text.strip():

        st.error(
            "Could not extract text from your resume. "
            "Make sure the file is not a scanned image."
        )

        st.stop()

    with st.spinner("Analyzing resume with NLP..."):
        result = analyze_resume(resume_text)

    # Store results
    st.session_state["resume_text"] = resume_text
    st.session_state["resume_result"] = result

    st.success(
        f"Resume analyzed successfully — {uploaded_file.name}"
    )

    st.divider()


    # ---------------------------------------------------------
    # RESUME OVERVIEW
    # ---------------------------------------------------------

    st.subheader("▦ Resume Overview")

    st.caption("Quick statistics from your uploaded resume.")

    word_count = len(resume_text.split())
    character_count = len(resume_text)

    skills_count = len(result.get("skills", []))
    organizations_count = len(
        result.get("organizations", [])
    )

    sections = result.get("sections", {})

    sections_present = sum(
        1
        for present in sections.values()
        if present
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Words",
            f"{word_count:,}"
        )

    with col2:
        st.metric(
            "Skills Found",
            skills_count
        )

    with col3:
        st.metric(
            "Organizations",
            organizations_count
        )

    with col4:
        st.metric(
            "Sections Present",
            sections_present
        )

    with col5:
        st.metric(
            "Characters",
            f"{character_count:,}"
        )


    st.divider()


    # ---------------------------------------------------------
    # CONTACT INFORMATION
    # ---------------------------------------------------------

    st.subheader("Contact Information")

    contact_col1, contact_col2, contact_col3 = st.columns(3)

    with contact_col1:
        st.caption("Name")
        st.write(
            result.get("name") or "Not detected"
        )

    with contact_col2:
        st.caption("Email")
        st.write(
            result.get("email") or "Not detected"
        )

    with contact_col3:
        st.caption("Phone")
        st.write(
            result.get("phone") or "Not detected"
        )


    st.divider()


    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------

    st.subheader("⚙ Skills Detected")

    skills = result.get("skills", [])

    if skills:

        st.success(
            f"Found {len(skills)} skills in your resume."
        )

        skill_columns = st.columns(4)

        for index, skill in enumerate(skills):

            with skill_columns[index % 4]:
                st.info(skill)

    else:

        st.warning(
            "No skills detected. Make sure your resume contains "
            "a clear Skills section."
        )


    st.divider()


    # ---------------------------------------------------------
    # ORGANIZATIONS
    # ---------------------------------------------------------

    st.subheader("▰ Organizations Detected")

    organizations = result.get("organizations", [])

    if organizations:

        org_columns = st.columns(3)

        for index, organization in enumerate(organizations):

            with org_columns[index % 3]:
                st.write(f"• {organization}")

    else:

        st.info("No organizations detected.")


    st.divider()


    # ---------------------------------------------------------
    # RESUME SECTIONS
    # ---------------------------------------------------------

    st.subheader("☷ Resume Sections")

    if sections:

        section_columns = st.columns(3)

        for index, (section, present) in enumerate(
                sections.items()
        ):

            with section_columns[index % 3]:

                if present:

                    st.success(
                        f"✓ {section.capitalize()}"
                    )

                else:

                    st.warning(
                        f"○ {section.capitalize()} — Missing"
                    )

        total_sections = len(sections)

        if total_sections > 0:

            completeness = (
                    sections_present / total_sections
            )

            st.write(
                f"**Resume Section Completeness: "
                f"{sections_present}/{total_sections}**"
            )

            st.progress(completeness)


    st.divider()


    # ---------------------------------------------------------
    # RAW RESUME TEXT
    # ---------------------------------------------------------

    with st.expander(
            "▤ View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted Text",
            resume_text,
            height=350
        )


    # ---------------------------------------------------------
    # NEXT STEP
    # ---------------------------------------------------------

    st.info(
        "→ Next step: Open **Job Matcher** from the sidebar "
        "to compare your resume with a job description."
    )


else:

    st.info(
        "▤ Please upload a PDF or DOCX resume to get started."
    )
