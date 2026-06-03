import streamlit as st
from config import API_KEY, DB_PATH
from ui.styles import inject_custom_css
from core.llm_engine import load_engine, initialize_qa_chain
from ui.sidebar import render_sidebar
from ui.smart_scribe import render_smart_scribe
from ui.navigator import render_navigator
from ui.prescription import render_prescription

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediLink AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Global CSS Styles
inject_custom_css()

# ── Session State Init ─────────────────────────────────────────────────────────
for key, default in {
    "agreed": False,
    "patient_records": {},
    "active_patient": None,
    "diag_result": None,
    "rx_result": None,
    "patient_counter": 1,
    "voice_transcript": "",
    "rx_photo": None,
    "show_rx_photo": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Disclaimer Gate ───────────────────────────────────────────────────────────
if not st.session_state.agreed:
    st.markdown("""
    <div class="disclaimer-box">
        <div class="disclaimer-icon">🩺</div>
        <div class="disclaimer-title">Clinical Decision Support Notice</div>
        <div class="disclaimer-text">
            <strong style="color:#f0f4ff">MediLink AI</strong> is a clinical support prototype grounded in official WHO protocols (2024–2026).<br><br>
            This tool is designed to <strong style="color:#f0f4ff">assist healthcare professionals</strong>, not replace clinical judgment or provide direct patient diagnosis.<br><br>
            Final clinical decisions, prescriptions, and treatment plans remain the sole responsibility of the licensed healthcare provider.<br><br>
            By proceeding, you confirm you are a qualified medical professional using this tool in a supervised clinical context.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        if st.button("✓  I Agree — Enter Clinical Suite", use_container_width=True):
            st.session_state.agreed = True
            st.rerun()
    st.stop()

# ── Engine Checks & Setup ─────────────────────────────────────────────────────
if not API_KEY:
    st.markdown("""
    <div class="alert-emergency">
        <strong>🔑 API Key Missing</strong><br>
        Add <code>MediLinkAI_API_KEY</code> in your Hugging Face Space → Settings → Repository secrets.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

vector_db = load_engine(DB_PATH)
if vector_db is None:
    st.markdown("""
    <div class="alert-emergency">
        <strong>🧠 Knowledge Base Not Found</strong><br>
        Upload the <code>med_pathogen_brain</code> FAISS folder to your <code>data/</code> directory.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

qa_chain, llm = initialize_qa_chain(vector_db, API_KEY)
if qa_chain is None:
    st.stop()

# ── App Layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="medilink-header">
    <div style="display:flex; align-items:center; gap:1rem;">
        <div style="font-size:2.5rem;">🩺</div>
        <div>
            <div class="header-title">MediLink AI</div>
            <div class="header-subtitle">WHO-Grounded Infectious Disease Clinical Co-Pilot</div>
            <div class="header-badge">Clinical Engine Active</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Render Global Sidebar Setup
lang = render_sidebar()

# Main Application Tabs Setup
tab1, tab2, tab3 = st.tabs([
    "📝  Smart Scribe",
    "🦠  Pathogen Navigator",
    "💊  Prescription Guard",
])

with tab1:
    render_smart_scribe(llm, lang)

with tab2:
    render_navigator(qa_chain, lang)

with tab3:
    render_prescription(qa_chain, lang)