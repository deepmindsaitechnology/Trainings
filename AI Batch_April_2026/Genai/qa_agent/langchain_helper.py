from langchain_community.vectorstores import FAISS
#from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile",
    temperature=0.1
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb_file_path = "faiss_index"


def create_vector_db():
    csv_file = "courses_faqs.csv"

    if not os.path.exists(csv_file):
        return f"Error: {csv_file} file not found."

    import pandas as pd
    from langchain_core.documents import Document

    try:
        df = pd.read_csv(csv_file, encoding="cp1252")
    except Exception as e:
        return f"CSV read error: {e}"

    df.columns = df.columns.str.strip()

    if "prompt" not in df.columns or "response" not in df.columns:
        return f"CSV must have prompt,response columns. Found: {df.columns.tolist()}"

    documents = []

    for _, row in df.iterrows():
        content = f"""
prompt: {row['prompt']}
response: {row['response']}
"""
        documents.append(Document(page_content=content))

    vectordb = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    vectordb.save_local(vectordb_file_path)

    return "Vector DB created successfully"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_qa_chain():
    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 3}
    )

    prompt_template = """
Given the following context and a question, generate an answer based on this context only.

Try to answer mainly from the "response" field in the CSV.

If the answer is not found in the context, try to give your own answer.

CONTEXT:
{context}

QUESTION:
{question}
"""

    prompt = PromptTemplate.from_template(prompt_template)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain