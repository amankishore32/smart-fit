"""AI Logic Module - Embeddings and Semantic Similarity Calculations.

This module provides the core semantic matching engine using Google's Generative AI API.
It handles text embeddings and calculates cosine similarity scores between vectors.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
from typing import List

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


class MatchEngine:
    """Semantic matching engine for comparing resumes with job descriptions.

    This class uses Google's embedding model to convert text into semantic vectors
    and calculates similarity scores using cosine similarity.
    """

    def get_embedding(self, text: str) -> List[float]:
        """Generate semantic embedding for input text.

        Args:
            text (str): The text to embed (resume or job description).

        Returns:
            List[float]: A vector representation of the text (1536 dimensions).

        Raises:
            Exception: If the API call fails or text is invalid.
        """
        # Fetch vector embedding from Google's text-embedding-004 model
        return genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )["embedding"]

    def calculate_score(self, v1: List[float], v2: List[float]) -> float:
        """Calculate semantic similarity score between two vectors.

        Uses cosine similarity metric and normalizes to 0-100 scale for readability.

        Args:
            v1 (List[float]): First embedding vector.
            v2 (List[float]): Second embedding vector.

        Returns:
            float: Similarity score ranging from 0 (no match) to 100 (perfect match).
        """
        # Cosine Similarity: (A·B) / (||A|| * ||B||)
        # Result is multiplied by 100 for human-readable percentage scoring
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        return (dot_product / (norm_v1 * norm_v2)) * 100
