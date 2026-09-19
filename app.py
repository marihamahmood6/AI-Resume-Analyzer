import streamlit as st
import json
from resume_parser import extract_text_from_file
from ai_analyzer import analyze_resume
st.set_page_config(
    page_title="AI Resume Analyzer", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background-color: #0b0813;
        color: #e2e8f0;
    }
    .pill-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 9999px;
        background: rgba(147, 51, 234, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.3);
        color: #c084fc;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 24px;
    }
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 16px;
    }

    .hero-title em {
        font-style: italic;
        font-weight: 400;
        color: #c084fc;
    }
    .hero-subtitle {
        text-align: center;
        max-width: 650px;
        margin: 0 auto 40px auto;
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    div[data-testid="stColumn"] > div {
        background: #120d21;
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        padding: 24px;
    }
    .step-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .step-header span.step-num {
        color: #a855f7;
        margin-right: 6px;
    }

    .step-meta {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
    }
    .stTextArea textarea {
        background-color: #0b0813 !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stFileUploader"] {
        background-color: #0b0813;
        border: 1px dashed rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 10px;
    }
    div.stButton > button, div.stDownloadButton > button {
        background: #18112c !important;
        color: #a855f7 !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: #a855f7 !important;
        color: #ffffff !important;
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        justify-content: flex-start;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        background-color: #120d21;
        border-radius: 9999px;
        color: #94a3b8;
        padding: 0px 24px;
        border: 1px solid rgba(139, 92, 246, 0.15);
        font-size: 0.85rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(168, 85, 247, 0.2) !important;
        color: #c084fc !important;
        border-color: #a855f7 !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .tab-content-box {
        background: #120d21;
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
    }

    .tab-content-box h3 {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .bullet-item {
        color: #cbd5e1;
        line-height: 1.8;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; width: 100%; margin-bottom: 40px;">
        <div class="pill-badge">✦ AI-Powered Resume Analysis</div>
        <h1 class="hero-title" style="margin: 12px 0;">Land your <em>dream role</em><br>with precision feedback</h1>
        <p class="hero-subtitle" style="max-width: 650px; margin: 0 auto; padding: 0;">
            Upload your resume, paste the job description, and get detailed AI analysis 
            on your match score, strengths, and exactly what to improve.
        </p>
    </div>
""", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("""
        <div class="step-header">
            <div><span class="step-num">01</span> Upload Resume</div>
            <div class="step-meta">PDF • DOCX</div>
        </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your resume here",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

with col_right:
    st.markdown("""
        <div class="step-header">
            <div><span class="step-num">02</span> Target Job Description</div>
        </div>
    """, unsafe_allow_html=True)
    job_description = st.text_area(
        "Target Job Description",
        height=140,
        placeholder="Paste the full job description here — include requirements, responsibilities, and preferred qualifications...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None

if st.button("✦ Analyze Resume & Match Score", use_container_width=True):
    if not uploaded_file:
        st.warning("Please upload a resume file first.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Processing document and generating match metrics..."):
            try:
                resume_text = extract_text_from_file(uploaded_file)
                st.session_state["analysis_results"] = analyze_resume(resume_text, job_description)
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    st.error("Rate limit reached. Please wait 15–20 seconds and click analyze again.")
                else:
                    st.error(f"Error executing analysis: {e}")

if st.session_state["analysis_results"]:
    results = st.session_state["analysis_results"]
    score = results.get("match_score", 0)

    st.markdown("<br><hr style='border-color: rgba(139, 92, 246, 0.2);'><br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Match Score", "Skill Gap Analysis", "Keyword Matching", "Actionable Tips"])

    with tab1:
        st.markdown('<div class="tab-content-box">', unsafe_allow_html=True)
        m1, m2 = st.columns([1, 2])
        with m1:
            st.markdown(f"""
                <div style="text-align: center; padding: 24px; background: rgba(168, 85, 247, 0.1); border-radius: 16px; border: 1px solid rgba(168, 85, 247, 0.3);">
                    <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Match Score</div>
                    <div style="font-size: 3.5rem; font-weight: 800; color: #ffffff;">{score}%</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("### Executive Summary")
            st.info(results.get("summary", "Analysis completed."))
            st.progress(score / 100)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="tab-content-box">', unsafe_allow_html=True)
        st.markdown("<h3>Candidate Strengths</h3>", unsafe_allow_html=True)
        for point in results.get("strong_points", []):
            st.markdown(f'<div class="bullet-item">• {point}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="tab-content-box">', unsafe_allow_html=True)
        st.markdown("<h3>Missing Technical Keywords</h3>", unsafe_allow_html=True)
        keywords = results.get("missing_keywords", [])
        if keywords:
            st.write(" ".join([f"`{kw}`" for kw in keywords]))
        else:
            st.success("No missing keywords identified.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="tab-content-box">', unsafe_allow_html=True)
        st.markdown("<h3>Actionable Recommendations</h3>", unsafe_allow_html=True)
        for idx, item in enumerate(results.get("actionable_suggestions", []), 1):
            st.markdown(f'<div class="bullet-item"><b>{idx}.</b> {item}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.download_button(
        label="Download Full Analysis Report (JSON)",
        data=json.dumps(results, indent=4),
        file_name="resume_analysis_report.json",
        mime="application/json",
        use_container_width=True
    )