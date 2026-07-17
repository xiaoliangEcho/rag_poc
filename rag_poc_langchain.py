from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
import os
from langchain_openai import ChatOpenAI
import pdb
import re
import readline

debug=True

# 1. 加载文档
print("step1 loading documents")
documents = []
docs_dir = "/home/zoe/AI/rag_poc/docs"
for file in os.listdir(docs_dir):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(docs_dir, file))
        documents.extend(loader.load())
    elif file.endswith(".txt"):
        loader = TextLoader(os.path.join(docs_dir, file))
        documents.extend(loader.load())

# 2. 分割文本
print("step2 split documents")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, 
                                               chunk_overlap=100, 
                                               separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
                                               length_function=len,)
chunks = text_splitter.split_documents(documents)

# 3. 创建向量存储
print("step3 making vectors from documents")
embeddings = HuggingFaceEmbeddings(model_name="/home/zoe/AI/rag_poc/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_type="mmr",
                                     search_kwargs={"k": 3,          # 最终返回3个
                                                    "fetch_k": 15,   # 候选池15个
                                                    "lambda_mult": 0.5  # 偏向多样性（因为你的文档有不同主题）
                                                    })

# 4. 初始化模型
print("step4 configure local llama using qwen2.5-3b")
llm = ChatOpenAI(
    model="qwen2.5-3b",
    base_url="http://localhost:8001/v1",
    api_key="sk-no-key-required",
    temperature=0,
    max_tokens=1024
)

# 5. 构建 RAG 链
print("step5 building RAG chain")
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个基于知识库回答问题的助手。请根据以下提供的上下文信息回答问题。如果无法从上下文中找到答案，请直接告知用户。"),
    ("user", "上下文：\n{context}\n\n问题：{question}")
])

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# # 6. 构建闲聊链（用于非 RAG 路径）
# chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个友好、简洁的AI助手。请用中文简短地回答用户的问题。"),
#     ("user", "{input}")
# ])
# chat_chain = chat_prompt | llm | StrOutputParser()

# 7. 持续问答循环
RAG_KEYWORDS = ["公司", "成立", "总部", "业务", "产品", "创易科技"]

print("🤖 RAG 知识库问答系统已启动（输入 'exit' 或 'quit' 退出）")
print("-" * 50)

def rag_debug(question="你好"):
    # 假设你的 retriever 已经实例化好了
    test_question = question
    docs = retriever.invoke(test_question)

    print(f"针对问题：'{test_question}'，共检索到 {len(docs)} 个片段：\n")
    for i, doc in enumerate(docs, 1):
        print(f"--- 片段 {i} ---")
        print(f"来源文件: {doc.metadata.get('source', '未知')}")
        print(f"页码: {doc.metadata.get('page', '未知')}")
        print(f"具体内容:\n{doc.page_content}\n")

def llm_debug(question='hello'):
    result = llm.invoke(question)
    print(f'result: {result.content}')
    print(f'meta data: {result.response_metadata}')

while True:
    question = input("\n❓ 请输入您的问题: ").strip()
    question = re.sub(r'[\x00-\x1F\x7F]', '', question).strip()
    print(f"question is {question}")
    
    # 退出判断
    if question.lower() in ['exit', 'quit', '退出']:
        print("👋 再见！")
        break
    if not question:
        print("⚠️ 问题不能为空，请重新输入。")
        continue
    
    # 核心问答逻辑
    try:
        print("⏳ 正在思考...")
        if any(keyword in question for keyword in RAG_KEYWORDS):
            print("⏳ 查询RAG...")
            if debug:
                print("rag debugging")
                rag_debug(question)

            print("\n💡 准备回答中...: ", end="", flush=True)

            # 使用 stream 方法，并传入相同的 config
            for chunk in rag_chain.stream(question, config={"configurable": {"session_id": "none"}}):
                # chunk 就是模型每次吐出的一小段文本
                print(chunk, end="", flush=True)

            print() # 输出结束后换行
        else:
            print("不查询RAG...")
            # if debug:
            #     print("llm debuging")
            #     llm_debug(question)
            print("\n💡 准备回答中...: ", end="", flush=True)
            # 使用 stream 方法获取一个生成器，逐块接收内容
            for chunk in llm.stream(question):
                # chunk.content 是当前生成的文本片段
                print(chunk.content, end="", flush=True)
            print() # 最后打印一个换行，保持格式整洁
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    
    print("-" * 50)
