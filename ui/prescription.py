import streamlit as st
from core.rag_chain import run_qa

def render_prescription(qa_chain, lang):
    col_l3, col_r3 = st.columns([1, 1.5], gap="large")

    with col_l3:
        st.markdown('<div class="section-label">Medication Check</div>', unsafe_allow_html=True)
        rx = st.text_input(
            "Medication",
            placeholder="e.g. Amoxicillin, Ceftriaxone, Azithromycin",
            label_visibility="collapsed",
            key="rx_input"
        )
        indication = st.text_input(
            "Indication (optional)",
            placeholder="e.g. Community-acquired pneumonia, Typhoid fever",
            key="rx_indication"
        )
        check_rx = st.button("🛡  Verify Medication", use_container_width=True)

        st.markdown("""
        <div class="med-card" style="margin-top:1rem;">
            <div class="med-card-title">AWaRe Classification</div>
            <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.7;">
                <span style="color:#10b981;font-weight:600;">ACCESS</span> — First-line, widely available<br>
                <span style="color:#f59e0b;font-weight:600;">WATCH</span> — Higher risk, monitor closely<br>
                <span style="color:#ef4444;font-weight:600;">RESERVE</span> — Last resort only
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r3:
        if check_rx:
            if not rx.strip():
                st.markdown('<div class="alert-warning">⚠ Please enter a medication name.</div>', unsafe_allow_html=True)
            else:
                query = f"Classify {rx} under the WHO AWaRe classification for antimicrobial stewardship."
                if indication.strip():
                    query += f" The intended indication is: {indication}. Is this appropriate per WHO guidelines?"

                with st.spinner(f"Verifying {rx} against WHO AWaRe database..."):
                    result = run_qa(qa_chain, query, lang)
                    answer = result["result"]
                    st.session_state.rx_result = result

                # Default values
                alert_class = "alert-warning"
                icon = "⚠️"

                if "INSUFFICIENT_DATA" in answer:
                    st.markdown(f"""
                    <div class="alert-warning">
                        <strong>⚠ Not Found in AWaRe Database</strong><br>
                        <strong>{rx}</strong> was not found in the current WHO AWaRe dataset. 
                        Consult a pharmacist or the latest WHO AWaRe list directly.
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    # Color-code the AWaRe category
                    answer_upper = answer.upper()
                    if "RESERVE" in answer_upper:
                        alert_class = "alert-emergency"
                        icon = "🔴"
                    elif "WATCH" in answer_upper:
                        alert_class = "alert-warning"
                        icon = "🟡"
                    else:
                        alert_class = "alert-success"
                        icon = "🟢"

                    st.markdown(
                        f'<div class="{alert_class}">{icon} <strong>AWaRe Verification Complete — {rx}</strong></div>',
                        unsafe_allow_html=True
                    )

                    # --- FIXED URDU FONT & BOLD LOGIC ---
                    if lang == "Urdu":
                        formatted_ans = answer.replace("**", "<b>").replace("</b> ", "</b>&nbsp;")
                        st.markdown(
                            f'<div style="font-size: 18px; line-height: 1.6; text-align: right; direction: rtl;">{formatted_ans}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(answer)

                    with st.expander("📚 WHO Evidence Sources"):
                        for i, doc in enumerate(result["source_documents"], 1):
                            src = doc.metadata.get("source", "Unknown")
                            st.markdown(f'<div class="source-item">📄 Source {i}: {src}</div>', unsafe_allow_html=True)

        elif st.session_state.rx_result:
            st.markdown('<div class="alert-info">📋 <strong>Previous verification result shown below</strong></div>', unsafe_allow_html=True)

            # --- FIXED PREVIOUS RESULT FONT LOGIC ---
            prev_ans = st.session_state.rx_result["result"]
            if lang == "Urdu":
                formatted_prev = prev_ans.replace("**", "<b>").replace("</b> ", "</b>&nbsp;")
                st.markdown(
                    f'<div style="font-size: 18px; line-height: 1.6; text-align: right; direction: rtl;">{formatted_prev}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(prev_ans)

        else:
            st.markdown("""
            <div class="med-card" style="text-align:center;padding:3rem 2rem;opacity:0.6;">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;">💊</div>
                <div style="font-size:0.88rem;color:var(--text-muted);">Enter a medication to verify its WHO AWaRe classification</div>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.4rem;">Supports antimicrobial stewardship decisions</div>
            </div>
            """, unsafe_allow_html=True)