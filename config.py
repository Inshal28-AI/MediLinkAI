import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    # 1. local env
    api_key = os.getenv("MediLinkAI_API_KEY")

    # 2. streamlit secrets fallback
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("MediLinkAI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError("❌ API_KEY is missing )")

    return api_key


API_KEY = get_api_key()

MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_PATH = "data/med_pathogen_brain"
