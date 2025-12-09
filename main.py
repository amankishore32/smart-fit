"""Command-Line Interface (CLI) for SmartFit Resume Matching Engine.

Provides a simple CLI interface to run semantic matching between job descriptions
and candidate resumes, displaying ranked results in a formatted table.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

from tabulate import tabulate
from data import CANDIDATES, JOB_DESCRIPTION
from engine import MatchEngine


def main() -> None:
    """Execute the main CLI workflow for candidate matching.

    Workflow:
    1. Initialize the semantic matching engine
    2. Generate embedding for job description
    3. Process each candidate resume
    4. Calculate fit scores using cosine similarity
    5. Display ranked results in a formatted table
    """
    print("Initializing Smartfit AI Engine...")
    engine = MatchEngine()

    # Step 1: Vectorize the Job Description (JD)
    print("Analyzing Job Description...")
    jd_vector = engine.get_embedding(JOB_DESCRIPTION)

    results = []

    # Step 2: Vectorize and Rank Candidates
    print(f"Scanning {len(CANDIDATES)} candidates...")

    for candidate in CANDIDATES:
        # Generate semantic embedding for candidate resume
        resume_vector = engine.get_embedding(candidate["resume"])

        # Calculate semantic fit score (0-100)
        score = engine.calculate_score(jd_vector, resume_vector)

        # Store result: [Name, Score, Resume Preview]
        results.append(
            [candidate["name"], f"{score:.2f}", candidate["resume"][:50] + "..."])

    # Sort results by score in descending order (highest match first)
    results.sort(key=lambda x: float(x[1].strip('%')), reverse=True)

    # Display formatted results
    print("\n MATCHING RESULTS: ")
    print(tabulate(results, headers=[
        "Candidate", "Match Score", "Resume Snippet"], tablefmt="grid"))


if __name__ == "__main__":
    main()
