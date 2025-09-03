import os
import pytesseract
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pdf2image import convert_from_path
from PIL import Image, ImageFile

# Local project imports
from db.Database import SessionLocal
from Models.Model import Fileupload, Image, Summary

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ImageFile.LOAD_TRUNCATED_IMAGES = True

router = APIRouter()

# Directories
BASE_UPLOADS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
PDF_DIR = os.path.join(BASE_UPLOADS, "pdfs")
IMG_DIR = os.path.join(BASE_UPLOADS, "images")

# Make folders if not exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Poppler & Tesseract paths
poppler_path = r"C:\Users\Nitin\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@router.post("/hindi")
async def upload_hindi_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 1. Save uploaded PDF
        pdf_path = os.path.join(PDF_DIR, file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # 2. Create DB record for the PDF
        pdf_doc = Fileupload(filename=file.filename)
        db.add(pdf_doc)
        db.flush()  # assigns id

        # 3. Extract first page → save as PNG
        pages = convert_from_path(
            pdf_path, dpi=200, first_page=1, last_page=1, poppler_path=poppler_path
        )
        if not pages:
            raise HTTPException(status_code=500, detail="Could not extract image from PDF")

        image_filename = f"{file.filename}_page1.png"
        image_path = os.path.join(IMG_DIR, image_filename)
        pages[0].save(image_path, "PNG")

        new_img = Image(filename=image_filename, document_id=pdf_doc.id)
        db.add(new_img)

        # 4. Extract Hindi text from all pages
        all_pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        extracted_text = ""
        for page in all_pages:
            extracted_text += pytesseract.image_to_string(page, lang="hin") + "\n"

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No Hindi text found in PDF")

        # 5. Save extracted text (without summary)
        new_summary = Summary(
            filename=file.filename,
            content=extracted_text.strip(),
            summary=None,  # No summarization
            document_id=pdf_doc.id,
        )
        db.add(new_summary)

        # 6. Commit everything
        db.commit()
        db.refresh(pdf_doc)

        return {
            "document_id": pdf_doc.id,
            "filename": file.filename,
            "pdf_url": f"/uploads/pdfs/{file.filename}",
            "image_url": f"/uploads/images/{image_filename}",
            "hindi_text": extracted_text.strip(),
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
