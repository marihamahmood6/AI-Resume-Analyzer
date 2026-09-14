import streamlit as st

from resume_parser import extract_text_from_file
from ai_analyzer import analyze_resume


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom Pink Styling
st.markdown("""
<style>
    .stButton > button {
        background-color: #ff69b4;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #ff1493;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Create two columns
col_left, col_right = st.columns([1, 1], gap="large")


# Left column - Resume upload
with col_left:
    st.subheader("1. Upload Resume")

    uploaded_file = st.file_uploader(
        "Supported formats: PDF, DOCX",
        type=["pdf", "docx"]
    )


# Right column - Job description
with col_right:
    st.subheader("2. Target Job Description")

    job_description = st.text_area(
        "Paste job description text:",
        height=180,
        placeholder="Paste full job requirement details here..."
    )


st.markdown("---")


# Analyze button
if st.button("Analyze Resume", use_container_width=True):

    if not uploaded_file:
        st.warning("Please upload a resume file first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        with st.spinner("Analyzing resume against job requirements..."):

            try:
                # 1. Extract text from uploaded resume
                resume_text = extract_text_from_file(uploaded_file)

                # 2. Send resume + job description to AI
                result = analyze_resume(
                    resume_text,
                    job_description
                )

                # 3. Display result
                st.subheader("Resume Analysis")
                st.write(result)

            except Exception as e:
                st.error(f"An error occurred: {e}")