"""
modul_ocr.py
Moduł do ekstrakcji tekstu z plików PNG i PDF przy użyciu OCRProcessor (Azure Read API).
"""

import os  # Operacje na plikach i ścieżkach
from azure.core.exceptions import HttpResponseError  # Obsługa błędów z Azure OCR API
import time
from typing import Any
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from src.config import AzureConfig


def get_text_from_file(plik: Any) -> str:
    """
    Ekstrakcja tekstu z pliku PNG lub PDF przy użyciu Azure Computer Vision Read API.
    :param plik: Ścieżka do pliku lokalnego (PNG lub PDF).
    :return: Rozpoznany tekst jako string (lub pusty string w przypadku błędu).
    """
    client = AzureConfig.get_computer_vision_client()

    if not os.path.isfile(plik):
        raise FileNotFoundError(
            f"Plik '{plik}' nie istnieje."
        )  # Walidacja istnienia pliku

    ext = os.path.splitext(plik)[1].lower()
    if ext not in [".png", ".pdf", ".jpg", ".jpeg"]:
        raise ValueError(
            "Obsługiwane formaty: PNG, JPG, JPEG, PDF."
        )  # Walidacja rozszerzenia

    try:
        # Otwieramy plik w trybie binarnym
        with open(plik, "rb") as f:
            print(f"Rozpoczynam OCR dla pliku: {plik} ---")
            # Wywołanie Read API dla strumienia pliku

            read_response: Any = client.read_in_stream(f, raw=True)
            headers = read_response.headers

            # Pobieramy wartość bezpiecznie metodą .get()
            operation_location = headers.get("Operation-Location")

        # Jeśli Azure nie zwrócił lokalizacji operacji (co byłoby dziwne, ale możliwe przy błędzie)
        if not operation_location:
            print("⚠️ Błąd Azure: Brak nagłówka Operation-Location.")
            return ""
        operation_id = operation_location.split("/")[-1]  # Wyciągnięcie ID operacji

        # Polling na wynik
        while True:
            read_result: Any = client.get_read_result(operation_id)
            if read_result.status not in ["notStarted", "running"]:
                break
            time.sleep(1)

        # 6. Przetwarzanie wyniku - ZAMIAST processor._process_read_result
        if read_result.status == OperationStatusCodes.succeeded:
            text_results = []
            if read_result.analyze_result and read_result.analyze_result.read_results:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text_results.append(line.text)

            final_text = "\n".join(text_results)
            return final_text if final_text else "OCR sukces, ale brak tekstu."
        else:
            return "Błąd rozpoznawania tekstu przez Azure."
    except HttpResponseError as e:
        print(f"✗ Błąd OCR: {e.message}")  # Obsługa błędów Azure
        return ""
    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")  # Obsługa innych błędów
        return ""


if __name__ == "__main__":
    """
    Demonstracja działania funkcji get_text_from_file.
    Użycie:
        python modul_ocr.py <ścieżka_do_pliku>
    Obsługiwane formaty: PNG, JPG, JPEG, PDF
    """

    import sys

    if len(sys.argv) < 2:
        print("❗ Podaj ścieżkę do pliku jako argument.")
        print("Przykład: python modul_ocr.py dokument.pdf")
        sys.exit(1)

    plik = sys.argv[1]

    try:
        tekst = get_text_from_file(plik)
        if tekst.strip():
            print("\n✅ Rozpoznany tekst:")
            print("-" * 70)
            print(
                tekst[:1000] + ("..." if len(tekst) > 1000 else "")
            )  # Podgląd pierwszych 1000 znaków
            print("-" * 70)

            # Zapisz do pliku .txt o tej samej nazwie co plik wejściowy z suffixem _result
            base_name = os.path.splitext(os.path.basename(plik))[0]
            output_file = base_name + "_result.txt"
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(tekst)
            print(f"\n💾 Rezultat zapisany do pliku: {output_file}")

        else:
            print("⚠ Brak rozpoznanego tekstu.")
    except Exception as e:
        print(f"❌ Wystąpił błąd: {e}")
