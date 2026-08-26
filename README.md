# AI Resume Analyzer

An AI-powered web application that analyzes a PDF resume against a job description.

The application extracts resume text, detects technical skills, compares them with job requirements, calculates a match score, identifies missing skills, and provides resume improvement suggestions.

## Features

- Upload and parse PDF resumes
- Extract text using PyMuPDF
- Detect technical and soft skills
- Compare resume skills with job-description skills
- Calculate a resume match score
- Measure semantic similarity
- Identify missing skills
- Detect relevant experience lines
- Generate improvement suggestions
- MVC project architecture
- FastAPI backend with HTML, CSS, and JavaScript frontend

## Tech Stack

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Scikit-learn
- Jinja2
- HTML
- CSS
- JavaScript

## Project Structure

```text
app/
├── controllers/
│   └── resume_controller.py
├── models/
│   ├── resume_model.py
│   └── skill_model.py
├── services/
│   ├── pdf_service.py
│   └── matching_service.py
├── views/
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       └── js/
└── main.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/rafittishanneo/ai-resume-analyzer.git
cd ai-resume-analyzer
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Project

```bash
python -m uvicorn app.main:app --reload
```

Open the application in a browser:

```text
http://127.0.0.1:8000
```

## How It Works

1. Upload a PDF resume.
2. Paste a job description.
3. The system extracts text from the PDF.
4. The system detects skills from both the resume and job description.
5. The application calculates matched skills, missing skills, semantic similarity, and an overall match score.
6. The dashboard displays suggestions for improving the resume.

## Future Improvements

- SentenceTransformer embeddings
- spaCy EntityRuler skill extraction
- LLM-powered resume feedback
- ChromaDB vector database
- Resume analysis history
- User authentication
- PDF report export
- OCR support for scanned PDF resumes

## License

This project is licensed under the MIT License.
