import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pdf2image import convert_from_path
import pdfplumber
from transformers import pipeline
from schemas import schema

from db.Database import SessionLocal
from Models.Model import Image, Fileupload, Summary

# Init
router = APIRouter()
BASE_UPLOADS = "uploads"
PDF_DIR = os.path.join(BASE_UPLOADS, "pdfs")
IMG_DIR = os.path.join(BASE_UPLOADS, "images")

# Make folders if not exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

poppler_path = r"C:\Users\Nitin\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

# ⚠️ Change summarizer model if Hindi support is needed
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/addpdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 1. Save PDF file in pdfs folder
        pdf_path = os.path.join(PDF_DIR, file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # 2. Create DB record for the file
        pdf_doc = Fileupload(filename=file.filename)
        db.add(pdf_doc)
        db.flush()  # assign id

        # 3. Extract first page as image & save in images folder
        pages = convert_from_path(
            pdf_path, dpi=200, first_page=1, last_page=1, poppler_path=poppler_path
        )
        if not pages:
            raise HTTPException(status_code=500, detail="Could not extract image from PDF")

        image_filename = f"{file.filename}_page1.png"
        image_path = os.path.join(IMG_DIR, image_filename)
        pages[0].save(image_path, "PNG")

        new_img = Image(
            filename=image_filename,
            document_id=pdf_doc.id,
        )
        db.add(new_img)

        # 4. Extract text using pdfplumber (instead of OCR)
        text = ""
        
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:5]:  # limit to first 5 pages
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # 5. Summarize text
        summary_result = summarizer(
            text[:1000], max_length=130, min_length=30, do_sample=False
        )
        summary = summary_result[0]["summary_text"]

        # 6. Save summary
        new_summary = Summary(
            filename=file.filename,
            content=text,
            summary=summary,
            document_id=pdf_doc.id,
        )
        db.add(new_summary)

        # ✅ Commit once
        db.commit()
        db.refresh(pdf_doc)

        return {
            "document_id": pdf_doc.id,
            "filename": file.filename,
            "summary": summary,
            "pdf_url": f"/uploads/pdfs/{file.filename}",
            "image_url": f"/uploads/images/{image_filename}",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pdfs", response_model=list[schema.PDFBase])
def get_all_pdfs(db: Session = Depends(get_db)):
    pdfs = db.query(Fileupload).all()
    return pdfs
