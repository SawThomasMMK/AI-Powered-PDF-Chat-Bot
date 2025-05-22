import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Streamlit setup
st.set_page_config(page_title="📄 Gemini PDF Chatbot")
st.title("📄 Chat with your PDF using Gemini AI")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Read PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content

    if not text.strip():
        st.error("❌ No text found in the PDF.")
    else:
        st.success("✅ PDF loaded successfully!")
        question = st.text_input("Ask a question about the PDF")

        if question:
            with st.spinner("Thinking..."):
                try:
                    # Limit prompt size (optional)
                    limited_text = text[:4000]
                    prompt = f"Based on this document:\n\n{limited_text}\n\nAnswer this question:\n{question}"
                    
                    response = model.generate_content(prompt)
                    st.write("🧠 **Response:**")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"❌ Error from Gemini: {e}")
