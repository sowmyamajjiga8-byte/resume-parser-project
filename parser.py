import re


SKILLS = [
    "Python", "Java", "C++", "JavaScript", "HTML", "CSS",
    "SQL", "MySQL", "MongoDB", "Django", "Flask", "React",
    "Pandas", "NumPy", "TensorFlow", "PyTorch",
    "Machine Learning", "Deep Learning", "Data Science",
    "OpenCV", "Git", "GitHub", "Docker",
    "Agile", "Agile Project Management", "Scrum",
    "JIRA", "Asana", "Data Analysis", "Budget Forecasting",
    "Team Leadership", "Project Coordination",
    "Project Management", "Communication",
    "Problem-solving", "Time Management",
    "Client Relations", "Cross-functional Collaboration",
    "Strategic Planning", "Stakeholder Management"
]


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return match.group(0) if match else "Not detected"


def extract_phone(text):
    match = re.search(
        r"\+?\d[\d\s().-]{8,}\d",
        text
    )
    return match.group(0).strip() if match else "Not detected"


def extract_name(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    for line in lines[:10]:
        if (
            2 <= len(line.split()) <= 4
            and "@" not in line
            and not any(c.isdigit() for c in line)
        ):
            return line

    return "Not detected"


def extract_skills(text):
    found = []
    text_lower = text.lower()

    # Normal skill matching
    for skill in SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)

    # Extra extraction from the Skills section
    section_match = re.search(
        r"(key skills|skills|hard skills)(.*?)(?=soft skills|education|work experience|experience|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if section_match:
        section = section_match.group(2)

        for skill in SKILLS:
            if skill.lower() in section.lower():
                found.append(skill)

    return sorted(set(found))


def extract_education(text):
    education_words = [
        "B.Tech", "B.E", "M.Tech", "M.E",
        "B.Sc", "M.Sc", "BCA", "MCA", "MBA",
        "Ph.D", "Bachelor", "Master", "Diploma"
    ]

    found = []

    for word in education_words:
        if word.lower() in text.lower():
            found.append(word)

    return ", ".join(found) if found else "Not detected"


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }
