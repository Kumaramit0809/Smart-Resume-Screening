from difflib import SequenceMatcher

def match_skills(resume_text, jd_text):
    resume_words = set(resume_text.split())
    jd_words = set(jd_text.split())

    matched_skills = list(resume_words.intersection(jd_words))
    match_percent = (len(matched_skills) / len(jd_words)) * 100
    return matched_skills, match_percent
