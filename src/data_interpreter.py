"""Task 2: Interpretacja Danych z OCR (AI Visual Data Reporter)"""
# Task 2 - Interpretation of OCR Data
# Purpose:
# 1. Takes raw text from Vision SDK (OCR)
# 2. Cleans and analyzes data
# 3. Creats a clear description in natural language, 
#  with modules: Name of chart, Source of chart, Type of chart, Variables, Units,
#                Topic of chart, Trends, Highest and lowest values, Confidence of your answers

from config import AzureConfig
# Configuration environment to use Azure resources, 
# taking information like: API_KEY, API_ENDPOINT from .env

from azure.ai.openai import AzureOpenAI 
# setup communication with Azure OpenAI resources 


def interpret(ocr_text: str) -> str:
    """
    Analyzes raw data from OCR and gives key information about chart.
    """
    print("\n=== INTERPRETATION OF OCR DATA ===")
    # Informing we start interpreting procedure
    
    # PROMPT
    prompt = f"""
    Interpret the following OCR text extracted from a chart.
    Your task is to clean OCR errors, recover numeric values, and extract structured information.

    IMPORTANT RULES:
    - Do NOT guess missing information. If something is not present, return "unknown".
    - Use only the content that appears in the OCR text.
    - Identify the chart type only if it can be clearly determined (e.g., bar, line, pie, scatter).
    If the type is ambiguous or unclear, return "unknown".
    The list of chart types is not exhaustive.

    Return the result in the following structured form:

    - Name of chart: <cleaned title or "unknown">
    - Source of chart: <if mentioned, otherwise "unknown">
    - Type of chart: <as defined above>
    - Variables (axes or categories): <list of variables extracted from the text>
    - Units: <if identified, otherwise "unknown">
    - Topic of chart (1–2 sentences): <short explanation of what the chart describes>
    - Trends (2–3 sentences): <main trend(s) visible in the data>
    - Highest and lowest values: <specify category + value for highest and lowest>
    - Confidence of your answers: <low / medium / high>

    OCR data:
    {ocr_text}

    """

    try:
        # Connection to Azure OpenAI
        client = AzureOpenAI(
            azure_endpoint=AzureConfig.AZURE_OPENAI_ENDPOINT,
            api_key=AzureConfig.AZURE_OPENAI_KEY
        )
        # azure_endpoint = Adress od our END_POINT w Azure
        # api_key = passwort to Azure API
        
        # Sending question to GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.0,
            max_tokens=400,
            messages=[
                {"role": "system", "content": "You are an expert of data analysis and charts."},
                {"role": "user", "content": prompt}
            ]
        )
        # This is "conversation with GPT-4"
        # - System: mówi modelowi kim ma być (ekspertem) gives role to AI model
        # - User: wysyła faktyczne dane OCR do interpretacji sends OCR-data to interpret 

        output = response.choices[0].message.content.strip()
        # Taking the answer
        # .choice[0] = choosing first proposition of models answer
        # .message.content = it's the messeage itself without metadata
        # .strip() = deleting unnessesery spaces and enters

        print("\n--- Interpretation results ---")
        print(output)
        # printing the result for testing
        
        return output
        # Saving results for further steps in main

    except Exception as e:
        # If any errors (internet connection, invalid credentials in .env)
        print(f"\nError: {e}")
        return "Nie udało się zinterpretować danych OCR. Could not interpret OCR data"

# LOCAL TEST
# Data for testing in local envirement
if __name__ == "__main__":
    test1 = """
    Chart title: Sales 2024
    Q1: 100
    Q2: 120
    Q3: 150
    Q4: 130
    """
    test2 = """Fig. 1 Sales 2023 Report
    SaIes by quarter (USD)

    Q1    25.OOO
    Q2  31 500
    Q3  29,8OO
    Q4   34.200

    -- Chart Title: "Yearly Sales 2023"
    X-axis: Q1 Q2 Q3     Q4
    Y-axis: Sales in USD (thous.)

    Bars:
    Q1: 25000
    Q2 :31500
    Q3: 29800_
    Q4.: 34200

    Note: Data Source: C0mpany Intemal Reporting
    *strong growth in Q2
    *sLight dip Q3 bUt recovery Q4
    ©C0pyright 2023

    S a 1 e s   2 0 2 3
    (Chart n° 04) """
    output = interpret(test2)
    print("\nInterpreted data:")
    print(output)
    

