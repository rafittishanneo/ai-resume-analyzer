import io
import re

import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "javascript",
    "typescript",
    "php",
    "java",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "vue",
    "angular",
    "node.js",
    "fastapi",
    "django",
    "flask",
    "laravel",
    "git",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "opencv",
    "mediapipe",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "rest api",
    "graphql",
    "rfid",
    "linux",
    "communication",
    "leadership",
    "project management",
]


ALIASES = {
    "js": "javascript",
    "node": "node.js",
    "postgres": "postgresql",
    "ml": "machine learning",
    "natural language processing": "nlp",
    "rest": "rest api",
}


def extract_pdf_text(file_data: bytes) -> str:
    document = fitz.open(
        stream=io.BytesIO(file_data),
        filetype="pdf",
    )

    pages = [page.get_text() for page in document]
    return "\n".join(pages).strip()


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+#. ]+", " ", text.lower())


def extract_skills(text: str) -> list[str]:
    normalized = normalize_text(text)
    detected = set()

    for skill in SKILLS:
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized):
            detected.add(skill)

    for alias, actual_skill in ALIASES.items():
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(alias)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized):
            detected.add(actual_skill)

    return sorted(detected)


def semantic_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    return float(
        cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]
    )


def find_relevant_experience(text: str) -> list[str]:
    keywords = [
        "experience",
        "developed",
        "built",
        "managed",
        "implemented",
        "project",
        "worked",
    ]

    results = []

    for line in text.splitlines():
        cleaned = line.strip()

        if len(cleaned) < 20:
            continue

        if any(
            keyword in cleaned.lower()
            for keyword in keywords
        ):
            results.append(cleaned)

    return results[:8]


def analyze_resume(
    resume_file: bytes,
    job_description: str,
) -> dict:
    resume_text = extract_pdf_text(resume_file)

    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = sorted(
        set(resume_skills).intersection(required_skills)
    )

    missing_skills = sorted(
        set(required_skills).difference(resume_skills)
    )

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        )
    else:
        skill_score = 0

    similarity = semantic_similarity(
        resume_text,
        job_description,
    )

    match_score = round(
        (skill_score * 0.65 + similarity * 0.35) * 100
    )

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Add evidence for: "
            + ", ".join(missing_skills[:6])
            + "."
        )

    suggestions.extend(
        [
            "Quantify achievements using percentages, time saved, "
            "revenue, or project scale.",
            "Use job-description terminology when it accurately "
            "describes your experience.",
            "Place your strongest relevant projects and technologies "
            "near the top of the resume.",
        ]
    )

    return {
        "score": match_score,
        "semantic_similarity": round(similarity * 100),
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "relevant_experience": find_relevant_experience(
            resume_text
        ),
        "suggestions": suggestions,
        "resume_text": resume_text[:12000],
    }