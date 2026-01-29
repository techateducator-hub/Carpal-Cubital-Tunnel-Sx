import streamlit as st
import google.generativeai as genai

st.title("Model Checker")
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

try:
    st.write("Attempting to list available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"AVAILABLE: {m.name}")
except Exception as e:
    st.error(e)
