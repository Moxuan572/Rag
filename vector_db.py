from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.vectorstores import FAISS

embed_model = HuggingFaceEmbeddings(
    model_name=r"D:\rag_model\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
)


async def build_db(file_paths):
    loader = PyMuPDF4LLMLoader(file_path=file_paths)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=25,
        separators=["\n\n", "\n", "。", "，", " ", ""]
    )

    splits = splitter.split_documents(docs)


    db = await FAISS.afrom_documents(splits, embed_model)
    db.save_local("faiss_db")
    print("success")


def load_vector():
    db = FAISS.load_local(
        folder_path="faiss_db",
        embeddings=embed_model,
        allow_dangerous_deserialization=True
    )
    return db


async def retrieve(query: str, top_k=3):
    db = load_vector()

    docs = await db.asimilarity_search(query, k=top_k)
    if not docs:
        return []
    result_text = "\n".join([doc.page_content for doc in docs])
    return result_text