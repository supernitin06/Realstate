from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from db.Database import Base, engine
from router import  Allinone , Hindi # 👈 Import both

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
IMAGE_DIR = os.path.join("Imageextract", "pdfimages")
app.mount("/uploads/pdfs", StaticFiles(directory="uploads/pdfs"), name="pdfs")
app.mount("/uploads/images", StaticFiles(directory="uploads/images"), name="images")

# Routers
# app.include_router(Imageget.router , prefix="/images", tags=["Images"])
# app.include_router(PdfUpload.router, prefix="/pdf", tags=["PDF Upload"])
# app.include_router(Summry.router, prefix="/summary", tags=["PDF Upload"])
app.include_router(Allinone.router, prefix="/all", tags=["All DATA"])
app.include_router(Hindi.router, prefix="/hindi", tags=["All HINDI DATA"])


@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
