from fastapi import APIRouter
from a_rag.vector_db import retrieve
from a_rag.prompts import llm

app02 = APIRouter()



@app02.get("/retrieve")
async def query(query: str):
    # 异步检索
    result = await retrieve(query)

    if not result:
        return {"message": "请输入正确的pdf"}


    res = await llm(result, query)

    return {"result": res}