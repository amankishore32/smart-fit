"""FastAPI Server for SmartFit Semantic Resume Matching Service.

Provides REST API endpoints for matching candidates to job descriptions
using semantic embeddings and cosine similarity scoring.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

from typing import List
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
import uvicorn

from engine import MatchEngine
from utils import extract_text_from_pdf


# Initialize FastAPI application with metadata
app = FastAPI(title="SmartFit AI", description="Semantic Resume Matcher")

# Initialize the semantic matching engine (instantiated once for performance)
engine = MatchEngine()


@app.post("/rank-candidates")
async def rank_candidates(
    # Accepts job description as text input
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)     # Accepts multiple PDF resume files
) -> dict:
    """Rank candidates by semantic similarity to job description.

    Workflow:
    1. Receive job description text from form
    2. Receive list of resume PDFs from file upload
    3. Extract text from each PDF resume
    4. Generate embeddings for all documents
    5. Calculate similarity scores using cosine similarity
    6. Return ranked results with scores

    Args:
        job_description (str): The target job description text.
        files (List[UploadFile]): List of PDF resume files to process.

    Returns:
        dict: Dictionary containing ranked results with scores and status information.

    Raises:
        HTTPException: If API error occurs during embedding generation.
    """

    results = []

    # Step 1: Vectorize Job Description (JD)
    try:
        print("Vectorizing JD...")
        jd_vector = engine.get_embedding(job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API error: {str(e)}")

    # Step 2: Process each Resume
    print(f"Processing {len(files)} files...")

    for file in files:
        # 2A. Validate file type
        if file.content_type != "application/pdf":
            results.append({"filename": file.filename,
                           "score": 0, "status": "Skipped (Not PDF)"})
            continue

        # 2B. Extract text from PDF
        resume_text = await extract_text_from_pdf(file)

        # 2C. Validate extracted text
        if len(resume_text) < 50:
            results.append({"filename": file.filename,
                           "score": 0, "status": "Error (Empty PDF)"})
            continue

        # 2D. Generate embedding for resume
        resume_vector = engine.get_embedding(resume_text)

        # 2E. Calculate semantic similarity score
        score = engine.calculate_score(jd_vector, resume_vector)

        # 2F. Append result with metadata
        results.append({
            "filename": file.filename,
            "score": score,
            "preview": resume_text[:100] + "...",
            "status": "Success"
        })

    # Step 3: Sort results by score in descending order (highest match first)
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"matches": sorted_results}


if __name__ == "__main__":
    # Run server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
