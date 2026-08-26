from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    score: int
    semantic_similarity: int
    resume_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    relevant_experience: list[str]
    suggestions: list[str]