from pydantic import BaseModel, Field

#Rules for what kind data API should accept
class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=1)

#Format of response
class AnalyzeResponse(BaseModel):
    match_score: int
    strengths: list[str]
    missing_skills: list[str]
    recommendations: list[str]
    match_analysis: str