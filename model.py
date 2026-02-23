from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re

# ----------------------------------------
# ROLE SKILL DATABASE
# ----------------------------------------

roles = {
    "Data Analyst": [
        "python","pandas","numpy","matplotlib","seaborn",
        "sql","excel","statistics","power bi","tableau"
    ],

    "SOC Analyst": [
        "siem","splunk","wireshark","incident response",
        "log analysis","network security","threat detection",
        "nmap","linux","security"
    ],

    "Web Developer": [
        "html","css","javascript","react","node",
        "mongodb","express","api","frontend","backend"
    ]
}

# ----------------------------------------
# PDF TEXT EXTRACTION
# ----------------------------------------

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

# ----------------------------------------
# ROLE PREDICTION (TFIDF + COSINE SIMILARITY)
# ----------------------------------------

def predict_role(resume_text):

    role_docs = [" ".join(skills) for skills in roles.values()]
    documents = role_docs + [resume_text]

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(documents)

    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    scores = similarity[0]

    best_index = scores.argmax()
    best_role = list(roles.keys())[best_index]

    return best_role, scores

# ----------------------------------------
# SKILL GAP ANALYSIS
# ----------------------------------------

def skill_gap_analysis(resume_text, role):

    resume_text = resume_text.lower()
    required = roles[role]

    present = [skill for skill in required if skill in resume_text]
    missing = [skill for skill in required if skill not in resume_text]

    return present, missing

# ----------------------------------------
# CERTIFICATION DETECTION (SMART)
# ----------------------------------------

def detect_certifications(text):

    text_original = text
    text = text.lower()
    found = set()

    patterns = [
        r'certified\s+[A-Za-z0-9+ ]+',
        r'[A-Za-z0-9+ ]+\s+certification',
        r'[A-Za-z0-9+ ]+\s+certificate',
        r'[A-Za-z0-9+ ]+\s+credential',
        r'\([A-Z]{2,6}-?\d{0,4}\)'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text_original, re.IGNORECASE)
        for m in matches:
            found.add(m.strip())

    providers = [
        "coursera","udemy","edx","nptel",
        "google","aws","azure","microsoft",
        "cisco","ibm","oracle","comptia"
    ]

    for line in text_original.split("\n"):
        for p in providers:
            if p in line.lower() and len(line.split()) < 12:
                found.add(line.strip())

    section_pattern = r'(certifications|licenses)(.*?)(projects|experience|skills|education)'
    section = re.search(section_pattern, text, re.DOTALL)

    if section:
        for l in section.group(2).split("\n"):
            if len(l.split()) <= 10:
                found.add(l.strip())

    return list(found)

# ----------------------------------------
# ATS SCORE CALCULATION
# ----------------------------------------

def ats_score(resume_text, role):

    text = resume_text.lower()

    required_skills = roles[role]
    skill_matches = sum(1 for skill in required_skills if skill in text)
    skills_score = (skill_matches / len(required_skills)) * 40

    project_keywords = ["project","developed","built","implemented","system"]
    project_count = sum(1 for word in project_keywords if word in text)
    project_score = min(project_count * 5, 20)

    certifications = detect_certifications(resume_text)
    cert_score = min(len(certifications) * 8, 20)

    experience_keywords = ["intern","experience","worked","company"]
    exp_count = sum(1 for word in experience_keywords if word in text)
    exp_score = min(exp_count * 5, 20)

    total_score = skills_score + project_score + cert_score + exp_score

    breakdown = {
        "skills": round(skills_score,2),
        "projects": project_score,
        "certifications": cert_score,
        "experience": exp_score
    }

    return round(total_score,2), breakdown


