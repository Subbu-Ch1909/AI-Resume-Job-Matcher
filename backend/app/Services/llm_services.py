from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import ast
import re

env_path = Path(__file__).resolve().parents[2]/".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_skills_response(result: str):
    if not result:
        return []
    
    cleaned = result.strip()

    #remove markdown code fences if present
    cleaned = re.sub(r"^```(?:python)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        skills_list = ast.literal_eval(cleaned)
        if isinstance(skills_list, list):
            return [str(skill).lower().strip() for skill in skills_list]
    except:
        pass
    return[]

def extract_resume_skills(resume_text: str):
    prompt = f"""
    Extract all technical skills, tools, programming languages, frameworks, and platforms and relevant technical competencies from the following resume. 
    Return only a python list of skills.

    Important:
    Return skills in standardized / canonical form.
    Expand abbreviations when appropriate.
    Normalize plural/ singular wording when appropriate.
    Prefer commonly understood full-forn technical names.

    Example:
    "OS" -> "operating system"
    "REST APIs" -> "rest api development"
    "LLMS" -> "large language model"
    

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You extract structured skill data from resumes."
            },
            {
                "role": "user",
                "content":prompt
            }
        ]
    )
    result = response.choices[0].message.content
    print("Resume skills raw response:", result)

    return parse_skills_response(result)


def extract_jd_skills(job_description: str):
    prompt = f"""
    Extract all required and preffered technical skills, tools, programming languages, frameworks and platforms, and relevant competencies from the following job description.PermissionError

    Return ONLY a python list of skills.
    Example:
    ["java", "spring boot", "docker", "kubernetes"]
    Do not include explanations. 

    Important:
    Return skills in standardized / canonical form.
    Expand abbreviations when appropriate.
    Normalize plural/ singular wording when appropriate.
    Prefer commonly understood full-forn technical names.

     Example:
    "OS" -> "operating system"
    "REST APIs" -> "rest api development"
    "LLMS" -> "large language model"

    Job Description:
    {job_description}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You extract structured skills data from the job descriptions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    print("JD skills raw response:", result)

    return parse_skills_response(result)

def generate_recommendations(match_score, strengths, missing_skills):
    prompt = f"""
    You are an expert resume reviewer. 

    A candidate has:
    Match Score: {match_score}%
    Strengths: {','.join(strengths) if strengths else 'None'}
    Missing Skills: {','.join(missing_skills) if missing_skills else 'None'}

    Provide 3 to 5 concise, actionable recommendations to improve the resume for better alignment with the job description. 

    Return ONLY a Python list of strings.
    Example:
    ["Highlight Java backend experience more clearly", Add evidence of Kubernetes Work", "Use job description keywords more directly"]"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate structures resume improvement suggestions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    result = response.choices[0].message.content
    print("Recommendations raw response:", result)

    return parse_skills_response(result)

def generate_match_analysis(
        resume_text: str,
        job_description: str,
        match_score: int,
        strengths: list,
        missing_skills: list
):
    prompt = f"""
    You are an AI resume-job matching assistant.

    Analyze the candidate's resume against the job description using context, not only exact skills.

    Consider:
    -direct skill matches
    -project experience
    -transferable skills
    -implied analytical or technical experience
    -missing or weak areas

    Current system results:
    Match Score: {match_score}%
    Strengths: {', '.join(strengths) if strengths else 'None'}
    Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

    Resume: {resume_text}
    Job Description: {job_description}


    Provide a concise explanation of
    1. Why the candidate matches the role
    2. Why the score may be limited.
    3. What the candidate should improve

    Return ONLY a plain text explanation."""

    
    response = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You provide contextual resume-job match analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def validate_missing_skills(
        resume_text: str,
        missing_skills: list[str]
):
    prompt = f"""

    You are reviewing a resume.

    Resume:
    {resume_text}

    The current system identified these missing skills:

    {missing_skills}

    Remove any skills that are actually demonstrated through:
    - projects
    - experience
    - equivalent technology
    - related technologies

    Return ONLY a Python list of skills that are truly missing."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": " You validate missing skills in resume."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    result = response.choices[0].message.content
    print("Validated missing skills raw response:", result)

    validate_missing_skills = parse_skills_response(result)

    if not validate_missing_skills:
        return missing_skills
    
    return validate_missing_skills

