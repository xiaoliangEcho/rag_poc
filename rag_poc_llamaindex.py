import os
import re
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings,
    PromptTemplate
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import ChatMessage
import readline
import asyncio

from llama_index.core import Document
from langchain_community.document_loaders import PyPDFLoader
from llama_index.core.readers.base import BaseReader

debug = True

# 1. 加载文档 & 2. 分割文本
# LlamaIndex 的 SimpleDirectoryReader 会自动识别并加载目录下的 PDF 和 TXT 文件
print("step1 & step2: loading and splitting documents")
docs_dir = "/home/zoe/AI/rag_poc/docs"

# 1. 定义一个继承自 BaseReader 的自定义类
class LangChainPDFReader(BaseReader):
    def load_data(self, file, extra_info=None):
        # 1. 获取纯文件名（比如 "rag_poc.pdf"）
        file_name = file.name if hasattr(file, 'name') else str(file)
        
        # 2. 使用 LangChain 加载内容
        loader = PyPDFLoader(str(file))
        langchain_docs = loader.load()
        
        # 3. 转换时，手动把文件名注入到 metadata 中
        return [
            Document(
                text=doc.page_content, 
                metadata={
                    "file_name": file_name,  # 👈 关键：注入文件名
                    "page_label": doc.metadata.get("page", "未知") # 顺便把页码也规范一下
                }
            ) for doc in langchain_docs
        ]

# 2. 实例化这个自定义 Reader
custom_pdf_reader = LangChainPDFReader()

# 3. 在 file_extractor 中传入实例化后的对象（注意是对象，不是函数）
documents = SimpleDirectoryReader(
    docs_dir,
    required_exts=[".pdf", ".txt"],
    file_extractor={
        ".pdf": custom_pdf_reader 
    }
).load_data()

# 配置文本切块策略（对应你原来的 RecursiveCharacterTextSplitter）
text_splitter = SentenceSplitter(chunk_size=500, chunk_overlap=100)

# 3. 创建向量存储
print("step3: making vectors from documents")
# 配置本地 Embedding 模型
Settings.embed_model = HuggingFaceEmbedding(model_name="/home/zoe/AI/rag_poc/all-MiniLM-L6-v2")

# 构建索引，并传入自定义的切块器
index = VectorStoreIndex.from_documents(
    documents, 
    transformations=[text_splitter]
)

# 配置 MMR 检索器（完美复刻你原来的 search_type="mmr" 策略）
retriever = index.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=5,          # 最终返回 3 个
    # fetch_k 和 lambda_mult 等高级参数可以在 query 时通过 kwargs 传入
)

# 4. 初始化模型
print("step4: configure local llama using qwen2.5-3b")
llm = OpenAILike(
    model="qwen2.5-3b",
    api_base="http://localhost:8001/v1",
    api_key="sk-no-key-required",
    is_chat_model=True,  # 告诉 LlamaIndex 这是一个支持对话模式的模型
    temperature=0,
    max_tokens=1024,
    context_window=32768 # 手动指定上下文窗口，防止报错
)
# 将 LLM 设置为全局默认
Settings.llm = llm

# 5. 构建 RAG 链 (QueryEngine)
print("step5: building RAG chain")
# 定义自定义提示词（LlamaIndex 使用 {context_str} 和 {query_str} 作为占位符）
qa_prompt_tmpl = (
    "你是一个基于知识库回答问题的助手。请根据以下提供的上下文信息回答问题。如果无法从上下文中找到答案，请直接告知用户。\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "问题：{query_str}\n"
    "回答："
)
qa_prompt = PromptTemplate(qa_prompt_tmpl)

# 创建查询引擎（相当于原来的 rag_chain）
query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    streaming=True # 开启流式输出
)

# 6. 闲聊链（用于非 RAG 路径）
# 直接复用上面配置的 llm，不需要额外构建 chain
chat_llm = Settings.llm

# 7. 持续问答循环
RAG_KEYWORDS = ["公司", "成立", "总部", "业务", "产品", "创易科技"]

print("🤖 RAG 知识库问答系统已启动（输入 'exit' 或 'quit' 退出）")
print("-" * 50)

def rag_debug(question="你好"):
    # 使用 retriever 进行检索测试
    nodes = retriever.retrieve(question)
    print(f"针对问题：'{question}'，共检索到 {len(nodes)} 个片段：\n")
    for i, node in enumerate(nodes, 1):
        print(f"--- 片段 {i} ---")
        # LlamaIndex 的 Node 对象通过 node.metadata 获取元数据
        print(f"来源文件: {node.metadata.get('file_name', '未知')}")
        print(f"页码: {node.metadata.get('page_label', '未知')}")
        print(f"具体内容:\n{node.text}\n")


async def main():
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
                
                # 1. 手动执行检索（这一步很快，不需要流式）
                nodes = retriever.retrieve(question)
                
                # 2. 将检索到的文档内容拼接成上下文字符串
                context_str = "\n\n".join([node.text for node in nodes])
                
                # 3. 手动拼接提示词（复刻你原来定义的 qa_prompt 逻辑）
                final_prompt = (
                "你是一个基于知识库回答问题的助手。请严格根据以下提供的上下文信息回答问题。\n"
                "【重要约束】：\n"
                "1. 你的回答必须详细、完整，尽可能多地提取上下文中的关键信息。\n"
                "2. 你的回答必须与用户的问题高度相关，不要输出上下文中与问题无关的背景信息。\n"
                "3. 如果上下文中没有直接回答问题的信息，请直接告知用户，不要推测或补充其他内容。\n"
                "---------------------\n"
                f"上下文信息：\n{context_str}\n"
                "---------------------\n"
                f"用户问题：{question}\n"
                "精准回答："
            )
                
                # 4. 使用你之前已经调通的 stream_chat 方法进行流式生成
                messages = [ChatMessage(role="user", content=final_prompt)]
                
                response = chat_llm.stream_chat(messages)
                for chunk in response:
                    print(chunk.delta, end="", flush=True)
                print() 
                
            else:
                print("不查询RAG...")
                print("\n💡 准备回答中...: ", end="", flush=True)
                
                # 闲聊模式：将字符串包装成消息列表格式
                messages = [ChatMessage(role="user", content=question)]
                
                response = chat_llm.stream_chat(messages)
                for chunk in response:
                    print(chunk.delta, end="", flush=True)
                print() # 最后打印一个换行
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        print("-" * 50)

# 在文件最末尾启动异步循环
if __name__ == "__main__":
    asyncio.run(main())