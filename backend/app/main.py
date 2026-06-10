from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from .schemas import AnalyzeRequest, AnalyzeResponse
from .Services.analyzer import analyze_resume_job
from dotenv import load_dotenv
from pathlib import Path
import os
from openai import OpenAI
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware


env_path = Path(__file__).resolve().parents[1]/ ".env"

load_dotenv(dotenv_path=env_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return{"status": "API is running"}

#defining a route
@app.get("/")
def root():
    return{"message":"Welcome-API is running.Go to /docs"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    result = analyze_resume_job(
        payload.resume_text,
        payload.job_description
    )

    return AnalyzeResponse(**result)


def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

@app.post("/analyze-upload", response_model=AnalyzeResponse)
async def analyze_upload_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail = "Only PDF files are supported.")
    try:
        resume_text = extract_text_from_pdf(resume_file.file)

        if not resume_text:
            raise HTTPException(status_code = 400, detail="Could not extract text from PDF.")
        result = analyze_resume_job(resume_text, job_description)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/test-openai")
def test_openai():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": "Say: OpenAI connection successful"
                }
            ]
        )
        return{
            "message": response.choices[0].message.content
        }
    except Exception as e:
        return{
            "error": str(e)
        }
    
