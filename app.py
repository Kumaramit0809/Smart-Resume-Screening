import streamlit as st
import spacy
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_matcher import match_skills

st.title("🧠 Smart Resume Screening using NLP")

import en_core_web_sm
nlp = en_core_web_sm.load()

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if uploaded_file and job_description:
        resume_text = extract_text_from_pdf(uploaded_file)
        cleaned_resume = clean_text(resume_text)

        jd_cleaned = clean_text(job_description)
        matched_skills, match_percent = match_skills(cleaned_resume, jd_cleaned)

        st.subheader("✅ Resume Match Result")
        st.write(f"**Match Percentage:** {match_percent:.2f}%")
        st.write("**Matched Skills:**", ", ".join(matched_skills))
    else:
        st.warning("Please upload a resume and paste a job description.")
