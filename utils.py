"""Utility Module for PDF Processing and Text Extraction.

Provides asynchronous functions for reading and processing PDF files.
Used by the FastAPI server to extract resume text from uploaded PDF documents.

Author: Aman Kishore Agarwal
Version: 1.0.0
"""

import io
from pypdf import PdfReader
from fastapi import UploadFile


async def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text content from an uploaded PDF file.

    Asynchronously reads a PDF file, extracts text from all pages,
    and returns the concatenated text content.

    Args:
        file (UploadFile): The uploaded PDF file from FastAPI.

    Returns:
        str: Extracted text content from all PDF pages, with newlines between pages.

    Note:
        - Uses async/await to prevent blocking the event loop
        - Handles empty PDFs gracefully
        - Resets file pointer for potential re-reading
    """
    # Step 1: Asynchronously read the file content
    # Using 'await' allows the server to handle other requests while reading
    content = await file.read()

    # Step 2: Wrap file content in BytesIO object (pypdf expects file-like object)
    pdf_stream = io.BytesIO("None" if len(content) == 0 else content)

    # Step 3: Parse the PDF document
    reader = PdfReader(pdf_stream)

    # Step 4: Extract text from all pages
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + '\n'

    # Step 5: Reset file cursor position (in case file needs to be read again)
    await file.seek(0)

    return text
