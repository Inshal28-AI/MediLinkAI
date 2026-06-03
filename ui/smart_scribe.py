import streamlit as st
from components.voice_recorder import voice_recorder_component
from components.image import image_to_b64
from core.utils import check_red_flags, save_patient_record, add_soap_note

def render_smart_scribe(llm, lang):
    col_left, col_right = st.columns([1, 1.4], gap="large")

    # ── Left: Patient Registration + Hardware + Inputs ──
    with col_left:
        st.markdown('<div class="section-label">Patient Registration</div>', unsafe_allow_html=True)
        p_name = st.text_input("Patient Name", placeholder="e.g. Ahmed Khan", key="p_name")
        c1, c2 = st.columns(2)
        with c1:
            p_age = st.number_input("Age", min_value=0, max_value=120, value=30, key="p_age")
        with c2:
            p_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="p_gender")
        p_cc = st.text_input("Chief Complaint", placeholder="e.g. Fever for 3 days", key="p_cc")

        # Voice Recorder
        voice_recorder_component(key="voice_main")

        # Camera + File Uploader
        st.markdown('<div class="section-label" style="margin-top:0rem;">📷 Prescription Photo</div>', unsafe_allow_html=True)
        cam_col1, cam_col2 = st.columns([1, 1])
        with cam_col1:
            use_camera = st.toggle("Open Camera", key="cam_toggle")
        with cam_col2:
            upload_rx = st.file_uploader("Or upload image", type=["jpg", "jpeg", "png"], key="rx_upload", label_visibility="collapsed")

        if use_camera:
            cam_image = st.camera_input("Point camera at prescription and capture", key="cam_capture", label_visibility="collapsed")
            if cam_image:
                st.session_state.rx_photo = image_to_b64(cam_image)
                st.session_state.show_rx_photo = True
                st.success("📷 Prescription photo captured!")

        if upload_rx and not st.session_state.rx_photo:
            st.session_state.rx_photo = image_to_b64(upload_rx)
            st.session_state.show_rx_photo = True
            st.success("🖼 Prescription image uploaded!")

        if st.session_state.rx_photo:
            col_clr, col_tog = st.columns(2)
            with col_clr:
                if st.button("🗑 Remove Photo", use_container_width=True, key="rm_photo"):
                    st.session_state.rx_photo = None
                    st.session_state.show_rx_photo = False
                    st.rerun()
            with col_tog:
                lbl = "🔲 Hide in SOAP" if st.session_state.show_rx_photo else "🔳 Show in SOAP"
                if st.button(lbl, use_container_width=True, key="tog_photo"):
                    st.session_state.show_rx_photo = not st.session_state.show_rx_photo

        # Clinical Notes Text Area
        st.markdown('<div class="section-label" style="margin-top:1rem;">Clinical Notes / History</div>', unsafe_allow_html=True)
        raw_input = st.text_area(
            "Enter raw observations, notes, or dictation",
            height=160,
            placeholder="Pt presents with 3d hx of high fever (39.5°C), chills, severe headache, retroorbital pain. No cough. Lives in dengue-endemic area. No prior similar illness...",
            label_visibility="collapsed",
            key="raw_notes",
        )

        if st.button("⚡  Generate SOAP Note", use_container_width=True):
            if not raw_input.strip():
                st.markdown('<div class="alert-warning">⚠ Please enter clinical observations before generating a SOAP note.</div>', unsafe_allow_html=True)
            elif not p_name.strip():
                st.markdown('<div class="alert-warning">⚠ Please enter a patient name to register the record.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Generating structured SOAP note..."):
                    rx_note = ""
                    if st.session_state.rx_photo:
                        rx_note = "\nNote: A doctor's prescription photo has been attached to this record."

                    soap_prompt = f"""Generate a complete, professional medical SOAP note in {lang}. Patient: {p_name}, {p_age}y, {p_gender}. Chief Complaint: {p_cc}. Clinical notes: {raw_input}{rx_note} 
                    Format with exact headers: SUBJECTIVE | OBJECTIVE | ASSESSMENT | PLAN
                    Under ASSESSMENT include: Probable Diagnosis, Differential Diagnoses, Severity.
                    Under PLAN include: Investigations, Treatment, Monitoring, Follow-up."""

                    res = llm.invoke(soap_prompt)
                    soap_text = res.content

                    pid = f"PT{st.session_state.patient_counter:04d}"
                    save_patient_record(pid, p_name, p_age, p_gender, p_cc)
                    add_soap_note(pid, soap_text, raw_input)
                    st.session_state.active_patient = pid
                    st.session_state.patient_counter += 1
                    st.session_state["last_soap"] = soap_text
                    st.session_state["last_soap_patient"] = p_name

        if raw_input.strip():
            flags = check_red_flags(raw_input)
            if flags:
                flaglist = ", ".join(flags)
                st.markdown(f'<div class="alert-emergency">🚨 <strong>Red Flag Detected:</strong> {flaglist}<br><small>Ensure immediate assessment and stabilization protocol.</small></div>', unsafe_allow_html=True)

    # ── Right: SOAP Processing & History Display ──
    with col_right:
        if st.session_state.get("last_soap"):
            has_photo = bool(st.session_state.rx_photo)
            hdr_left, hdr_right = st.columns([3, 1])
            
            with hdr_left:
                st.markdown(f'<div class="section-label">SOAP Note — {st.session_state.get("last_soap_patient","Patient")}</div>', unsafe_allow_html=True)
            
            with hdr_right:
                if has_photo:
                    btn_label = "📷 Hide Rx" if st.session_state.show_rx_photo else "📷 View Rx"
                    if st.button(btn_label, key="soap_rx_toggle", use_container_width=True):
                        st.session_state.show_rx_photo = not st.session_state.show_rx_photo

            raw_soap = st.session_state["last_soap"]
            formatted_soap = raw_soap.replace("**", "<b>").replace("</b> ", "</b>&nbsp;")
            
            for header in ["SUBJECTIVE", "OBJECTIVE", "ASSESSMENT", "PLAN"]:
                formatted_soap = formatted_soap.replace(header, f"<br><b>{header}</b>")

            if lang == "Urdu":
                st.markdown(f'''
                    <div class="soap-output" style="font-size: 20px; line-height: 1.3; text-align: right; direction: rtl; padding: 10px;">
                        {formatted_soap}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="soap-output" style="font-size: 14px; line-height: 1.4; text-align: left; padding: 10px;">
                        {formatted_soap}
                    </div>
                ''', unsafe_allow_html=True)

            if has_photo and st.session_state.show_rx_photo:
                st.markdown("""
                <div style="margin-top:10px; border:1px solid #ddd; border-radius:4px;">
                    <div style="background:#f0f2f6; padding:5px; font-size:0.75rem; font-weight:bold; text-align:center;">
                        📄 ATTACHED PRESCRIPTION PHOTO
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.image(st.session_state.rx_photo, use_container_width=True)

            st.divider()

            st.download_button(
                "⬇ Download SOAP Note",
                data=st.session_state["last_soap"],
                file_name=f"SOAP_{st.session_state.get('last_soap_patient','patient').replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.markdown("""
            <div class="med-card" style="text-align:center;padding:3rem 2rem;opacity:0.6;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">📋</div>
                <div style="font-size:0.88rem;color:var(--text-muted);">SOAP note will appear here after generation</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.patient_records:
            st.markdown('<div class="section-label" style="margin-top:1.5rem;">Session Patient Records</div>', unsafe_allow_html=True)
            for pid, rec in reversed(list(st.session_state.patient_records.items())):
                label = f"👤 {rec['name']} ({pid}) — {rec['age']}y · {rec['gender']}"
                
                if st.button(label, key=f"btn_{pid}", use_container_width=True):
                    st.session_state.active_patient = pid
                    st.session_state["last_soap"] = rec["soap_notes"][-1]["soap"] if rec.get("soap_notes") else ""
                    st.session_state["last_soap_patient"] = rec["name"]
                    st.rerun()