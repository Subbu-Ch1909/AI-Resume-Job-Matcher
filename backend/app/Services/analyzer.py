#Writing logic instead giving mock response
import re
from .embedding_matcher import compute_similarity, semantic_skill_match
from .llm_services import extract_resume_skills, extract_jd_skills, generate_recommendations, generate_match_analysis, validate_missing_skills





def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
#replace seperators
    skill = skill.replace("-", " ").replace("/", " ")
#replace extra spaces
    skill = re.sub(r"\s+", " ", skill)
    return skill


def analyze_resume_job(resume_text: str, job_description: str):
      
    #Normalize text: lowercase + collapse whitespace
    resume = re.sub(r"\s+", " ", resume_text.lower().strip())
    jd = re.sub(r"\s+"," ", job_description.lower().strip())

    #AI based skill extraction
    resume_skills = set(normalize_skill(s) for s in extract_resume_skills(resume))
    jd_skills = set(normalize_skill(s) for s in extract_jd_skills(jd))

    #semantic match
    skill_match_result = semantic_skill_match(resume_skills, jd_skills, threshold=0.65)
    
    #Compare Extracted skills
    strengths = skill_match_result["matched_skills"]
    missing_skills = skill_match_result["missing_skills"]

    missing_skills = validate_missing_skills(
        resume_text,
        missing_skills
    )



    #Compute match score safely
    if not jd_skills:
        match_score = 0
    else:
        match_score =round((len(strengths)/len(jd_skills))*100)
    #Embedding Similarity    
    embedding_result = compute_similarity(resume, jd)
    similarity_score = embedding_result["best_score"]                                      #Extracts only the numeric values instead of whole dict from the embedding matcher return statement.
   
   #Final Hybrid Score
    final_score = round((match_score* 0.6) + similarity_score * 100 * 0.4)
    print("Rule Score:", match_score)
    print("Embedded Score:", similarity_score)
    print("Final score:", final_score)
    print("Best Resume Chunk:", embedding_result["best_resume_chunk"])
    print("Best JD Chunk:", embedding_result["best_jd_chunk"])
    
    #LLM based Recommendations
    recommendations = generate_recommendations(final_score, strengths, missing_skills)

    if not recommendations:
        recommendations = [
            "Consider adding missing skills to your resume.",
            "Tailor resume bullets to match the job description."
        ]
    #LLM based contextual analysis
    match_analysis = generate_match_analysis(
        resume_text=resume_text,
        job_description=job_description,
        match_score=final_score,
        strengths=strengths,
        missing_skills=missing_skills
    )


    return {
    "match_score": final_score,
    "strengths":strengths,
    "missing_skills":missing_skills,
    "recommendations": recommendations,
    "match_analysis": match_analysis,
}