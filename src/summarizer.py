# Autor: Basia



# Moduł odpowiedzialny za tworzenie krótkiego streszczenia na podstawie danych od Oli.





from openai import AzureOpenAI


from config import AzureConfig








#????????#


# from modul_interpretacji import zrob_interpretacje 


# nie jestem pewna czy trzeba importować w moim pliku plik od Oli. 


# Wydaje mi sie ze takie dane powinny być zbiorczo zebrane w pliku gradio???








def _build_prompt(interpreted_data: str) -> str:


    """


    Tworzy prompt dla modelu. Dodaje instrukcje + dane od Oli.


    """


    prompt = f"""


You are a business assistant who creates short, clear summaries of provided data.


Based on the interpretation below, prepare a concise summary in English,


understandable for a non-technical reader.





Guidelines:


- Maximum 4–6 sentences.


- Style: professional, concise, focused on conclusions.


- Avoid technical jargon.


- Focus on trends, differences, changes, and key figures.


- Do not repeat raw data — describe them in words.


- If the data shows growth/decline – state it clearly.


- Do not add any information that is not present in the interpretation.





DATA FOR SUMMARY:


{interpreted_data}


    """


    return prompt








def create_summary(interpreted_data: str) -> str:


    """


    Główna funkcja modułu streszczenia.


    Waliduje dane od Oli, łączy się z Azure OpenAI i zwraca zwięzłe podsumowanie.


    """





    # -------------------------


    # 1. Walidacja danych wejściowych


    # -------------------------


    if not interpreted_data or not isinstance(interpreted_data, str):


        return "⚠️ Error: The data for summarization is invalid."





    if len(interpreted_data.strip()) < 10:


        return "⚠️ Error: The received interpretation is too short."





    # -------------------------


    # 2. Połączenie z Azure OpenAI


    # -------------------------


    try:


        client = AzureOpenAI(


            azure_endpoint=AzureConfig.OPENAI_ENDPOINT,


            api_key=AzureConfig.OPENAI_API_KEY,


            api_version=AzureConfig.OPENAI_API_VERSION,


        )


    except Exception as e:


        return f"❌ Connection error with Azure OpenAI: {e}"





    # -------------------------


    # 3. Budowanie promptu


    # -------------------------


    prompt = _build_prompt(interpreted_data)





    # -------------------------


    # 4. Wywołanie modelu


    # -------------------------


    try:


        response = client.chat.completions.create(


            model=AzureConfig.OPENAI_DEPLOYMENT_NAME,


            messages=[


                {"role": "system", "content": "You are a helpful business assistant."},


                {"role": "user", "content": prompt},


            ],


            max_tokens=250,


            temperature=0.3,


        )





        return response.choices[0].message["content"]





    except Exception as e:


        return f"❌ Error while generating summary: {e}"








# ---------------------------------------------------------


# NAJPROSTSZA FUNKCJA – SHORT SUMMARY (1 zdanie)


# ---------------------------------------------------------


def create_short_summary(interpreted_data: str) -> str:


    """


    Tworzy bardzo krótkie, jednozdaniowe podsumowanie.


    """





    if not interpreted_data or not isinstance(interpreted_data, str):


        return "⚠️ Error: The data for short summary is invalid."





    # Połączenie z Azure OpenAI


    try:


        client = AzureOpenAI(


            azure_endpoint=AzureConfig.OPENAI_ENDPOINT,


            api_key=AzureConfig.OPENAI_API_KEY,


            api_version=AzureConfig.OPENAI_API_VERSION,


        )


    except Exception as e:


        return f"❌ Connection error with Azure OpenAI: {e}"





    # Najprostszy możliwy prompt


    prompt = f"""


Create a one-sentence short summary describing the main trend or key insight.


Be concise and rely only on the interpretation below.





INTERPRETATION:


{interpreted_data}


"""





    # Wywołanie modelu


    try:


        response = client.chat.completions.create(


            model=AzureConfig.OPENAI_DEPLOYMENT_NAME,


            messages=[


                {"role": "system", "content": "You are a helpful business assistant."},


                {"role": "user", "content": prompt},


            ],


            max_tokens=40,


            temperature=0.2,


        )





        return response.choices[0].message["content"]





    except Exception as e:


        return f"❌ Error while generating short summary: {e}"