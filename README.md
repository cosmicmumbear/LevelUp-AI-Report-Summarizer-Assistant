### LevelUp-AI-Report-Summarizer-Assistant
# TEMAT:
AI Report Summarizer - Asystent, który przetwarza raporty z wykresami (np. PNG, PDF) i generuje podsumowanie danych.
Zakres: 
- OCR / Vision SDK – odczyt tekstu z wykresu. 
- GPT-4o Vision SDK – interpretacja danych.
- Generowanie streszczenia (OpenAI completions). 
- Testy jakości i prezentacja wyników.
- UI demo.
  
### NASZA PROPOZYCJA

The application showcases how PDFs can be ingested and intelligently scanned to determine their content.

## The application's workflow is as follows:

    1. Say Hello My Friend and ask for file with chart to analyse (PNG/PDF)
    2. PNGs/PDFs are uploaded to a blob storage input container.
    3. Downloads the blob (PDF/PNG).
    4. Utilizes the OCR/Vision SDK endpoint to extract the text from the PNG/PDF.
    5. Sends the extracted text to Azure Open AI to analyze and determine the content of the file.
    6. Send the content of the file to the OpenAI Completions to create a summary.
    7. Save the summary results from Azure Open AI to a new file and upload it to the output blob container. / Print summary on the UI?  ?????(DZIEWCZYNY???)

Below, you will find the instructions to set up and run this app locally...

## Prerequsites
- Create an active Azure subscription.
- Install the latest Azure Functions Core Tools to use the CLI
- Python 3.10 or greater
- Access permissions to create Azure OpenAI resources and to deploy models.
- Gradio

## .env
You will need to configure a .env file at the root of the repo that looks similar to the below. Make sure to replace the placeholders with your specific values.
{
# ================================
# Azure Computer Vision (dla czesci OCR)
# ================================
VISION_ENDPOINT=""
VISION_KEY=""


# ================================
# Azure OpenAI (dla summarizer.py i data_interpreter.py)
# ================================
AZURE_OPENAI_VERSION =""  
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_KEY=""
AZURE_OPENAI_DEPLOYMENT_NAME =""
}

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
