RED_FLAGS = [
    "chest pain", "unconscious", "seizure", "bleeding", "can't breathe",
    "cannot breathe", "difficulty breathing", "altered consciousness",
    "severe headache", "stiff neck", "petechiae", "hemorrhage", "shock",
    "respiratory distress", "cyanosis"
]

import streamlit as st
from datetime import datetime

def check_red_flags(text: str) -> list:
    text_lower = text.lower()
    return [rf for rf in RED_FLAGS if rf in text_lower]

def save_patient_record(pid, name, age, gender, chief_complaint):
    if pid not in st.session_state.patient_records:
        st.session_state.patient_records[pid] = {
            "name": name, "age": age, "gender": gender,
            "chief_complaint": chief_complaint,
            "soap_notes": [],
            "created": datetime.now().strftime("%d %b %Y, %H:%M"),
        }

def add_soap_note(pid, soap_text, raw_input):
    if pid in st.session_state.patient_records:
        st.session_state.patient_records[pid]["soap_notes"].append({
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
            "raw": raw_input,
            "soap": soap_text,
        })