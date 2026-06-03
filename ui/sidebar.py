import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🩺 MediLink AI</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">⚙ Preferences</div>', unsafe_allow_html=True)
        lang = st.selectbox("Response Language / زبان", ["English", "Urdu"], label_visibility="collapsed")

        st.markdown('<hr class="med-divider">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">👤 Active Patient</div>', unsafe_allow_html=True)
        if st.session_state.active_patient and st.session_state.active_patient in st.session_state.patient_records:
            p = st.session_state.patient_records[st.session_state.active_patient]
            st.markdown(f"""
            <div class="sidebar-section">
                <div style="font-weight:600;color:#f0f4ff;">{p['name']}</div>
                <div style="font-size:0.78rem;color:#8892a4;margin-top:0.3rem;">
                    {p['age']}y · {p['gender']}<br>
                    CC: {p.get('chief_complaint','—')[:35]}{'...' if len(p.get('chief_complaint','')) > 35 else ''}
                </div>
                <div style="font-size:0.72rem;color:#3b82f6;margin-top:0.4rem;">
                    {len(p['soap_notes'])} SOAP note(s)
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Clear Active Patient", use_container_width=True):
                st.session_state.active_patient = None
                st.rerun()
        else:
            st.markdown('<div style="color:#8892a4;font-size:0.82rem;">No patient selected. Register in Smart Scribe tab.</div>', unsafe_allow_html=True)

        st.markdown('<hr class="med-divider">', unsafe_allow_html=True)

        total_patients = len(st.session_state.patient_records)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-chip">Patients<span>{total_patients}</span></div>
            <div class="metric-chip">Session<span>Live</span></div>
        </div>
        """, unsafe_allow_html=True)

        if total_patients > 0:
            if st.button("🗑 Clear All Records", use_container_width=True):
                st.session_state.patient_records = {}
                st.session_state.active_patient = None
                st.session_state.patient_counter = 1
                st.rerun()
                
    return lang