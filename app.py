import streamlit as st
import sqlite3
from pypdf import PdfReader
from docx import Document
from parser import parse_resume

st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄",
    layout="wide"
)

DB_NAME = "candidates.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT
        )
    """)

    conn.commit()
    conn.close()


def extract_text(uploaded_file):
    file_type = uploaded_file.name.lower()

    if file_type.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif file_type.endswith(".docx"):
        document = Document(uploaded_file)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    elif file_type.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    return ""


def save_candidate(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates
        (name, email, phone, skills, education)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["email"],
        data["phone"],
        ", ".join(data["skills"]),
        data["education"]
    ))

    conn.commit()
    conn.close()


def get_candidates(search=""):
    conn = sqlite3.connect(DB_NAME)

    if search:
        query = """
            SELECT * FROM candidates
            WHERE name LIKE ?
            OR email LIKE ?
            OR skills LIKE ?
            OR education LIKE ?
        """
        value = f"%{search}%"
        rows = conn.execute(
            query, (value, value, value, value)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM candidates"
        ).fetchall()

    conn.close()
    return rows


def delete_candidate(candidate_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "DELETE FROM candidates WHERE id = ?",
        (candidate_id,)
    )
    conn.commit()
    conn.close()


init_db()

st.title("📄 Resume Parser & Candidate Database")
st.write(
    "Upload a resume to automatically extract candidate information."
)

st.header("📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Choose a resume",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    st.success(f"File uploaded: {uploaded_file.name}")

    try:
        text = extract_text(uploaded_file)

        if not text.strip():
            st.error("Could not extract text from this resume.")
        else:
            data = parse_resume(text)

            st.header("👤 Extracted Candidate Details")

            st.write("**Name:**", data["name"])
            st.write("**Email:**", data["email"])
            st.write("**Phone:**", data["phone"])
            st.write(
                "**Skills:**",
                ", ".join(data["skills"])
                if data["skills"]
                else "Not detected"
            )
            st.write("**Education:**", data["education"])

            if st.button("💾 Save Candidate"):
                save_candidate(data)
                st.success("Candidate saved successfully! ✅")

    except Exception as e:
        st.error(f"Error processing resume: {e}")


st.divider()

st.header("🔎 Candidate Search")

search = st.text_input(
    "Search by name, email, skill, or education"
)

candidates = get_candidates(search)

if candidates:

    for candidate in candidates:
        st.subheader(candidate[1])

        st.write("📧 Email:", candidate[2])
        st.write("📱 Phone:", candidate[3])
        st.write("🛠️ Skills:", candidate[4])
        st.write("🎓 Education:", candidate[5])

        if st.button(
            "🗑️ Delete",
            key=f"delete_{candidate[0]}"
        ):
            delete_candidate(candidate[0])
            st.success("Candidate deleted.")
            st.rerun()

        st.divider()

else:
    st.info("No candidates found.")
