# SmartFit AI - Semantic Resume Matcher

SmartFit AI is a powerful tool that uses Google's Generative AI to semantically match candidate resumes against job descriptions. Unlike keyword-based matchers, SmartFit understands the context and meaning of skills and experiences to provide a more accurate ranking of candidates.

Validates the resume against the Job Description(JD). Simply provide the JD shared and upload the resume(s) and let the AI do its magic. Get the score of your Resumé alignment with JD.

## Features

- **Semantic Matching**: Uses Google's `text-embedding-004` model to understand context.
- **Resume Parsing**: Extracts text from PDF resumes.
- **Ranked Results**: Provides a scored list of candidates based on relevance.
- **Dual Interface**:
  - **CLI**: Simple command-line interface for quick testing with mock data.
  - **REST API**: FastAPI-based server for integrating with frontend applications.

## Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- A Google Cloud API Key with access to Generative AI (Gemini)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/amankishore32/smart-fit.git
   cd smart-fit
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

## Configuration

1. Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```

2. Add your Google API Key to the `.env` file:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Usage

### 1. Command Line Interface (CLI)
Run the CLI to match mock candidates against a sample job description:

```bash
poetry run python main.py
```

### 2. REST API Server
Start the FastAPI server to handle file uploads and real-time matching:

```bash
poetry run python api.py
```

The server will start at `http://0.0.0.0:8000`.
You can access the interactive API documentation at `http://localhost:8000/docs`.

## Project Structure

```
smart-fit/
├── api.py           # FastAPI server endpoints
├── data.py          # Mock data for testing
├── engine.py        # Core AI matching logic
├── main.py          # CLI entry point
├── utils.py         # Utility functions (PDF extraction)
├── pyproject.toml   # Project dependencies
├── README.md        # Project documentation
└── .env             # Environment variables (not committed)
```

## Author

**Aman Kishore Agarwal**
