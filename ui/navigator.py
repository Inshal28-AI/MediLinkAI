import streamlit as st
from core.utils import check_red_flags
from core.rag_chain import run_qa

def render_navigator(qa_chain, lang):
    col_l2, col_r2 = st.columns([1, 1.5], gap="large")
 
    with col_l2:
        st.markdown('<div class="section-label">Symptom Entry</div>', unsafe_allow_html=True)
        sx = st.text_area(
            "Symptoms",
            height=140,
            placeholder="e.g. High fever (39-40°C), severe headache, retro-orbital pain, myalgia, maculopapular rash, positive tourniquet test...",
            label_visibility="collapsed",
            key="sx_input"
        )
 
        st.markdown('<div class="section-label" style="margin-top:1rem;">Clinical Context (optional)</div>', unsafe_allow_html=True)
        context_extras = st.text_input(
            "Context",
            placeholder="e.g. Travel history, exposure, vaccination status, endemic area",
            label_visibility="collapsed",
            key="sx_context"
        )
 
        run_diag = st.button("🔍  Run Differential Diagnosis", use_container_width=True)
 
    with col_r2:
        if run_diag:
            if not sx.strip():
                # Indented 4 spaces inside 'if not sx.strip()'
                st.markdown('<div class="alert-warning">⚠ Please enter patient symptoms to proceed.</div>', unsafe_allow_html=True)
            else:
                # Indented 4 spaces inside 'else'
                # Emergency check first
                flags = check_red_flags(sx + " " + context_extras)
                if flags:
                    flaglist = ", ".join([f"<strong>{f}</strong>" for f in flags])
                    st.markdown(f'<div class="alert-emergency">🚨 <strong>EMERGENCY RED FLAGS DETECTED</strong><br>{flaglist}<br><br>Initiate immediate stabilization. Apply ABC protocol. Escalate to senior clinician.</div>', unsafe_allow_html=True)

                full_sx = sx
                if context_extras.strip():
                    full_sx += f". Additional context: {context_extras}"

                with st.spinner("Consulting WHO evidence base..."):
                    result = run_qa(
                        qa_chain,
                        f"Provide a structured differential diagnosis and WHO-recommended management for a patient presenting with: {full_sx}",
                        lang
                    )
                    answer = result["result"]
                    st.session_state.diag_result = result

                if "INSUFFICIENT_DATA" in answer:
                    st.markdown("""
                    <div class="alert-warning">
                        <strong>⚠ Insufficient WHO Guideline Data</strong><br>
                        The provided symptom pattern does not match specific pathogens in the current WHO dataset. 
                        Consider clinical consultation and broader investigation.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-success"><strong>✓ Evidence-Based Analysis Complete</strong></div>', unsafe_allow_html=True)
                    
                    # --- FIXED URDU FONT & BOLD LOGIC ---
                    if lang == "Urdu":
                        formatted_ans = answer.replace("**", "<b>").replace("</b> ", "</b>&nbsp;")
                        st.markdown(f'<div style="font-size: 18px; line-height: 1.6; text-align: right; direction: rtl;">{formatted_ans}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(answer)
                        
                    with st.expander("📚 WHO Evidence Sources"):
                        for i, doc in enumerate(result["source_documents"], 1):
                            src = doc.metadata.get("source", "Unknown")
                            st.markdown(f'<div class="source-item">📄 Source {i}: {src}</div>', unsafe_allow_html=True)

        elif st.session_state.diag_result:
            # Aligned with 'if run_diag'
            st.markdown('<div class="alert-info">📋 <strong>Previous diagnostic result shown below</strong></div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.diag_result["result"]
            if lang == "Urdu":
                formatted_prev = prev_ans.replace("**", "<b>").replace("</b> ", "</b>&nbsp;")
                st.markdown(f'<div style="font-size: 18px; line-height: 1.6; text-align: right; direction: rtl;">{formatted_prev}</div>', unsafe_allow_html=True)
            else:
                st.markdown(prev_ans)
                
        else:
            # Aligned with 'if run_diag'
            st.markdown("""
            <div class="med-card" style="text-align:center;padding:3rem 2rem;opacity:0.6;">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;">🦠</div>
                <div style="font-size:0.88rem;color:var(--text-muted);">Enter symptoms and run differential diagnosis</div>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.4rem;">Grounded in WHO 2024-2026 infectious disease guidelines</div>
            </div>
            """, unsafe_allow_html=True)