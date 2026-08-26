from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.matching_service import analyze_resume
from app.services.pdf_service import extract_text_from_pdf


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(
    directory=str(BASE_DIR / "views" / "templates")
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post("/api/analyze")
async def analyze_resume_route(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    pdf_data = await resume.read()

    if len(pdf_data) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF size must be under 10 MB.",
        )

    try:
        resume_text = extract_text_from_pdf(pdf_data)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in this PDF.",
            )

        return analyze_resume(
            resume_text=resume_text,
            job_description=job_description,
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(error)}",
        )