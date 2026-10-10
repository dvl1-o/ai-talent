import os
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


class MatchResult(BaseModel):
    skills_score: float = Field(description="0-100 score based on skills overlap")
    experience_score: float = Field(description="0-100 score based on relevant experience")
    education_score: float = Field(description="0-100 score based on education relevance")
    semantic_score: float = Field(description="0-100 overall semantic fit between candidate and job")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    explanation: str = Field(description="Short human-readable explanation for the recruiter")


# Pondération — volontairement centralisée ici pour pouvoir évoluer facilement
# sans toucher au reste de la logique (voir doc section 24 : ne pas figer en dur).
WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "education": 0.15,
    "semantic": 0.20,
}


def calculate_final_score(result: MatchResult) -> float:
    return round(
        result.skills_score * WEIGHTS["skills"]
        + result.experience_score * WEIGHTS["experience"]
        + result.education_score * WEIGHTS["education"]
        + result.semantic_score * WEIGHTS["semantic"],
        2,
    )


def match_candidate_to_job(candidate_profile_text: str, job_description: str, required_skills: List[str]) -> MatchResult:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
    )
    structured_llm = llm.with_structured_output(MatchResult)

    prompt = (
        "You are an assistant helping a recruiter evaluate a candidate for a job. "
        "Compare the candidate's profile with the job requirements and score each "
        "dimension from 0 to 100. Be honest and base your assessment only on the "
        "information provided — never invent facts about the candidate.\n\n"
        f"JOB DESCRIPTION:\n{job_description}\n\n"
        f"REQUIRED SKILLS:\n{', '.join(required_skills)}\n\n"
        f"CANDIDATE PROFILE:\n{candidate_profile_text}"
    )

    return structured_llm.invoke(prompt)