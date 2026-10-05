# 📄 ResumeIQ

### AI-Powered Resume Analysis, Job Matching & ATS Scoring

ResumeIQ is a web-based resume analysis platform that helps students and job seekers understand how well their resume matches a job description and how they can improve it.

🔗 **Live Demo:** https://resumeiq-5-10.streamlit.app/

🔗 **GitHub:** https://github.com/Priya-droid-hub/ResumeIQ

---

## 🚀 Features

### 📊 Resume Analyzer

* Upload your resume in PDF or DOCX format
* Extract contact information
* Identify skills and important resume sections
* Analyze resume content using NLP

### 💼 Job Matcher

* Compare your resume with a job description
* Identify matching skills and keywords
* Calculate similarity between resume and job requirements
* Highlight missing skills

### 🎯 ATS Scorer

* Evaluate resume ATS compatibility
* Analyze important sections and keywords
* Generate an overall ATS score
* Identify areas that can affect resume screening

### 💡 Resume Improvements

* Identify missing skills
* Find important keywords
* Get actionable suggestions
* Improve resume structure and content

---

## 🛠️ Tech Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core development               |
| Streamlit             | Web application                |
| spaCy                 | NLP & Named Entity Recognition |
| Sentence Transformers | Semantic similarity            |
| Scikit-learn          | TF-IDF & similarity            |
| pdfplumber            | PDF resume extraction          |
| python-docx           | DOCX processing                |
| PyTorch               | Machine learning backend       |

---

## 🧠 How It Works

```text
Resume Upload
      ↓
Text Extraction
      ↓
NLP & Skill Extraction
      ↓
Resume Analysis
      ↓
Job Description Matching
      ↓
ATS Scoring
      ↓
Improvement Suggestions
```

---

## 📁 Project Structure

```text
ResumeIQ/
│
├── app.py
├── theme.py
├── requirements.txt
├── README.md
│
├── analyzer/
│   ├── parser.py
│   ├── ner.py
│   ├── vectorizer.py
│   ├── matcher.py
│   ├── scorer.py
│   └── suggester.py
│
├── data/
│   ├── skills_list.json
│   └── job_descriptions.json
│
└── pages/
    ├── 1_Resume_Analyzer.py
    ├── 2_Job_Matcher.py
    ├── 3_ATS_Scorer.py
    └── 4_Improvements.py
```

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Priya-droid-hub/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🎯 Use Cases

ResumeIQ can be useful for:

* Students preparing for placements
* Freshers applying for internships
* Job seekers improving their resumes
* Candidates preparing ATS-friendly resumes
* Comparing resumes with specific job descriptions

---

## 🔮 Future Improvements

* AI-powered resume rewriting
* More advanced interview preparation
* Resume section quality scoring
* Support for additional file formats
* More job description datasets
* Personalized career recommendations
* Resume version comparison

---

## 👩‍💻 Author

**Priyanka Jagtap**

IT Engineering Student | Java Developer | AI & Cloud Enthusiast

---

## ⭐ Project

If you find ResumeIQ useful, consider giving the repository a ⭐ on GitHub.
