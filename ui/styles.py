import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-primary:    #0a0f1e;
        --bg-secondary:  #0d1530;
        --bg-card:       #111827;
        --bg-card-hover: #162040;
        --accent-blue:   #3b82f6;
        --accent-cyan:   #06b6d4;
        --accent-green:  #10b981;
        --accent-red:    #ef4444;
        --accent-amber:  #f59e0b;
        --text-primary:  #f0f4ff;
        --text-muted:    #8892a4;
        --border:        rgba(59,130,246,0.15);
        --border-bright: rgba(59,130,246,0.4);
        --glow:          0 0 20px rgba(59,130,246,0.2);
        --glow-strong:   0 0 40px rgba(59,130,246,0.35);
    }
    
    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1400px !important; }
    
    .stApp::before {
        content: '';
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none; z-index: 0;
    }
    
    .medilink-header {
        background: linear-gradient(135deg, #0d1530 0%, #0a1628 50%, #0d1a35 100%);
        border: 1px solid var(--border-bright);
        border-radius: 16px;
        padding: 1.8rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--glow-strong), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .medilink-header::before {
        content: '';
        position: absolute; top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .medilink-header::after {
        content: '';
        position: absolute; bottom: -30%; left: 5%;
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .header-title {
        font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px;
        background: linear-gradient(90deg, #60a5fa, #06b6d4, #a78bfa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin: 0 0 0.3rem 0;
    }
    .header-subtitle {
        font-size: 0.95rem; color: var(--text-muted); font-weight: 400;
        letter-spacing: 0.3px; margin: 0;
    }
    .header-badge {
        display: inline-block;
        background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.35);
        color: #10b981; border-radius: 20px;
        padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600;
        letter-spacing: 0.5px; margin-top: 0.6rem;
    }
    .header-badge::before { content: '● '; font-size: 0.6rem; }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important; padding: 4px !important;
        border: 1px solid var(--border) !important; gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important; padding: 0.55rem 1.4rem !important;
        font-size: 0.88rem !important; font-weight: 500 !important;
        color: var(--text-muted) !important; background: transparent !important;
        border: none !important; transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a6e, #1a3560) !important;
        color: #93c5fd !important; border: 1px solid var(--border-bright) !important;
        box-shadow: 0 0 12px rgba(59,130,246,0.25) !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }
    
    .med-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px; padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .med-card:hover {
        border-color: var(--border-bright);
        box-shadow: var(--glow);
    }
    .med-card-title {
        font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px;
        color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 0.8rem;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
        outline: none !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        color: #fff !important; border: 1px solid rgba(96,165,250,0.3) !important;
        border-radius: 10px !important; padding: 0.55rem 1.5rem !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.88rem !important; font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s ease !important; cursor: pointer !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        box-shadow: 0 0 20px rgba(59,130,246,0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem !important; }
    
    .sidebar-logo {
        font-size: 1.3rem; font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #06b6d4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin-bottom: 0.3rem;
    }
    .sidebar-section {
        background: rgba(59,130,246,0.06);
        border: 1px solid var(--border); border-radius: 10px;
        padding: 0.9rem 1rem; margin: 0.7rem 0;
    }
    .sidebar-section-title {
        font-size: 0.68rem; font-weight: 600; letter-spacing: 1.2px;
        color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;
    }
    .status-dot-green { color: #10b981; }
    .status-dot-red   { color: #ef4444; }
    
    .metric-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1rem; }
    .metric-chip {
        background: rgba(59,130,246,0.1); border: 1px solid var(--border);
        border-radius: 8px; padding: 0.5rem 0.9rem;
        font-size: 0.78rem; color: var(--text-muted);
    }
    .metric-chip span { display: block; font-size: 1.1rem; font-weight: 600; color: var(--text-primary); }
    
    .alert-emergency {
        background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.4);
        border-left: 4px solid #ef4444; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem;
        animation: pulse-red 2s infinite;
    }
    @keyframes pulse-red {
        0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
        50%      { box-shadow: 0 0 15px 3px rgba(239,68,68,0.2); }
    }
    .alert-warning {
        background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3);
        border-left: 4px solid #f59e0b; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem;
    }
    .alert-success {
        background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);
        border-left: 4px solid #10b981; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem;
    }
    .alert-info {
        background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3);
        border-left: 4px solid #3b82f6; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem;
    }
    
    .soap-output {
        background: var(--bg-secondary); border: 1px solid var(--border);
        border-radius: 12px; padding: 1.4rem 1.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem; line-height: 1.8;
        white-space: pre-wrap; color: #cbd5e1;
    }
    
    .patient-card {
        background: var(--bg-card);
        border: 1px solid var(--border); border-radius: 10px;
        padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;
        display: flex; justify-content: space-between; align-items: center;
        cursor: pointer; transition: all 0.15s;
    }
    .patient-card:hover { border-color: var(--border-bright); background: var(--bg-card-hover); }
    
    .source-item {
        background: rgba(59,130,246,0.07); border: 1px solid var(--border);
        border-radius: 8px; padding: 0.6rem 0.9rem; margin-bottom: 0.4rem;
        font-size: 0.78rem; color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stSpinner > div { border-top-color: var(--accent-blue) !important; }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
    
    .voice-recorder-wrap {
        background: var(--bg-secondary);
        border: 1px solid var(--border); border-radius: 12px;
        padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    }
    .recorder-btn {
        display: inline-flex; align-items: center; gap: 0.5rem;
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        color: #fff; border: 1px solid rgba(96,165,250,0.3);
        border-radius: 9px; padding: 0.5rem 1.1rem;
        font-size: 0.85rem; font-weight: 600; cursor: pointer;
        font-family: 'Sora', sans-serif; transition: all 0.2s;
    }
    .recorder-btn:hover { background: linear-gradient(135deg, #2563eb, #1d4ed8); box-shadow: 0 0 16px rgba(59,130,246,0.35); }
    .recorder-btn.recording {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        border-color: rgba(239,68,68,0.5) !important;
        animation: pulse-rec 1.2s infinite;
    }
    @keyframes pulse-rec {
        0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
        50%      { box-shadow: 0 0 14px 4px rgba(239,68,68,0.3); }
    }
    .transcript-box {
        margin-top: 0.7rem; background: rgba(59,130,246,0.07);
        border: 1px dashed var(--border-bright); border-radius: 8px;
        padding: 0.7rem 1rem; font-size: 0.83rem; color: #cbd5e1;
        min-height: 2.2rem; font-style: italic;
    }
    .rec-status { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.45rem; }
    
    .disclaimer-box {
        background: var(--bg-card);
        border: 1px solid rgba(245,158,11,0.4);
        border-radius: 16px; padding: 2.5rem;
        max-width: 680px; margin: 4rem auto;
        box-shadow: 0 0 60px rgba(245,158,11,0.1);
    }
    .disclaimer-icon { font-size: 3rem; margin-bottom: 0.8rem; }
    .disclaimer-title {
        font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .disclaimer-text { color: #94a3b8; font-size: 0.9rem; line-height: 1.7; margin-bottom: 1.5rem; }
    .med-divider { border: none; border-top: 1px solid var(--border); margin: 1.2rem 0; }
    .section-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 1.5px; color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)