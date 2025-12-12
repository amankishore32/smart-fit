"""
SmartFit AI - Semantic Resume Matcher UI

This module provides the Streamlit frontend for the SmartFit AI application.
It allows users to:
1. Input a job description
2. Upload multiple PDF resumes
3. Get semantic rankings of candidates based on relevance to the job

The application communicates with a FastAPI backend at http://localhost:8000
to perform the semantic matching using Google's Generative AI embeddings.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

import streamlit as st
import requests
import pandas as pd

# Backend API endpoint for ranking candidates
API_URL = "http://localhost:8000/rank-candidates"

# Configure Streamlit page settings
st.set_page_config(page_title="SmartFit AI", layout="wide")

# --- HEADER ---
st.title("SmartFit: Semantic Resume Matcher")
st.markdown("""
**Stop matching Keywords.** Match meaning.
            This tool uses **Gemini Pro** to vectorise your job Description and Candidates,
            ranking them by semantic relevance.
""")

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    st.header("1. Define the Role")
    # Text area for job description input
    job_description = st.text_area(
        "Paste Job Description: ",
        placeholder="e.g. We need a Senior Python Engineer with experience in Microservices..."
    )

    st.header("2. Upload Candidates")
    # File uploader for PDF resumes (supports multiple files)
    uploaded_files = st.file_uploader(
        "Uploaded Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Main action button to trigger analysis
    run_btn = st.button("Analyse & Rank", type="primary")

    # --- MAIN AREA (Results) ---
    if run_btn:
        # Validate user inputs
        if not job_description or not uploaded_files:
            st.error("Please provide both a JD and at least one resume.")
        else:
            # Show loading spinner while processing
            with st.spinner(f"Reading {len(uploaded_files)} resumes & consulting Gemini..."):
                # Prepare the multipart form data for API request
                files = []
                for file in uploaded_files:
                    # Streamlit file object needs to be converted to tuple format for requests library
                    files.append(
                        ("files", (file.name, file.getvalue(), "application/pdf"))
                    )
                payload = {"job_description": job_description}

                # Call the FastAPI backend to get rankings
                try:
                    response = requests.post(
                        API_URL, data=payload, files=files)

                    # Process successful response from backend
                    if response.status_code == 200:
                        data = response.json()["matches"]

                        # Display the top candidate match with score
                        top_candidate = data[0]
                        st.success(
                            f"Top Match: **{top_candidate['filename']}** ({round(top_candidate['score'],2)}%)")

                        # Create and format results dataframe
                        df = pd.DataFrame(data)
                        df = df[['filename', 'score', 'preview', 'status']]

                        # Display results with color-coded gradient highlighting (green for higher scores)
                        st.dataframe(
                            df.style.background_gradient(
                                subset=["score"], cmap="Greens"),
                            use_container_width=True
                        )

                        # Optional: Show raw JSON response for debugging
                        with st.expander("View Raw JSON Logic"):
                            st.json(data)
                    else:
                        # Handle server errors
                        st.error(f"Server Error: {response.text}")
                except Exception as e:
                    # Handle connection errors or other exceptions
                    st.error(
                        f"Failed to connect to backend. Is it runnning? Error: {e}")
