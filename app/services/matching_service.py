import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.skill_model import SKILLS


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+#. ]+", " ", text.lower())


def extract_skills(text: str) -> list[str]:
    normalized_text = normalize_text(text)
    found_skills = set()

    for skill in SKILLS:
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized_text):
            found_skills.add(skill)

    return sorted(found_skills)


def calculate_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )

    vectors = vectorizer.fit_transform([
        resume_text,
        job_description,
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2],
    )[0][0]

    return float(similarity)


def find_relevant_experience(resume_text: str) -> list[str]:
    keywords = [
        "developed",
        "built",
        "implemented",
        "project",
        "experience",
        "worked",
        "managed",
    ]

    experience_lines = []

    for line in resume_text.splitlines():
        line = line.strip()

        if len(line) < 20:
            continue

        if any(keyword in line.lower() for keyword in keywords):
            experience_lines.append(line)

    return experience_lines[:8]


def analyze_resume(
    resume_text: str,
    job_description: str,
) -> dict:
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = sorted(
        set(resume_skills).intersection(required_skills)
    )

    missing_skills = sorted(
        set(required_skills).difference(resume_skills)
    )

    skill_match = (
        len(matched_skills) / len(required_skills)
        if required_skills else 0
    )

    semantic_similarity = calculate_similarity(
        resume_text,
        job_description,
    )

    score = round(
        (skill_match * 0.65 + semantic_similarity * 0.35) * 100
    )

    suggestions = [
        "Use measurable achievements, for example: improved speed by 30% or handled 1,000 users.",
        "Use job-description keywords only where they truthfully reflect your skills and experience.",
        "Keep important technical skills and relevant projects near the top of the resume.",
    ]

    if missing_skills:
        suggestions.insert(
            0,
            "Consider adding evidence of these missing skills if you have them: "
            + ", ".join(missing_skills[:6]),
        )

    return {
        "score": score,
        "semantic_similarity": round(semantic_similarity * 100),
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "relevant_experience": find_relevant_experience(resume_text),
        "suggestions": suggestions,
    }