from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf import parse_pdf
from image import parse_image
from word import parse_docx
from txt import parse_txt
import os, shutil
import tempfile

app = FastAPI()

origins = [
    "http://localhost:9000",
    "http://127.0.0.1:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/parse/")
async def parse_uploaded_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    file.file.seek(0)

    temp_path = f"/tmp/{file.filename}"

    with tempfile.NamedTemporaryFile(delete = False, suffix = ext) as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    try:
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
    except Exception as error:
        return {"internal server error": str(error)}

    os.remove(temp_path)
    return result