from fastapi import APIRouter, UploadFile, File
import os
from a_rag.vector_db import build_db  # 内部我也会帮你改成异步调用

file_paths = None
os.makedirs("file_upload", exist_ok=True)

app01 = APIRouter()


@app01.post("/UploadFile")
async def upload(file: UploadFile = File(...), file_name: str = "temp.pdf"):
    global file_paths

    files = await file.read()

    file_paths = os.path.join("file_upload", file_name)
    with open(file_paths, "wb") as f:
        f.write(files)

    await build_db(file_paths)

    return {"file_name": file_name}