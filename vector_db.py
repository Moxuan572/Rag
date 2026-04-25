from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder

size = 800
lap = 120
db = None

model_embed = HuggingFaceEmbeddings(
    model_name = r"D:\rag_model\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
)

model_rank = CrossEncoder(
    model_name_or_path = r"D:\rag_model\rank_model"
)

#  ------------------------------建库--------------------------------
async def build_db(path):
    global db,size,lap
    loader = PyMuPDF4LLMLoader(file_path=path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = size,
        chunk_overlap = lap,
        separators = ["\n\n","\n","。","，"," ",""]
    )

    splits = splitter.split_documents(docs)

    db = await FAISS.afrom_documents(splits,model_embed)
    db.save_local("faiss_db")

# --------------------------多路召回-------------------------------
async def multi_recall(query, top_k=15):
    docs1 = await db.asimilarity_search(query, k=top_k)
    #  MMR 最大边际相关性
    docs2 = await db.amax_marginal_relevance_search(query, k=top_k)

    # 合并去重
    all_docs = []
    seen = set()
    for doc in docs1 + docs2:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            all_docs.append(doc)

    print(f"多路召回完成，共 {len(all_docs)} 条")
    return all_docs

#---------------------------重排序-------------------------------
def rerank(query, docs, top_n=3):
    pairs = [[query,doc.page_content] for doc in docs]
    scores = model_rank.predict(pairs)

    ranked = sorted(zip(docs,scores),key=lambda x:x[1],reverse=True)
    top_docs = [temp[0] for temp in ranked[:top_n]]
    return top_docs

#-----------------------RAG检索--------------------------------------
async def retrieve(query):
    global db
    if not db:
        try:
            db = FAISS.load_local("faiss_db",model_embed,allow_dangerous_deserialization=True)
        except:
            print("请先建数据库")
            return ""

    recall_docs = await multi_recall(query,top_k=15)
    final_docs = rerank(query, recall_docs, top_n=3)
    return "\n".join([doc.page_content for doc in final_docs])


# ---------------------------测试上传的pdf哪个size overlap合适--------------
def test_chunk_size(path, chunk_size, chunk_overlap):
    import os
    loader = PyMuPDF4LLMLoader(file_path=path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。",".",",", "，", " ", ""]
    )

    splits = splitter.split_documents(docs)

    print(os.path.getsize(path))


    print(f"===== 测试 chunk_size={chunk_size}, overlap={chunk_overlap} =====")
    for i, split in enumerate(splits[:10]):
        print(f"\n【第{i+1}块】")
        print(split.page_content)
        print(len(split.page_content))
        print("-"*50)


if __name__ == "__main__":
    test_chunk_size("upload_file/key.pdf", 800, 120)