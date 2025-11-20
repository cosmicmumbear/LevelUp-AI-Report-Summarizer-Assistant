"""
modul_ocr.py
Moduł do ekstrakcji tekstu z plików PNG i PDF przy użyciu OCRProcessor (Azure Read API).
"""

import os  # Operacje na plikach i ścieżkach
from azure.core.exceptions import HttpResponseError  # Obsługa błędów z Azure OCR API
from ocr_processor import OCRProcessor
from .config import AzureConfig
from typing import Any


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

    processor = OCRProcessor()  # Tworzymy instancję klasy OCRProcessor
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
        result = processor._poll_for_result(operation_id)
        if result:
            processed = processor._process_read_result(
                result,
                plik,
                description="Local file OCR",
                language=None,
                elapsed_time=0,
            )
            return processed.get("full_text", "")  # Zwracamy rozpoznany tekst
        else:
            print("✗ OCR nie zwrócił wyniku.")
            return ""
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
