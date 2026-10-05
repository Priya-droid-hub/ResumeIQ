import re
import json
import os

import streamlit as st
import spacy


@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return spacy.load("en_core_web_md")


nlp = load_nlp()

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_PATH = os.path.join(BASE_DIR, "..", "data", "skills_list.json")


# ============================================================
# ORGANIZATION DATA
# ============================================================

ORG_BLOCKLIST = {
    "education", "experience", "skills", "projects", "objective",
    "summary", "certifications", "achievements", "hobbies",
    "interests", "references", "profile", "gpa",

    "python", "java", "javascript", "typescript", "css", "html",
    "sql", "bash", "react", "node", "nodejs", "django", "flask",
    "numpy", "pandas", "matplotlib", "tensorflow", "pytorch",
    "scikit", "scikit-learn", "opencv", "spacy", "nltk",
    "docker", "kubernetes", "git", "github", "linux", "aws",
    "azure", "gcp", "mysql", "postgresql", "mongodb", "redis",

    "machine learning enthusiast", "aspiring", "personal project",
    "full stack", "frontend", "backend", "ui", "ux", "api",
    "rest", "agile", "scrum", "kociemba", "rubik", "cbse",
    "intermediate", "senior", "junior", "intern", "developer",
    "engineer", "analyst", "manager", "lead", "head",

    "computer science and engineering",
    "technical group",
    "cultural heritage of india",
    "solutions architecture simulation",
    "certificate",
    "certification",
    "hackathon 2024 certificate",
    "apac",
}


KNOWN_ORGS = [
    # Indian Colleges
    "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kanpur",
    "IIT Kharagpur", "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad",
    "IIT BHU",

    "NIT Trichy", "NIT Surathkal", "NIT Warangal", "NIT Calicut",

    "BITS Pilani", "BITS Goa", "BITS Hyderabad",

    "VIT Vellore", "VIT Chennai",

    "SRM University",
    "Amity University",
    "Delhi University",
    "Mumbai University",
    "Anna University",
    "Jawaharlal Nehru University",
    "Jadavpur University",

    "Maharana Pratap Group of Institutes",
    "Maharana Institute of Professional Studies Kanpur",
    "Kendriya Vidyalaya O.E.F Kanpur",
    "Dr. Virendra Swarup Public School",

    # Global Companies
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix",
    "Adobe", "Salesforce", "Oracle", "IBM", "Intel", "Nvidia",
    "Twitter", "LinkedIn", "Uber", "Airbnb", "Spotify",

    # Indian Companies
    "Infosys", "Wipro", "TCS",
    "Tata Consultancy Services",
    "HCL Technologies",
    "Tech Mahindra",
    "Cognizant",
    "Accenture",
    "Capgemini",
    "Mphasis",
    "Hexaware",
    "Mindtree",
    "Flipkart",
    "Zomato",
    "Swiggy",
    "Paytm",
    "Razorpay",
    "BYJU'S",
    "Ola",
    "Myntra",
    "Meesho",
    "PhonePe",

    # Clubs & Organizations
    "Tech-E-Clan",
    "IEEE",
    "ACM",
    "NSS",
    "NCC",
    "Smart India Hackathon",
    "Google Developer Student Clubs",
    "GDSC",
    "Microsoft Learn Student Ambassadors",

    # Platforms
    "HackerRank",
    "LeetCode",
    "Coursera",
    "Udemy",
    "edX",
    "GitHub",
    "GitLab",
]


# ============================================================
# UTILITY
# ============================================================

def remove_substrings(org_list):
    result = []

    for org in org_list:
        if not any(
                org != other and org.lower() in other.lower()
                for other in org_list
        ):
            result.append(org)

    return result


# ============================================================
# SKILLS
# ============================================================

def load_skills() -> list:

    with open(SKILLS_PATH, "r", encoding="utf-8") as f:
        skills_dict = json.load(f)

    flat_skills = []

    for category, skills in skills_dict.items():
        flat_skills.extend(skills)

    return flat_skills


# ============================================================
# NAME EXTRACTION
# ============================================================

