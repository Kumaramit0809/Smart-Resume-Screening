import streamlit as st
import spacy
from spacy.cli import download as spacy_download
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_matcher import match_skills
from utils.report_generator import generate_pdf
from utils.skills_list import TECH_SKILLS
import plotly.graph_objects as go


# ---------------------------PAGE CONFIG---------------------------
st.set_page_config(
    page_title="The Job-Fit Predictor",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------DARK MODE STYLE---------------------------
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
        body, .stApp { background-color: #0E1117; color: white; }

        .result-card { 
            background: #1E1F26; 
            padding: 20px; 
            border-radius: 12px;
            margin-top: 20px; 
        }

        .skill-tag {
            background: #2E3B4E;
            padding: 8px 14px;
            margin: 6px;
            border-radius: 10px;
            font-size: 14px;
            display: inline-block;
            color: white;
            border: 1px solid #445A77;
        }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
        .result-card { 
            background: #F5F5F7; 
            padding: 20px; 
            border-radius: 12px; 
            margin-top: 20px; 
        }

        .skill-tag {
            background: #E0E7FF;
            padding: 8px 14px;
            margin: 6px;
            border-radius: 10px;
            font-size: 14px;
            display: inline-block;
            color: #1F2A44;
            border: 1px solid #B3C5FF;
        }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------LOAD SPACY MODEL---------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy_download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# ---------------------------NAVIGATION---------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "📊 Results"])
st.sidebar.divider()

# ---------------------------HOME PAGE---------------------------
if page == "🏠 Home":

    st.title("🧠 The Job-Fit Predictor")
    st.write("AI-powered Resume Evaluation")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

    with col2:
        job_description = st.text_area("📝 Paste Job Description", height=220)

    if st.button("🔍 Analyze Resume", use_container_width=True):

        if uploaded_file and job_description:

            with st.spinner("Analyzing resume..."):
                progress = st.progress(0)

                # Extract text
                resume_text = extract_text_from_pdf(uploaded_file)
                progress.progress(25)

                # Clean text
                cleaned_resume = clean_text(resume_text)
                jd_cleaned = clean_text(job_description)
                progress.progress(50)

                # Skill match
                matched_skills, match_percent = match_skills(cleaned_resume, jd_cleaned)
                progress.progress(90)

                # Save to session
                st.session_state["percent"] = match_percent
                st.session_state["skills"] = matched_skills

                progress.progress(100)

            # SUCCESS + CLICKABLE ARROW BUTTON
            st.success("✅ Analysis Completed! Go to Results")

            # # ------------------ ARROW BUTTON TO RESULTS PAGE ------------------
            # if st.button("➡ Go to Results"):
            #     st.switch_page("Results")


        else:
            st.warning("⚠️ Upload resume and enter job description!")

# ---------------------------RESULTS PAGE---------------------------
elif page == "📊 Results":

    if "percent" not in st.session_state:
        st.warning("⚠️ No analysis found. Please analyze resume first.")
        st.stop()

    match_percent = st.session_state["percent"]
    matched_skills = st.session_state["skills"]

    st.title("📊 Resume Analysis Result")

    # Gauge Meter
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_percent,
        title={"text": "Resume Match Score"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    st.plotly_chart(gauge, use_container_width=True)

    # Result Card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    st.markdown(f"<h2>Match Score: {match_percent:.2f}%</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Matched Skills:</h4>", unsafe_allow_html=True)

    # Horizontal Skill Tags
    if matched_skills:
        skills_html = "<div style='display:flex; flex-wrap:wrap; gap:10px;'>"
        for skill in matched_skills:
            skills_html += f"<span class='skill-tag'>{skill}</span>"
        skills_html += "</div>"

        st.markdown(skills_html, unsafe_allow_html=True)

    else:
        st.write("❌ No matching skills found")

    st.markdown("</div>", unsafe_allow_html=True)

    # Feedback
    st.subheader("🗣 Feedback")

    if match_percent >= 80:
        feedback = "Excellent match! Your resume aligns very well with the job requirements."
    elif match_percent >= 60:
        feedback = "Good match. Improve your resume with more detailed experience and relevant skills."
    else:
        feedback = "Low match score. Consider updating your resume with job-relevant skills."

    st.info(feedback)

    # PDF Download
    st.subheader("📥 Download Full Report")
    pdf_bytes = generate_pdf(match_percent, matched_skills)

    st.download_button(
        label="📄 Download Report (PDF)",
        data=pdf_bytes,
        file_name="Resume_Analysis_Report.pdf",
        mime="application/pdf"
    )
