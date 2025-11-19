
"""
modul_ocr.py
Moduł do ekstrakcji tekstu z plików PNG i PDF przy użyciu OCRProcessor (Azure Read API).
"""

import os
from azure.core.exceptions import HttpResponseError
from ocr_processor import OCRProcessor

def get_text_from_file(plik: str) -> str:
    """
    Ekstrakcja tekstu z pliku PNG lub PDF przy użyciu Azure Computer Vision Read API.
    :param plik: Ścieżka do pliku lokalnego (PNG lub PDF).
    :return: Rozpoznany tekst jako string (lub pusty string w przypadku błędu).
    """
    if not os.path.isfile(plik):
        raise FileNotFoundError(f"Plik '{plik}' nie istnieje.")

    ext = os.path.splitext(plik)[1].lower()
    if ext not in [".png", ".pdf", ".jpg", ".jpeg"]:
        raise ValueError("Obsługiwane formaty: PNG, JPG, JPEG, PDF.")

    processor = OCRProcessor()
    try:
        # Otwieramy plik w trybie binarnym
        with open(plik, "rb") as f:
            print(f"Rozpoczynam OCR dla pliku: {plik} ---")
            # Wywołanie Read API dla strumienia pliku
            read_operation = processor.client.read_in_stream(f, raw=True)
            operation_location = read_operation.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

        # Polling na wynik
        result = processor._poll_for_result(operation_id)
        if result:
            processed = processor._process_read_result(result, plik, description="Local file OCR", language=None, elapsed_time=0)
            return processed.get("full_text", "")
        else:
            print("✗ OCR nie zwrócił wyniku.")
            return ""
    except HttpResponseError as e:
        print(f"✗ Błąd OCR: {e.message}")
        return ""
    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")
        return ""
