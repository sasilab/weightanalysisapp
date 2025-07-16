# gripper_ranker/app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.weightapp.utils import extract_text_from_pdf, parse_parameters
from src.weightapp.crud import save_gripper_data
from src.weightapp.models import init_db
import shutil
import os

import tempfile



temp_dir = tempfile.gettempdir()

app = FastAPI()

# Allow Gradio to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    #file_path = f"/tmp/{file.filename}"
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    os.remove(file_path)
    parameters = parse_parameters(text)

    gripper_id = save_gripper_data(file.filename, parameters)
    return {"gripper_id": gripper_id, "parameters": parameters}
