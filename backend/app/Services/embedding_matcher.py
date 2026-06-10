from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#Load pre-trained model
model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


#Adding a Chunking Helper
def chunk_text(text:str, chunk_size: int = 300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def compute_similarity(resume: str, jd: str):
    """
    compute semantic similarity between resume and job description
    using chunk-based embedding
    """

    resume_chunks = chunk_text(resume)
    jd_chunks = chunk_text(jd)

    
    resume_embedding = get_model().encode(resume_chunks)
    jd_embedding = get_model().encode(jd_chunks)

    #Calculate Cosine Similarity
    similarity_matrix= cosine_similarity(resume_embedding, jd_embedding)
    best_score = similarity_matrix.max()

    #Checking which resume chunk is best matchedd with best JD chunk
    best_resume_index, best_jd_index = divmod(
        similarity_matrix.argmax(),
        similarity_matrix.shape[1]
    )
    best_resume_chunk = resume_chunks[best_resume_index]
    best_jd_chunk = jd_chunks[best_jd_index]
    return {
        "best_score": best_score,
        "best_resume_chunk": best_resume_chunk,
        "best_jd_chunk": best_jd_chunk
    }


def semantic_skill_match(resume_skills, jd_skills, threshold: float = 0.65):
    if not resume_skills or not jd_skills:
        return{
            "matched_skills": [],
            "missing_skills": list(jd_skills)
        }
    resume_skills = list(resume_skills)
    jd_skills = list(jd_skills)

    resume_skills_embedding = get_model().encode(resume_skills)
    jd_skills_embedding = get_model().encode(jd_skills)

    similarity_matrix_skills = cosine_similarity(resume_skills_embedding, jd_skills_embedding)

    matched_jd_skills = set()

    for i, resume_skill in enumerate(resume_skills):
        for j, jd_skill in enumerate(jd_skills):
            if similarity_matrix_skills[i][j] >= threshold:
                matched_jd_skills.add(jd_skill)
    missing_skills = [skill for skill in jd_skills if skill not in matched_jd_skills]

    return{
        "matched_skills": sorted(list(matched_jd_skills)),
        "missing_skills": sorted(missing_skills)
    }