# backend/main.py
import os
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

# LangChain imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 1. FastAPI Setup
app = FastAPI()

# 2. Hardcode OPENAI_API_KEY (This is for demonstration purposes only. Use environment variables or secure vaults in production.)
openai_api_key = "sk-...."

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

# 3. Document Loading
# For text files:
# loader = DirectoryLoader('path/to/texts', glob='*.txt', loader_cls=TextLoader)
# For PDFs:
loader = DirectoryLoader('data', glob='*.pdf', loader_cls=PyPDFLoader)
docs = loader.load()

# 4. Text Splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
documents = splitter.split_documents(docs)

# 5. Vector Store (FAISS)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 6. LLM & Prompt Template
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=0,
    model_name="gpt-4o-mini"
)

template = """You are a helpful assistant. Use the provided context to answer the question.
If you cannot find the answer in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# 7. Create RetrievalQA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # or "map_reduce", "refine"
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

# 8. Data Models
class Message(BaseModel):
    text: str

# 9. REST Endpoint
@app.post("/api/chat")
async def chat_endpoint(msg: Message):
    """
    Receives user query as JSON, returns the LLM's response.
    """
    user_query = msg.text
    answer = qa_chain.run(user_query)
    return {"assistant": answer}

# 10. Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
