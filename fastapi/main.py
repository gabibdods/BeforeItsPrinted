from fastapi import FastAPI, UploadFile, File
from pdf import parse_pdf
from image import parse_image
from word import parse_docx
from txt import parse_txt
import os, shutil
import tempfile

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/parse/")
async def parse_uploaded_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    temp_path = f"/tmp/{file.filename}"

    with tempfile.NamedTemporaryFile(delete = False, suffix = ext) as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    if ext == ".pdf":
        result = parse_pdf(temp_path)
    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        result = parse_image(temp_path)
    elif ext == ".docx":
        result = parse_docx(temp_path)
    elif ext == ".txt":
        result = parse_txt(temp_path)
    else:
        os.remove(temp_path)
        return {"error": "Unsupported file type"}

    os.remove(temp_path)
    return result
# fastapi, uvicorn, pdfplumber, python-docx, pytesseract, pillow, python-multipart