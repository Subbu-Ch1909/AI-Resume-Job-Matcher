# 🚀 AI Resume Matcher

An AI-powered web application that helps job seekers evaluate how well their resumes align with job descriptions using semantic similarity and Large Language Models (LLMs).

Unlike traditional keyword-based matching systems, AI Resume Matcher leverages Sentence Transformers for semantic understanding and the OpenAI API for intelligent skill extraction, enabling more meaningful resume-job compatibility analysis.

## 🌐 Live Demo
**Application**
https://ai-resume-matcher-c603.onrender.com

**API Documentation (Swagger UI):**
https://resume-matcher-api-d3axg2dnf0a9a3cp.centralus-01.azurewebsites.net

## 💡 Motivation
Job seekers often rely on ATS scanners or keyword matching tools that fail to capture the semantic relationship between a resume and a job description.

AI Resume Matcher was built to provide a more intelligent evaluation by combining semantic embeddings with Large Language Models. Instead of simply matching keywords, the application analyzes the contextual similarity between a candidate's experience and the job requirements, identifies strengths and missing skills, and generates actionable recommnedations.

## ✨ Features

- 📄 Upload resumes in PDF format
- 📝 Analyze resumes against any job description
- 🤖 AI-powered resume-job match scoring
- 🧠 Semantic similarity analysis using Sentence Transformers
- 💪 Identify technical strengths
- 🎯 Detect missing skills
- 💡 Generate personalized AI recommendations using OpenAI
- 📚 Interactive API documentation with Swagger UI
- ☁️ Fully deployed cloud application


## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- pdfplumber

### AI & Machine Learning
- OpenAI API
- Sentence Transformers
- Semantic Similarity
- Cosine Similarity

### Frontend
- HTML
- CSS
- JavaScript

### Cloud & DevOps
- Microsoft Azure App Service
- Render Static Site
- Git
- GitHub
- GitHub Actions (CI/CD)

## 🏗️ System Architecture
            User
        │
        ▼
Render Static Frontend
(HTML • CSS • JavaScript)
        │
 HTTPS POST /analyze-upload
        │
        ▼
Azure App Service
(FastAPI Backend)
        │
 ┌──────────────┬──────────────┐
 ▼                             ▼
Sentence Transformers      OpenAI API
        │
        ▼
Semantic Matching &
AI Recommendations
        │
        ▼
Match Score + Results
        │
        ▼
User Interface


# How it Works
1. Upload a resume in PDF format.
2. paste a job description.
3. The application extracts text from the uploaded PDF using pdfplumber.
4. Sentence Transformers generate semantic embeddings for the resume and job description.
5. The OpenAI API extracts technical strengths, identifies missing skills, and generates personalized recommendations.
6. The backend calculates an overall resume-job match score.
7. The analysis is returned to the frontend and displayed to the user.


# ☁️ Deployment
## Frontend
--> Hosted on Render Static Site.
## Backend
--> Hosted on Microsoft Azure App Service.

# Continuous Deployment
1. Github actions automatically deploys backend changes to Azure App Service.
2. Render automatically deploys frontend changes from GitHub repositoty.

# 📖 API Endpoint
## Analyze Resume
POST/analyze-upload

Input
1. Resume(PDF)
2. Job description

Returns
1. Match Score
2. Technical Strengths
3. Missing skills
4. AI-generated Recommendations

Interactive API documentation is available through Swagger UI

## Future Improvements
1. ATS compatibility scoring
2. Resume Keyword highlighting
3. AI-powered resume rewriting
4. Export analysis as PDF
5. User authentication
6. Resume history dashboard.
7. Docx resume support
8. Multiple job description comparision.


# 👨‍💻 Author
Doondi Chintalapudi

🎓 Master of Science in Data Analytics
Clark University

Passionate about AI, Machine Learning, Data Analytics, and building end-to-end intelligent applications.

