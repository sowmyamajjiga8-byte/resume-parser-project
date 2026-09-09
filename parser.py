import re


SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "MongoDB",
    "Django",
    "Flask",
    "React",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "OpenCV",
    "Git",
    "GitHub",
    "Docker",
    "Agile",
    "Agile Project Management",
    "Scrum",
    "JIRA",
    "Jira",
    "Asana",
    "Data Analysis",
    "Budget Forecasting",
    "Team Leadership",
    "Project Coordination",
    "Project Management",
    "Communication",
    "Problem-solving",
    "Time Management",
    "Client Relations",
    "Cross-functional Collaboration",
    "Strategic Planning",
    "Stakeholder Management"
]


def extract_email(text):
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if match:
        return match.group(0)

    return "Not detected"


def extract_phone(text):
    match = re.search(
        r"(\+?\d[\d\s().-]{8,}\d)",
        text
    )

    if match:
        return match.group(0).strip()

    return "Not detected"


def extract_name(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:
        if (
            2 <= len(line.split()) <= 4
            and "@" not in line
            and not any(char.isdigit() for char in line)
        ):
            return line

    return "Not detected"


def extract_skills(text):
    found = []

    text_lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)

    return sorted(set(found))


def extract_education(text):
    patterns = [
        r"B\.?\s*Tech",
        r"B\.?\s*E",
        r"M\.?\s*Tech",
        r"M\.?\s*E",
        r"B\.?\s*Sc",
        r"M\.?\s*Sc",
        r"BCA",
        r"MCA",
        r"MBA",
        r"Ph\.?\s*D",
        r"Bachelor",
        r"Master",
        r"Diploma"
    ]

    found = []

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(
                re.sub(r"\\\.?|\s+", "", pattern)
            )

    if found:
        return ", ".join(found)

    return "Not detected"


def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }
