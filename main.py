from fastapi import FastAPI
import uvicorn
from apps.app01 import app01
from apps.app02 import app02

app = FastAPI(title="langchain_rag")

app.include_router(app01,tags=["上传PDF"])
app.include_router(app02,tags=["检索"])

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8080,reload=True)