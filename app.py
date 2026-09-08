import streamlit as st

st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄"
)

st.title("📄 Resume Parser & Candidate Database")
st.write("Upload a resume to extract candidate information.")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    st.subheader("Candidate Details")

    name = st.text_input("Candidate Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    skills = st.text_input("Skills")
    education = st.text_input("Education")

    if st.button("Save Candidate"):
        st.success("Candidate saved successfully! ✅")
