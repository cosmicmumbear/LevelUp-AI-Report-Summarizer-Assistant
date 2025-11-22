#Druga wersja UI dla chetnych co maja stremlit :)

import streamlit as st
import os
from src.pipeline import analyze_report_file

# Ścieżki do przykładowych plików
example_file_path = os.path.join(os.getcwd(), "data")
example_1 = os.path.join(example_file_path, "Wydatki.pdf")
example_2 = os.path.join(example_file_path, "Wydatki.png")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Stylizacja pastelowa ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ffe6f2 0%, #e6fff7 100%);
        font-family: "Comic Sans MS", cursive, sans-serif;
    }
    .stApp {
        background-color: transparent;
    }
    h1, h2, h3 {
        color: #ff66b2;
        text-shadow: 1px 1px #aaffcc;
    }
    .bear {
        font-size: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI ---
st.title("🐻 Awesome & Best Ever Chart Analysis Assistant 🐻")
st.subheader("Hello My Dear Friend! 🌸🌿")
st.write("Upload a **PNG** or **PDF** file with a chart to get detailed analysis and insights.")

# Upload pliku
uploaded_file = st.file_uploader("📂 Upload your chart file", type=["png", "pdf"])

# Przykłady
st.write("Or try with example files:")
col1, col2 = st.columns(2)
with col1:
    if st.button("🐻 Example PDF"):
        uploaded_file = open(example_1, "rb")
with col2:
    if st.button("🐻 Example PNG"):
        uploaded
