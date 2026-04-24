from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def llm(context,question):
    prompt = f"""
请根据下面的上下文回答问题，不要编造内容。
上下文：
{context}

问题：{question}
回答：
    """
    response = await client.chat.completions.create(
        model = "qwen-turbo",
        messages = [{"role":"user","content":prompt}],
        stream = False
    )
    return response.choices[0].message.content


