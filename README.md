# LevelUp-AI-Report-Summarizer-Assistant

## TEMAT
AI Report Summarizer – Asystent, który przetwarza raporty z wykresami (np. PNG, PDF) i generuje podsumowanie danych.  

**Zakres:**  
- OCR / Vision SDK – odczyt tekstu z wykresu  
- GPT-4o Vision SDK – interpretacja danych  
- Generowanie streszczenia (OpenAI Completions)  
- Testy jakości i prezentacja wyników  
- UI demo  

---

# NASZA PROPOZJA
# The application demonstrates how PDFs and images can be ingested, scanned, and intelligently summarized.  

---

## Workflow
1. Greet the user and ask for a file with a chart to analyze (PNG/PDF).  
2. Upload the file.
3. Use the **OCR/Vision SDK** endpoint to extract text from the file.  
4. Send the extracted text to **Azure OpenAI** for analysis and interpretation.  
5. Forward the interpreted content to **OpenAI Completions** to generate a summary.  
6. Display the results (steps 3–5) in the UI.  

---

## Prerequisites
- Active Azure subscription  
- Installed dependencies from `requirements.txt`  
- Python 3.9+  

---

## .env Configuration
At the root of the repo, create a `.env` file with the following structure (replace placeholders with your values):

```env
================================
Azure Computer Vision (dla czesci OCR)
================================
VISION_ENDPOINT=""
VISION_KEY=""
================================
Azure OpenAI (dla summarizer.py i data_interpreter.py)
================================
AZURE_OPENAI_VERSION =""  
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_KEY=""
AZURE_OPENAI_DEPLOYMENT_NAME =""
```
---

## Running the App Locally

1. Install dependencies:

    python -m pip install -r requirements.txt

2. Start the application: 

    python app.py

3. Upload your file through the UI.
4. After a few seconds, enjoy the summarized results of your awesome application 😄

### Roadmap

⚠️ Be aware that version 2.0 is coming soon… with big bear foot 🐾
