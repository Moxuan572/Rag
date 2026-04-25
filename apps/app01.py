from fastapi import APIRouter, UploadFile, File,HTTPException
import os
from a_rag.vector_db import build_db


os.makedirs("upload_file", exist_ok=True)

app01 = APIRouter()


@app01.post("/UploadFile")
async def upload(file:UploadFile = File(...),file_name: str="temp.pdf"):
    try:
        files = await file.read()
        file_name = os.path.basename(file_name)
        path = os.path.join("upload_file",file_name)
        with open(path,"wb") as f:
            f.write(files)

        await build_db(path)

        return {"message":"上传成功并且数据库建好"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件处理失败：{str(e)}"
        )