def extract_name(text: str, doc) -> str | None:
    """
    Extract the candidate's name using multiple signals.

    Priority:
    1. Explicit "Name:" / "Full Name:" field
    2. Name-like line near the beginning
    3. spaCy PERSON entity near the beginning

    Explicitly ignores:
    Father's Name, Mother's Name, Guardian Name, Parent Name, etc.
    """

    # --------------------------------------------------------
    # Normalize text
    # --------------------------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # --------------------------------------------------------
    # Words/phrases that indicate someone else's name
    # --------------------------------------------------------

    excluded_labels = [
        "father",
        "father's",
        "father name",
        "fathers name",
        "mother",
        "mother's",
        "mother name",
        "mothers name",
        "guardian",
        "guardian's",
        "guardian name",
        "parent",
        "parent's",
        "parent name",
        "husband",
        "wife",
        "spouse",
        "son of",
        "daughter of",
        "s/o",
        "d/o",
        "care of",
        "c/o",
    ]

    # --------------------------------------------------------
    # 1. Look for explicit Name field
    # --------------------------------------------------------

    name_patterns = [
        r"^\s*name\s*[:\-]\s*(.+)$",
        r"^\s*full\s*name\s*[:\-]\s*(.+)$",
        r"^\s*candidate\s*name\s*[:\-]\s*(.+)$",
        r"^\s*applicant\s*name\s*[:\-]\s*(.+)$",
    ]

    for line in lines[:40]:

        line_lower = line.lower()

        # Never accept a line mentioning father/mother/etc.
        if any(label in line_lower for label in excluded_labels):
            continue

        for pattern in name_patterns:

            match = re.match(pattern, line, re.IGNORECASE)

            if match:

                candidate = match.group(1).strip()

                if is_valid_name(candidate):
                    return candidate


    # --------------------------------------------------------
    # 2. Look for a name-like line near the top
    # --------------------------------------------------------

    # Most resumes put the candidate name within the first
    # several lines.

    for line in lines[:15]:

        line_lower = line.lower()

        # Ignore contact/heading lines
        if any(
                keyword in line_lower
                for keyword in [
                    "resume",
                    "curriculum vitae",
                    "email",
                    "phone",
                    "mobile",
                    "linkedin",
                    "github",
                    "http",
                    "www.",
                    "@",
                    "address",
                    "objective",
                    "summary",
                    "profile",
                ]
        ):
            continue

        # Ignore family/member names
        if any(label in line_lower for label in excluded_labels):
            continue

        if is_valid_name(line):
            return line


    # --------------------------------------------------------
    # 3. spaCy fallback
    # --------------------------------------------------------

    person_entities = []

    for ent in doc.ents:

        if ent.label_ != "PERSON":
            continue

        candidate = ent.text.strip()

        # Ignore family-related context
        start = max(0, ent.start_char - 60)
        context_before = text[start:ent.start_char].lower()

        if any(label in context_before for label in excluded_labels):
            continue

        if is_valid_name(candidate):
            person_entities.append(
                (
                    ent.start_char,
                    candidate
                )
            )

    # Prefer the earliest valid person in the document
    if person_entities:
        person_entities.sort(key=lambda x: x[0])
        return person_entities[0][1]

    return None


def is_valid_name(candidate: str) -> bool:
    """
    Basic validation for a person's name.
    """

    candidate = candidate.strip()

    if not candidate:
        return False

    # Remove common punctuation around the name
    candidate = candidate.strip(":-|,.")

    # Too long to realistically be a person's name
    words = candidate.split()

    if len(words) < 2 or len(words) > 5:
        return False

    # Don't accept numbers
    if re.search(r"\d", candidate):
        return False

    # Don't accept email / URLs
    if "@" in candidate:
        return False

    if "http://" in candidate.lower():
        return False

    if "https://" in candidate.lower():
        return False

    # Name should mostly contain letters
    if not re.fullmatch(
            r"[A-Za-zÀ-ÖØ-öø-ÿ.'\- ]+",
            candidate
    ):
        return False

    # Reject common resume headings
    blocked = {
        "resume",
        "curriculum vitae",
        "professional summary",
        "career objective",
        "computer science",
        "software engineer",
        "software developer",
        "data analyst",
        "student",
    }

    if candidate.lower() in blocked:
        return False

    return True


# ============================================================
# ENTITY EXTRACTION
# ============================================================

