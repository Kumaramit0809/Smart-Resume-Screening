from utils.skills_list import TECH_SKILLS

def match_skills(cleaned_resume, cleaned_jd):
    resume_words = set(cleaned_resume.split())
    jd_words = set(cleaned_jd.split())

    # ONLY match real tech skills
    matched = []

    for skill in TECH_SKILLS:
        if skill.lower() in resume_words and skill.lower() in jd_words:
            matched.append(skill)

    match_percent = (len(matched) / len(TECH_SKILLS)) * 100

    return matched, match_percent
