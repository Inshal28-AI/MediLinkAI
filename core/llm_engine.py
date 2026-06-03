import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from core.prompts import PROMPT

@st.cache_resource(show_spinner="Initializing clinical knowledge base...")
def load_engine(db_path):
    if not os.path.exists(db_path):
        return None
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Knowledge base load error: {e}")
        return None
    

    

def initialize_qa_chain(vector_db, api_key):
    try:
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=1024,
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True,
        )
        return qa_chain, llm
    except Exception as e:
        st.error(f"LLM initialization failed: {e}")
        return None, None
    
def load_vector_db(db_path):
    return load_engine(db_path)


def load_llm(api_key):
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=1024,
)   