def extract_entities(text: str) -> dict:

    doc = nlp(text)

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    email_pattern = (
        r'[a-zA-Z0-9._%+-]+'
        r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )

    emails = re.findall(email_pattern, text)

    email = emails[0] if emails else None


    # --------------------------------------------------------
    # Phone
    # --------------------------------------------------------

    phone_pattern = r'(\+?\d[\d\s\-().]{8,14}\d)'

    phones = re.findall(phone_pattern, text)

    phone = phones[0].strip() if phones else None


    # --------------------------------------------------------
    # Name
    # --------------------------------------------------------

    name = extract_name(text, doc)


    # --------------------------------------------------------
    # Organizations
    # --------------------------------------------------------

    organizations = extract_organizations(text)


    return {
        "name": name,
        "email": email,
        "phone": phone,
        "organizations": organizations
    }


# ============================================================
# ORGANIZATION EXTRACTION
# ============================================================

def extract_organizations(text: str) -> list:

    organizations = []

    for org in KNOWN_ORGS:

        pattern = r'\b' + re.escape(org) + r'\b'

        if re.search(pattern, text, re.IGNORECASE):

            if org not in organizations:
                organizations.append(org)

    return remove_substrings(organizations)


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text: str) -> list:

    skills = load_skills()

    text_lower = text.lower()

    found = []

    for skill in skills:

        skill_lower = skill.lower()

        pattern = r'\b' + re.escape(skill_lower) + r'\b'

        if re.search(pattern, text_lower):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_sections(text: str) -> dict:
    """
    Detect common resume sections using flexible heading patterns.
    """

    text_lower = text.lower()

    return {

        "education": bool(
            re.search(
                r"\beducation\b"
                r"|\bacademic background\b"
                r"|\beducational background\b",
                text_lower
            )
        ),

        "experience": bool(
            re.search(
                r"\bexperience\b"
                r"|\bwork experience\b"
                r"|\bwork history\b"
                r"|\bprofessional experience\b"
                r"|\binternship\b"
                r"|\binternships\b",
                text_lower
            )
        ),

        "skills": bool(
            re.search(
                r"\bskills\b"
                r"|\btechnical skills\b"
                r"|\btechnical expertise\b"
                r"|\bcore skills\b",
                text_lower
            )
        ),

        "projects": bool(
            re.search(
                r"\bprojects\b"
                r"|\bproject experience\b"
                r"|\bacademic projects\b"
                r"|\bpersonal projects\b",
                text_lower
            )
        ),

        "summary": bool(
            re.search(
                r"\bsummary\b"
                r"|\bprofessional summary\b"
                r"|\bcareer summary\b"
                r"|\bobjective\b"
                r"|\bprofile\b"
                r"|\babout me\b",
                text_lower
            )
        ),

        "certifications": bool(
            re.search(
                r"\bcertification\b"
                r"|\bcertifications\b"
                r"|\bcertificate\b"
                r"|\bcourses\b"
                r"|\bcredentials\b",
                text_lower
            )
        ),

        "achievements": bool(
            re.search(
                r"\bachievement[s]?\b"
                r"|\baccomplishment[s]?\b"
                r"|\baward[s]?\b"
                r"|\bhonor[s]?\b"
                r"|\bhonours?\b",
                text_lower
            )
        )
    }


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_resume(text: str) -> dict:

    entities = extract_entities(text)

    skills = extract_skills(text)

    sections = extract_sections(text)

    return {
        "name": entities["name"],
        "email": entities["email"],
        "phone": entities["phone"],
        "organizations": entities["organizations"],
        "skills": skills,
        "sections": sections,
        "raw_text": text
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    import sys

    ROOT = os.path.abspath(
        os.path.join(BASE_DIR, "..")
    )

    sys.path.insert(0, ROOT)

    from analyzer.parser import extract_text_from_pdf

    pdf_path = os.path.join(
        ROOT,
        "sample_resume.pdf"
    )

    text = extract_text_from_pdf(pdf_path)

    result = analyze_resume(text)

    print(f"Name          : {result['name']}")
    print(f"Email         : {result['email']}")
    print(f"Phone         : {result['phone']}")
    print(f"Organizations : {result['organizations']}")
    print(f"Skills found  : {result['skills']}")

    print("\nSections:")

    for section, present in result["sections"].items():

        print(
            f"  {'✓' if present else '✗'} "
            f"{section.capitalize()}"
        )