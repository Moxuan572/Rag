Lightweight-RAG-Local
纯本地轻量化 RAG 检索项目，基于 FAISS + 多路召回 + Reranker 重排序，
支持长文档 PDF 解析、智能文本分块、向量检索、语义精排，全程本地离线运行，无第三方接口依赖。
📌 项目简介
本项目实现工业级经典 RAG 全链路：
大体积 PDF 文档文本解析（支持 10w+ 字长文档）
自适应递归文本切割，合理控制块大小与上下文重叠
双路多路召回：向量相似度检索 + MMR 多样性召回
本地 Reranker 模型精准重排序，大幅提升检索准确率
全异步向量库构建与检索，性能更优
完整数据库缓存机制，避免重复建库、重复加载
适合场景：本地知识库、文档问答、长资料检索、私有化部署 AI 问答底座。
🛠️ 技术栈
文档解析：pymupdf4llm
文本分割：RecursiveCharacterTextSplitter
向量数据库：FAISS
嵌入模型：all-MiniLM-L6-v2 本地 Embedding
重排序模型：本地 BGE-Reranker
异步框架：asyncio
依赖生态：LangChain
📁 项目目录
plaintext
├── faiss_db/            # 自动生成 FAISS 向量库存放目录
├── upload_file/         # 自定义PDF文档存放文件夹
├── rag_model/           # 本地Embedding、Reranker模型目录
├── main.py              # 核心代码：建库、召回、重排、检索
└── README.md            # 项目说明文档
🚀 快速安装依赖
bash
运行
pip install langchain
pip install langchain-huggingface
pip install langchain-community
pip install sentence-transformers
pip install faiss-cpu
pip install pymupdf
🎯 核心功能说明
1. 智能文档分块
默认工业级最优参数（长文档适配）
python
运行
chunk_size = 800
chunk_overlap = 120
支持中英文双分隔符，语义切割更自然
合理重叠，解决上下文断裂问题
2. 多路召回策略
向量相似度检索：精准语义匹配
MMR 最大边际相关性检索：增加结果多样性、减少冗余
自动合并 + 内容去重，精简候选文档
3. 本地重排序 Rerank
召回粗筛选 → 重排精打分
对候选文档逐段相关性打分
按分数降序，输出 Top-N 最优结果
4. 向量库缓存机制
首次运行：异步构建向量库并本地持久化保存
二次运行：自动加载本地库，无需重复向量化
全局单例 DB 管理，减少内存占用与 IO 消耗
📖 使用教程
1. 环境准备
下载对应 Embedding / Reranker 模型，放入 rag_model 目录
将需要解析的 PDF 放入 upload_file 文件夹
修改代码内本地模型路径与PDF 文件路径
