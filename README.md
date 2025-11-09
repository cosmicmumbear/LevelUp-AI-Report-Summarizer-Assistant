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
- Python 3.9 or greater
- Access permissions to create Azure OpenAI resources and to deploy models.

## .env
You will need to configure a .env file at the root of the repo that looks similar to the below. Make sure to replace the placeholders with your specific values.
{
API_KEY="YourApiKey"
API_ENDPOINT="YourEndpoint"
API_VERSION="2024-12-01-preview"
DEPLOYMENT="gpt-4o"
}


