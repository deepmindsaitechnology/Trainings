import streamlit as st
import os
from langchain_helper import get_qa_chain, create_vector_db

st.title("Deepminds Courses Q&A 🌱")

if st.button("Create Knowledgebase"):
    message = create_vector_db()

    if message.startswith("Error"):
        st.error(message)
    else:
        st.success(message)

question = st.text_input("Question:")

if question:
    if not os.path.exists("faiss_index/index.faiss"):
        st.error("Please click 'Create Knowledgebase' first.")
    else:
        chain = get_qa_chain()
        response = chain.invoke(question)

        st.header("Answer")
        st.write(response)