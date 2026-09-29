from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.gemini import generate_legal_document
from app.pdf_generator import create_pdf
from app.docx_generator import create_docx

import os

app = FastAPI(title="LegalEase - AI Legal Document Generator")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

os.makedirs("generated", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": "",
            "document_type": "",
            "party_name": "",
            "details": ""
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    document_type: str = Form(...),
    party_name: str = Form(...),
    details: str = Form(...)
):
    result = generate_legal_document(
        document_type,
        party_name,
        details
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result,
            "document_type": document_type,
            "party_name": party_name,
            "details": details
        }
    )


@app.post("/download/pdf")
async def download_pdf(
    content: str = Form(...)
):
    path = create_pdf(content)

    return FileResponse(
        path,
        media_type="application/pdf",
        filename="LegalEase_Document.pdf"
    )


@app.post("/download/docx")
async def download_docx(
    content: str = Form(...)
):
    path = create_docx(content)

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="LegalEase_Document.docx"
    )