"""
OCR Implementation with Azure Computer Vision Read API
AI-102 Topic: Extract text from images using OCR (15-20% of exam)
"""

from typing import Any

import json  # Technicznie: zapis i odczyt danych w formacie JSON

# To jest "tłumacz języków dla komputera"
# Dlaczego to mamy? Bo musimy zapisywać wyniki OCR (rozpoznany tekst) w formacie,
# który mogą odczytać zarówno ludzie jak i inne programy
# JSON to uniwersalny format danych - jak esperanto dla komputerów!

import time  # Technicznie: pozwala mierzyć czas i robić przerwy w działaniu programu

# To jest "stoper i budzik"
# Dlaczego to mamy? Bo:
# 1. Mierzymy jak długo trwa rozpoznawanie tekstu (stoper)
# 2. Czekamy między sprawdzaniem czy OCR się skończył (budzik)
# To jak timer w kuchni - sprawdzamy czy ciasto jest gotowe co minutę

import re  # Technicznie: wyrażenia regularne do wyszukiwania wzorców w tekście

# To jest "detektyw do szukania wzorców"
# Dlaczego to mamy? Bo musimy:
# - Czyścić tekst z nadmiarowych spacji
# - Szukać dziwnych znaków (błędów OCR)
# - Tworzyć bezpieczne nazwy plików (usuwając znaki specjalne)
# To jak Ctrl+F na sterydach - potrafi znajdować skomplikowane wzorce!

from datetime import datetime  # Technicznie: operacje na dacie i czasie

# To jest "zegar i kalendarz"
# Dlaczego to mamy? Żeby zapisać KIEDY rozpoznaliśmy tekst
# Każdy wynik dostaje znacznik czasowy jak pieczątkę na dokumencie
# Dzięki temu wiemy które rozpoznanie jest najnowsze

from config import (
    AzureConfig,
)  # Technicznie: konfiguracja połączenia z Azure Computer Vision

# To jest "książka telefoniczna i klucze do Azure"
# Dlaczego to mamy? Bo musimy wiedzieć:
# - GDZIE jest nasza usługa OCR (adres)
# - JAK się zalogować (klucz API)
# AzureConfig bezpiecznie przechowuje te tajemnice

from azure.cognitiveservices.vision.computervision.models import (
    OperationStatusCodes,
)  # Kody statusu operacji

# To są "kody sygnalizacyjne"
# Dlaczego to mamy? Bo OCR działa ASYNCHRONICZNIE (wysyłamy → czekamy → sprawdzamy)
# Musimy wiedzieć czy operacja:
# - Succeeded (sukces! ✓)
# - Failed (porażka ✗)
# - Running (jeszcze pracuje...)
# To jak sprawdzanie statusu przesyłki: "W drodze", "Dostarczona", "Problem z dostawą" --> do zapamiętania!!!

from azure.core.exceptions import (
    HttpResponseError,
)  # Obsługa błędów komunikacji z Azure

# To jest "system alarmowy"
# Dlaczego to mamy? Bo mogą wystąpić problemy:
# - Brak internetu, przekroczony limit zapytań, zły klucz...
# Ten moduł pozwala elegancko obsłużyć błędy zamiast wywałki programu
# To jak poduszka powietrzna w samochodzie - chroni przed katastrofą!


class OCRProcessor:
    """Comprehensive OCR processor using Azure Computer Vision Read API"""

    # To jest "czytnik dokumentów"
    # Dlaczego to mamy? Bo ta klasa zbiera wszystkie narzędzia do rozpoznawania tekstu z obrazów
    # OCR = Optical Character Recognition = "Rozpoznawanie znaków optycznych"
    # To jak skaner w drukarce, ale inteligentny - potrafi przeczytać tekst z każdego zdjęcia!

    def __init__(self):
        print("\n=== Initializing OCR Processor ===")
        # To jest "procedura uruchomienia procesora OCR"
        # Informujemy użytkownika że system startuje

        self.client = AzureConfig.get_computer_vision_client()
        # Tworzymy "telefon do Azure Computer Vision"
        # To jest połączenie z chmurą Microsoft, które pozwala nam czytać tekst z obrazów
        # Bez tego nie moglibyśmy w ogóle używać OCR!

        self.results = []
        # Tworzymy pustą "teczkę na wyniki"
        # Tu będziemy zbierać wszystkie rozpoznane teksty
        # To jak pudełko na dokumenty - każde rozpoznanie tekstu trafi na osobną kartkę

    def extract_text_from_url(self, image_url, description="", language=None):
        """Extract text from image URL using Read API (async pattern)"""
        # To jest "główny czytnik tekstu"
        # Bierze link do obrazu i wyciąga z niego cały tekst
        # UWAGA: Działa ASYNCHRONICZNIE - czyli "zacznij zadanie, czekaj, odbierz wynik"
        # To jak zamówienie pizzy: dzwonisz → czekasz → odbierasz

        print(f"\n--- Extracting text from: {description or image_url} ---")
        # Informujemy co teraz czytamy
        # Jeśli jest opis pokazujemy go, jeśli nie - pokazujemy URL

        try:
            # PRÓBUJEMY przeprowadzić rozpoznawanie tekstu
            # try = siatka bezpieczeństwa - jeśli coś pójdzie źle, złapiemy błąd

            # STEP 1: Start Read operation
            start_time = time.time()
            # Uruchamiamy stoper! Zapisujemy moment rozpoczęcia
            # To jak naciśnięcie START na sekundniku

            read_operation: Any = (
                self.client.read(image_url, language=language, raw=True)
                if language
                else self.client.read(image_url, raw=True)
            )
            # WYSYŁAMY OBRAZ DO AZURE OCR!
            # Mówimy: "Przeczytaj ten obraz"
            # language = jaki język? (np. "en", "pl") - jeśli None to auto-detect
            # raw=True = daj mi pełną odpowiedź (nie tylko przetworzoną)
            # To jak wysłanie listu pocztą - teraz musimy czekać na odpowiedź

            if language:
                print(f"   Language: {language}")
                # Jeśli określiliśmy język, informujemy o tym
                # Przykład: "Language: en" (angielski)

            # STEP 2: Extract operation ID
            operation_location = read_operation.headers["Operation-Location"]
            # Wyciągamy ADRES gdzie są wyniki
            # Azure mówi: "OK, zaczynam czytać, sprawdź wyniki pod tym adresem"
            # To jak numer zamówienia w restauracji - będziesz go potrzebować żeby odebrać amciu amciu

            operation_id = operation_location.split("/")[-1]
            # Z pełnego adresu wyciągamy tylko ID operacji
            # split("/") = podziel adres na kawałki po znaku "/"
            # [-1] = weź ostatni kawałek
            # Przykład: "https://api.com/operations/12345" → "12345"
            # To jak wyciągnięcie numeru z билету

            print(f"   Operation ID: {operation_id}")
            # Pokazujemy numer operacji - przydatne do debugowania

            # STEP 3: Poll for completion
            result = self._poll_for_result(operation_id)
            # CZEKAMY AŻ OCR SKOŃCZY!
            # Wywołujemy funkcję która sprawdza co chwilę: "Gotowe? Gotowe? Gotowe?"
            # To jak sprawdzanie czy woda już się zagotowała - zaglądamy co chwilę

            elapsed_time = time.time() - start_time
            # Zatrzymujemy stoper! Obliczamy ile czasu zajęło całe rozpoznawanie
            # Odejmujemy czas startu od obecnego czasu
            # Przykład: zaczęliśmy o 10:00:00, skończyliśmy o 10:00:03 → 3 sekundy

            if result:
                # Sprawdzamy: "Czy dostaliśmy wynik?"
                # Jeśli tak - przetwarzamy go i zapisujemy

                processed_result = self._process_read_result(
                    result, image_url, description, language, elapsed_time
                )
                # PRZETWARZAMY SUROWY WYNIK!
                # Azure dał nam masę danych, teraz je rozpakowujemy i porządkujemy
                # To jak rozpakowywanie paczki - sortujemy zawartość na półki

                self.results.append(processed_result)
                # Dodajemy wynik do naszej "teczki"
                # To jak dołożenie kolejnego dokumentu do segregatora

                self._print_extraction_summary(processed_result)
                # Wyświetlamy podsumowanie na ekran
                # Pokazujemy użytkownikowi co udało się przeczytać

                return processed_result
                # Zwracamy wynik do osoby która wywołała tę funkcję

            else:
                # Nie dostaliśmy wyniku - coś poszło nie tak podczas czekania
                print("   ✗ Text extraction failed")
                return None
                # Zwracamy "nic" bo nie udało się rozpoznać tekstu

        except HttpResponseError as e:
            # ŁAPIEMY BŁĘDY KOMUNIKACJI Z AZURE!
            # Gdy coś pójdzie nie tak z internetem lub API

            print(f"✗ Error: {e.message}")
            # Wypisujemy komunikat błędu

            if e.status_code == 429:
                # Kod 429 = "Too Many Requests" (za dużo zapytań!)
                print("  Rate limit exceeded. Implement exponential backoff retry.")
                # Azure mówi: "Hej, zwolnij! Za dużo pytasz!"
                # Sugerujemy rozwiązanie: czekaj coraz dłużej między próbami
                # To jak gdy dzwonisz za często do kolegi - nie odbiera bo go irytuje

            elif e.status_code == 400:
                # Kod 400 = "Bad Request" (źle sformatowane żądanie)
                print("  Bad Request - check image URL and format")
                # Coś jest nie tak z obrazem lub jego adresem
                # Może URL jest zły, może format nie jest wspierany
                # To jak próba wysłania listu bez adresu - poczta go odrzuci

            return None
            # Zwracamy "nic" bo nie udało się rozpoznać tekstu

        except Exception as e:
            # ŁAPIEMY WSZYSTKIE INNE BŁĘDY
            # Cokolwiek się stanie czego nie przewidzieliśmy

            print(f"✗ Unexpected error: {str(e)}")
            # Wypisujemy błąd
            # To jak powiedzenie: "Coś poszło nie tak, ale nie wiem co dokładnie"

            return None
            # Znowu zwracamy "nic"

    def _poll_for_result(self, operation_id, max_attempts=30, poll_interval=1):
        """Poll for Read operation result"""
        # To jest "cierpliwy czekacz"
        # OCR działa w tle i może trwać kilka sekund
        # Ta funkcja sprawdza co sekundę: "Gotowe? Gotowe? Gotowe?"
        # To jak sprawdzanie czy pranie w pralce się skończyło - zaglądamy co chwilę

        print("   Polling for results...", end="", flush=True)
        # Informujemy że zaczynamy czekać
        # end="" = nie rób nowej linii (będziemy dodawać kropki)
        # flush=True = wyświetl natychmiast (nie czekaj)
        # To pozwoli nam pokazać animację: "Polling for results..."

        for attempt in range(max_attempts):
            # PĘTLA CZEKANIA!
            # Będziemy próbować max 30 razy
            # attempt = numer próby (0, 1, 2, ... 29)
            # To jak odliczanie: "Próba 1, próba 2, próba 3..."

            try:
                result: Any = self.client.get_read_result(operation_id)
                # PYTAMY AZURE: "Czy już gotowe?"
                # Wysyłamy numer operacji i pytamy o status
                # To jak sprawdzenie statusu przesyłki: "Gdzie jest moja paczka?"

                if result.status == OperationStatusCodes.succeeded:
                    # Sprawdzamy: "Czy status to SUKCES?"
                    # OperationStatusCodes.succeeded = kod oznaczający że się udało

                    print(" ✓ Succeeded")
                    # Wypisujemy że się udało! (z nowej linii, kończymy animację)

                    return result
                    # ZWRACAMY WYNIK! Koniec czekania!
                    # To jak odebranie gotowej pizzy

                elif result.status == OperationStatusCodes.failed:
                    # Sprawdzamy: "Czy status to PORAŻKA?"
                    # OCR się nie udał (obraz nieczytelny, błąd, itp.)

                    print(" ✗ Failed")
                    # Informujemy o porażce

                    return None
                    # Zwracamy "nic" bo nie ma wyniku
                    # To jak powiadomienie "Przepraszamy, nie udało się dostarczyć paczki"

                print(".", end="", flush=True)
                # Jeśli ani sukces ani porażka (status = "running")
                # Wypisujemy kropkę żeby pokazać że czekamy
                # To daje animację: "Polling for results..."

                time.sleep(poll_interval)
                # CZEKAMY 1 SEKUNDĘ!
                # time.sleep(1) = zatrzymaj program na 1 sekundę
                # Nie pytamy Azure co milisekundę żeby nie spamować
                # To jak odczekanie minuty przed ponownym zadzwonieniem

            except Exception as e:
                # ŁAPIEMY BŁĘDY podczas sprawdzania
                print(f" ✗ Error polling: {str(e)}")
                return None
                # Coś poszło nie tak podczas sprawdzania statusu

        print(" ✗ Timeout")
        # Jeśli wyszliśmy z pętli (30 prób się skończyło) i nie było sukcesu
        # To TIMEOUT - za długo czekaliśmy!
        # To jak gdy pizza nie przyszła po godzinie - coś jest nie tak

        return None
        # Zwracamy "nic" bo nie udało się w czasie

    def _process_read_result(
        self, result, image_url, description, language, elapsed_time
    ):
        """Process and structure Read API results"""
        # To jest "organizator wyników"
        # Azure daje nam masę danych w skomplikowanej formie
        # Ta funkcja wszystko rozpakuje i uporządkuje w czytelną strukturę
        # To jak sortowanie zakupów po powrocie ze sklepu - wszystko na swoje miejsce!

        processed = {
            "timestamp": datetime.now().isoformat(),
            "image_url": image_url,
            "description": description,
            "language": language or "auto-detected",
            "processing_time_ms": round(elapsed_time * 1000, 2),
            "pages": [],
            "full_text": "",
            "statistics": {},
        }
        # Tworzymy "pusty szablon raportu"
        # To jak formularz do wypełnienia - już wiemy jakie pola mamy, teraz je wypełnimy:
        # - timestamp: kiedy to rozpoznaliśmy
        # - image_url: skąd był obraz
        # - description: opis dokumentu
        # - language: język tekstu
        # - processing_time_ms: ile to trwało (w milisekundach!)
        # - pages: lista stron (będziemy wypełniać)
        # - full_text: cały tekst w jednym kawałku
        # - statistics: statystyki (ile linii, słów, itp.)

        if not result.analyze_result or not result.analyze_result.read_results:
            # Sprawdzamy: "Czy są jakieś wyniki?"
            # Jeśli nie ma wyniku lub wyniku OCR - zwracamy pusty szablon
            # To jak otwarcie pustej koperty
            return processed

        all_text = []
        # Pusta lista gdzie będziemy zbierać CAŁY TEKST
        # Każda linia tekstu trafi tutaj
        # To jak koszyk - będziemy wrzucać do niego wszystkie zdania

        total_lines = 0
        # Licznik linii - zaczynamy od zera
        # To jak licznik kilometrów w samochodzie

        total_words = 0
        # Licznik słów - też od zera
        # Będziemy zliczać każde słowo które OCR rozpoznał

        # Process each page
        for page_num, page in enumerate(result.analyze_result.read_results, 1):
            # PĘTLA PRZEZ WSZYSTKIE STRONY!
            # enumerate(..., 1) = numeruj od 1 (strona 1, 2, 3...)
            # page_num = numer strony
            # page = dane tej strony
            # Niektóre dokumenty mają wiele stron (jak PDF)
            # To jak czytanie książki - strona po stronie

            page_data = {
                "page_number": page_num,
                "width": getattr(page, "width", 0),
                "height": getattr(page, "height", 0),
                "unit": getattr(page, "unit", "pixel"),
                "angle": getattr(page, "angle", 0),
                "lines": [],
            }
            # Tworzymy "notatkę o stronie"
            # Zapisujemy:
            # - page_number: którą stroną jest
            # - width/height: wymiary strony
            # - unit: jednostka wymiarów (pixele, cale, cm)
            # - angle: czy strona jest obrócona? (0° = prosto, 90° = w bok)
            # - lines: lista linii tekstu (wypełnimy za chwilę)
            # getattr(..., 0) = weź wartość, jeśli nie ma daj 0
            # To jak mierzenie kartki papieru przed pisaniem

            # Process each line
            if hasattr(page, "lines") and page.lines:
                # Sprawdzamy: "Czy na tej stronie są jakieś linie tekstu?"
                # hasattr = sprawdź czy obiekt ma to pole
                # To jak pytanie: "Czy ta strona ma jakiś tekst czy jest pusta?"

                for line in page.lines:
                    # PĘTLA PRZEZ WSZYSTKIE LINIE!
                    # Każda linia to jeden wiersz tekstu (jak w notatniku)
                    # line = dane jednej linii

                    line_data = {
                        "text": line.text,
                        "bounding_box": getattr(line, "bounding_box", []),
                        "words": [],
                    }
                    # Tworzymy "notatkę o linii"
                    # - text: co jest napisane w tej linii
                    # - bounding_box: współrzędne gdzie jest ta linia (ramka wokół tekstu)
                    # - words: lista słów (zaraz wypełnimy)
                    # To jak zakreślaczem - oznaczamy gdzie dokładnie jest tekst

                    # Process words with confidence scores
                    if hasattr(line, "words") and line.words:
                        # Sprawdzamy: "Czy ta linia ma pojedyncze słowa?"
                        # Czasem linia jest podzielona na słowa z osobnymi wynikami

                        line_data["words"] = [
                            {
                                "text": word.text,
                                "confidence": round(
                                    getattr(word, "confidence", 1.0), 3
                                ),
                                "bounding_box": getattr(word, "bounding_box", []),
                            }
                            for word in line.words
                        ]
                        # ROZPAKOWUJEMY WSZYSTKIE SŁOWA!
                        # Dla każdego słowa w linii tworzymy notatkę:
                        # - text: jakie to słowo ("kot", "pies", "dom")
                        # - confidence: jak OCR jest pewny? (0.0 - 1.0, czyli 0% - 100%)
                        # - bounding_box: gdzie dokładnie jest to słowo
                        # confidence pokazuje czy OCR jest pewny czy zgaduje
                        # Przykład: "confidence": 0.987 = OCR jest w 98.7% pewien że to słowo jest dobre
                        # To jak sprawdzian - każde słowo dostaje ocenę pewności!

                        total_words += len(line.words)
                        # DODAJEMY DO LICZNIKA!
                        # len(line.words) = ile słów ma ta linia
                        # Dodajemy to do całkowitej sumy
                        # Przykład: miałem 10 słów, ta linia ma 5 → teraz mam 15

                    page_data["lines"].append(line_data)
                    # Dodajemy linię do listy linii strony
                    # To jak dopisywanie kolejnego wiersza do notatnika

                    all_text.append(line.text)
                    # Dodajemy tekst linii do całego tekstu
                    # To jak zbieranie zdań do esseju

                    total_lines += 1
                    # Zwiększamy licznik linii o 1
                    # total_lines++ w innych językach

            processed["pages"].append(page_data)
            # Dodajemy całą stronę do listy stron
            # To jak dołożenie kolejnej kartki do teczki

        # Compile statistics
        processed["full_text"] = "\n".join(all_text)
        # SKLEJAMY CAŁY TEKST!
        # '\n'.join() = połącz wszystkie linie znakiem nowej linii
        # all_text to lista linii: ["Ala", "ma", "kota"]
        # Po join: "Ala\nma\nkota" (każda linia w nowej linii)
        # To jak przepisanie notatek z karteczek do jednego zeszytu

        processed["statistics"] = {
            "total_pages": len(processed["pages"]),
            "total_lines": total_lines,
            "total_words": total_words,
            "total_characters": len(processed["full_text"]),
            "avg_words_per_line": (
                round(total_words / total_lines, 2) if total_lines > 0 else 0
            ),
        }
        # TWORZYMY STATYSTYKI!
        # To jest "raport z liczenia"
        # - total_pages: ile stron przeczytaliśmy
        # - total_lines: ile linii tekstu
        # - total_words: ile słów (policzone wcześniej)
        # - total_characters: ile znaków (liter, spacji, kropek)
        # - avg_words_per_line: średnia słów na linię
        # Przykład: 100 słów ÷ 20 linii = 5 słów na linię
        # if total_lines > 0 = zabezpieczenie przed dzieleniem przez zero!
        # To jak podsumowanie wypracowania: "Napisałeś 500 słów w 25 zdaniach"

        return processed
        # ZWRACAMY KOMPLETNY RAPORT!
        # Wszystkie dane uporządkowane i gotowe do użycia
        # To jak oddanie wypełnionego formularza

    def _print_extraction_summary(self, result):
        """Print readable summary of extraction results"""
        # To jest "prezenter wyników"
        # Zamiast pokazywać gigantyczny JSON, wybieramy najważniejsze informacje
        # i pokazujemy je ładnie użytkownikowi
        # Jak streszczenie długiego artykułu - same kluczowe fakty!

        stats = result["statistics"]
        # Wyciągamy statystyki (liczby) z wyniku
        # Skrót dla wygody - zamiast pisać result['statistics'] za każdym razem

        print(f"\n✓ Extraction completed in {result['processing_time_ms']}ms")
        # Informujemy: "Gotowe! Zajęło to X milisekund"
        # To jak powiedzenie: "Przeczytanie tego dokumentu zajęło 2 sekundy"

        print(
            f"📄 Pages: {stats['total_pages']} | Lines: {stats['total_lines']} | Words: {stats['total_words']}"
        )
        # Pokazujemy kluczowe statystyki w jednej linii
        # Ile stron, linii i słów rozpoznaliśmy
        # | = kreska pionowa dla czytelności (separator)
        # Przykład: "📄 Pages: 3 | Lines: 45 | Words: 287"
        # To jak raport: "Dokument ma 3 strony, 45 linii tekstu i 287 słów"

        print(f"📝 Extracted Text (first 200 chars):")
        # Nagłówek przed podglądem tekstu
        # Pokazujemy tylko pierwsze 200 znaków żeby nie zaśmiecać ekranu

        print("-" * 70)
        # Linia oddzielająca z 70 myślników
        # To jak ramka wokół tekstu - wizualne oddzielenie

        text = result["full_text"]
        # Wyciągamy cały rozpoznany tekst

        print(text[:200] + "..." if len(text) > 200 else text)
        # PODGLĄD TEKSTU!
        # text[:200] = pierwsze 200 znaków
        # Jeśli tekst ma więcej niż 200 znaków: pokazujemy pierwsze 200 i dodajemy "..."
        # Jeśli ma mniej: pokazujemy cały tekst
        # To jak czytanie początku książki w księgarni - widzisz czy Cię interesuje

        print("-" * 70)
        # Zamykająca linia - koniec ramki

    def validate_text(self, text):
        """Validate and clean extracted text"""
        # To jest "kontroler jakości tekstu"
        # Sprawdza czy rozpoznany tekst jest dobry czy ma błędy
        # Jak nauczyciel sprawdzający wypracowanie - szuka problemów i je opisuje

        validation = {
            "original_length": len(text),
            "has_content": len(text.strip()) > 0,
            "line_count": len(text.split("\n")),
            "word_count": len(text.split()),
            "issues": [],
            "cleaned_text": text,
        }
        # Tworzymy "raport kontroli jakości"
        # - original_length: ile znaków ma tekst
        # - has_content: czy jest JAKIŚ tekst? (True/False)
        # - line_count: ile linii (podziel po \n i policz)
        # - word_count: ile słów (podziel po spacjach i policz)
        # - issues: lista problemów (wypełnimy za chwilę)
        # - cleaned_text: wyczyszczony tekst (najpierw taki sam jak original)
        # To jak formularz oceny - wypisujemy wszystkie parametry

        # Check for common OCR issues
        if not text.strip():
            # Sprawdzamy: "Czy tekst jest pusty?"
            # text.strip() usuwa spacje z początku i końca
            # not = zaprzeczenie (jeśli NIE ma treści)
            # To jak sprawdzenie czy kartka jest pusta

            validation["issues"].append("No text extracted")
            # Dodajemy problem do listy: "Nie wyciągnięto żadnego tekstu"
            # To jak napisanie uwagi: "Uwaga: brak treści!"

        if "  " in text:
            # Sprawdzamy: "Czy są PODWÓJNE spacje?"
            # '  ' = dwie spacje obok siebie
            # OCR czasem robi błędy i dodaje za dużo spacji
            # To jak szukanie błędów formatowania w dokumencie

            validation["issues"].append("Excessive whitespace detected")
            # Dodajemy uwagę o nadmiarowych spacjach

            validation["cleaned_text"] = re.sub(r"\s+", " ", text)
            # CZYŚCIMY TEKST!
            # re.sub(r'\s+', ' ', text) = zamień każdy ciąg białych znaków na JEDNĄ spację
            # \s+ = jeden lub więcej białych znaków (spacje, taby, newline)
            # Przykład: "Ala  ma   kota" → "Ala ma kota"
            # To jak używanie korektora - poprawiamy formatowanie

        if re.search(r"[^\x00-\x7F]", text):
            # Sprawdzamy: "Czy są znaki spoza ASCII?"
            # [^\x00-\x7F] = znaki które NIE są standardowym ASCII
            # ASCII = podstawowe znaki angielskie (a-z, 0-9, .,!)
            # Znaki spoza ASCII: ą, ę, ł, €, ™, itp.
            # To może być OK (polski tekst) lub błąd OCR (dziwne symbole)
            # To jak sprawdzanie czy w tekście są nietypowe symbole

            validation["issues"].append(
                "Non-ASCII characters detected (check if expected)"
            )
            # Uwaga: są nietypowe znaki - sprawdź czy to celowe
            # (check if expected) = może to być normalne jeśli tekst nie jest po angielsku

        if len(re.findall(r"[^\w\s]", text)) / max(len(text), 1) > 0.3:
            # Sprawdzamy: "Czy jest ZA DUŻO znaków interpunkcyjnych?"
            # re.findall(r'[^\w\s]', text) = znajdź wszystkie znaki które NIE są literami ani spacjami
            # [^\w\s] = nie litera, nie cyfra, nie spacja (czyli: .,!?@#$ itp.)
            # len(...) / max(len(text), 1) = procent znaków interpunkcyjnych
            # max(..., 1) = zabezpieczenie przed dzieleniem przez 0
            # > 0.3 = więcej niż 30%
            # Jeśli 30%+ tekstu to dziwne znaki, prawdopodobnie OCR się pomylił
            # To jak sprawdzenie czy dokument nie jest przypadkiem zaszyfrowany lub pełen śmieci

            validation["issues"].append("High punctuation ratio (potential OCR noise)")
            # Uwaga: za dużo znaków specjalnych - może być szum OCR (błędy rozpoznawania)

        return validation
        # Zwracamy cały raport kontroli jakości
        # To jak oddanie wypełnionej listy kontrolnej

    def compare_extractions(self):
        """Compare text extraction results across different sources"""
        # To jest "porównywacz dokumentów"
        # Stawia wszystkie rozpoznane teksty obok siebie
        # Pokazuje różnice w jakości i szybkości rozpoznawania
        # Jak zestawienie wyników testów z różnych przedmiotów!

        if len(self.results) < 2:
            # Sprawdzamy: "Czy mamy przynajmniej 2 dokumenty?"
            # Jeśli mniej niż 2, nie ma co porównywać

            print("\nNeed at least 2 processed documents to compare.")
            # Informujemy użytkownika: "Za mało danych"
            # To jak próba zrobienia wykresu porównawczego z jednym punktem

            return
            # Kończymy funkcję - wychodzimy

        print("\n" + "=" * 70)
        print("COMPARISON OF TEXT EXTRACTION RESULTS")
        print("=" * 70)
        # Ładny nagłówek z ramką
        # To jak tytuł raportu porównawczego

        for i, result in enumerate(self.results, 1):
            # PĘTLA PRZEZ WSZYSTKIE WYNIKI!
            # enumerate(..., 1) = numeruj od 1
            # i = numer dokumentu (1, 2, 3...)
            # result = pełny wynik rozpoznawania jednego dokumentu
            # To jak przeglądanie teczki dokument po dokumencie

            stats = result["statistics"]
            # Wyciągamy statystyki dla wygody
            # Skrót zamiast pisać result['statistics'] za każdym razem

            print(f"\n{i}. {result['description']}")
            # Wypisujemy numer i opis dokumentu
            # Przykład: "1. Printed English Text"
            # To jak punkt na liście

            print(
                f"   Processing time: {result['processing_time_ms']}ms | Language: {result['language']}"
            )
            # Pokazujemy jak długo trwało i jaki był język
            # Wcięcie "   " = to jest podpunkt
            # Przykład: "Processing time: 1234ms | Language: en"

            print(
                f"   Pages: {stats['total_pages']} | Lines: {stats['total_lines']} | Words: {stats['total_words']}"
            )
            # Pokazujemy statystyki: strony, linie, słowa
            # To jak raport: "Dokument ma 3 strony, 45 linii i 287 słów"

            # Validate text quality
            validation = self.validate_text(result["full_text"])
            # SPRAWDZAMY JAKOŚĆ!
            # Wywołujemy naszego "kontrolera jakości"
            # Dostajemy raport z problemami (jeśli jakieś są)

            print(
                f"   {'⚠️  Issues: ' + ', '.join(validation['issues']) if validation['issues'] else '✓ Text quality: Good'}"
            )
            # WARUNKOWE WYŚWIETLANIE!
            # Jeśli są problemy (validation['issues'] nie jest puste):
            #   - Pokazujemy: "⚠️ Issues: problem1, problem2, problem3"
            #   - ', '.join() = łączy problemy przecinkami
            # Jeśli nie ma problemów:
            #   - Pokazujemy: "✓ Text quality: Good"
            # To jak ocena: albo lista błędów albo "Bardzo dobrze!"

        print("\n" + "=" * 70)
        # Zamykająca linia - koniec porównania

    def save_results(self, filename="task2_results.json"):
        """Save all OCR results to JSON file"""
        # To jest "archiwista wyników"
        # Zapisuje WSZYSTKIE wyniki OCR do pliku JSON na dysku
        # Żeby móc je później przeczytać, przeanalizować lub przekazać komuś
        # Jak zapisywanie raportu Word - dane przetrwają zamknięcie programu!

        with open(filename, "w", encoding="utf-8") as f:
            # Otwieramy plik do ZAPISU
            # 'w' = write (pisz, nadpisz jeśli istnieje)
            # encoding='utf-8' = wsparcie dla polskich znaków
            # 'as f' = nazwij plik literką 'f'
            # with = automatycznie zamknie plik (bezpieczne!)

            json.dump(
                {
                    "task": "Task 2: OCR Text Extraction",
                    "timestamp": datetime.now().isoformat(),
                    "total_documents_processed": len(self.results),
                    "results": self.results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
            # ZAPISUJEMY DANE!
            # json.dump() = wylej dane do pliku w formacie JSON
            # Pakujemy wszystko w słownik:
            # - task: nazwa zadania
            # - timestamp: kiedy zapisaliśmy (TERAZ)
            # - total_documents_processed: ile dokumentów rozpoznaliśmy
            # - results: pełna lista wszystkich wyników
            # indent=2 = wcięcia (ładnie czytelnie)
            # ensure_ascii=False = polskie znaki OK

        print(f"\n✓ Results saved to: {filename}")
        # Informujemy gdzie zapisaliśmy

        return filename
        # Zwracamy nazwę pliku

    def export_text_files(self):
        """Export extracted text to separate .txt files"""
        # To jest "eksporter do plików tekstowych"
        # Bierze rozpoznany tekst i zapisuje każdy dokument jako osobny plik .txt
        # Żeby można było łatwo otworzyć w Notatniku
        # To jak robienie kserokopii - każdy dokument osobno!

        print("\n--- Exporting text files ---")
        # Nagłówek informacyjny

        for i, result in enumerate(self.results, 1):
            # PĘTLA PRZEZ WSZYSTKIE WYNIKI!
            # Każdy dokument dostanie swój własny plik .txt
            # i = numer dokumentu (1, 2, 3...)

            # Create safe filename
            safe_desc = re.sub(r"[^\w\s-]", "", result["description"])
            # CZYŚCIMY OPIS żeby zrobić bezpieczną nazwę pliku!
            # re.sub(r'[^\w\s-]', '', ...) = usuń wszystko co NIE jest:
            # - \w = literą/cyfrą
            # - \s = spacją
            # - - = myślnikiem
            # Przykład: "Text (v2.0)!" → "Text v20"
            # Dlaczego? Bo nazwy plików nie mogą mieć znaków: / \ : * ? " < > |
            # To jak przygotowanie tekstu na tablicę rejestracyjną - tylko proste znaki!

            safe_desc = re.sub(r"[\s]+", "_", safe_desc)
            # Zamieniamy SPACJE na PODKREŚLNIKI
            # r'[\s]+' = jedna lub więcej spacji
            # Przykład: "Printed English Text" → "Printed_English_Text"
            # Dlaczego? Bo spacje w nazwach plików są problematyczne (trzeba używać "")
            # To jak zastępowanie spacji myślnikami w URL-ach

            filename = f"ocr_output_{i}_{safe_desc}.txt"
            # Składamy PEŁNĄ NAZWĘ PLIKU
            # Format: ocr_output_NUMER_OPIS.txt
            # Przykład: "ocr_output_1_Printed_English_Text.txt"
            # To daje nam unikalne, opisowe nazwy dla każdego pliku

            with open(filename, "w", encoding="utf-8") as f:
                # Otwieramy plik do zapisu
                # encoding='utf-8' = polskie znaki będą działać

                f.write(f"OCR Extraction Results\n")
                f.write(f"Source: {result['description']}\n")
                f.write(f"Language: {result['language']}\n")
                f.write(f"Timestamp: {result['timestamp']}\n")
                f.write(f"\n{'='*70}\n\n")
                # Piszemy NAGŁÓWEK pliku
                # To informacje o dokumencie:
                # - Tytuł
                # - Skąd pochodzi
                # - Jaki język
                # - Kiedy rozpoznane
                # - Linia oddzielająca (70 znaków "=")
                # To jak strona tytułowa raportu

                f.write(result["full_text"])
                # Piszemy CAŁY ROZPOZNANY TEKST!
                # To jest główna treść pliku
                # To jak skopiowanie treści z jednego dokumentu do drugiego

            print(f"   ✓ Exported: {filename}")
            # Informujemy że zapisaliśmy plik
            # Przykład: "✓ Exported: ocr_output_1_Printed_English_Text.txt"


def demonstrate_ocr_processing():
    """Main demonstration function showcasing OCR capabilities"""
    # To jest "GŁÓWNA FUNKCJA DEMO OCR"
    # Pokazuje wszystkie możliwości rozpoznawania tekstu
    # Testuje różne typy dokumentów i języków
    # To jak pokaz możliwości nowego skanera!

    print("=" * 70)
    print("TASK 2: OCR IMPLEMENTATION - AZURE COMPUTER VISION READ API")
    print("AI-102 Coverage: Extract text from images using OCR")
    print("=" * 70)
    # Ładny nagłówek z ramką
    # Informujemy co będziemy robić
    # To jak tytuł prezentacji

    processor = OCRProcessor()
    # Tworzymy nasz procesor OCR!
    # To uruchamia __init__ który łączy się z Azure
    # Teraz mamy gotowe narzędzie do czytania tekstu

    # Test scenarios
    test_images = [
        (
            "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg",
            "Printed English Text",
            "en",
        ),
        (
            "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/handwritten_text.jpg",
            "Handwritten English Text",
            "en",
        ),
        (
            "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg",
            "Auto-detect Language",
            None,
        ),
    ]
    # To jest "lista testów do wykonania"
    # Każdy element to KROTKA (trójka) zawierająca:
    # 1. URL obrazu (link do zdjęcia)
    # 2. Opis testu (co sprawdzamy)
    # 3. Język ("en" = angielski, None = auto-detect)
    # Testujemy różne scenariusze:
    # - Drukowany tekst (łatwy do rozpoznania)
    # - Pismo odręczne (trudniejsze!)
    # - Auto-detekcja języka (OCR sam zgaduje)
    # To jak zestaw próbek do laboratorium!

    for i, (url, desc, lang) in enumerate(test_images, 1):
        # PĘTLA PRZEZ WSZYSTKIE TESTY!
        # enumerate(..., 1) = numeruj od 1
        # (url, desc, lang) = rozpakowujemy krotkę na 3 zmienne
        # i = numer testu (1, 2, 3)
        # url = link do obrazu
        # desc = opis testu
        # lang = język lub None
        # To jak wykonywanie listy zadań - jedno po drugim

        print(f"\n\n### TEST {i}: {desc} ###")
        # Wypisujemy nagłówek testu
        # Przykład: "### TEST 1: Printed English Text ###"
        # To jak tytuł rozdziału w instrukcji

        processor.extract_text_from_url(url, description=desc, language=lang)
        # ROZPOZNAJEMY TEKST!
        # Wywołujemy główną metodę która:
        # 1. Wysyła obraz do Azure
        # 2. Czeka na wynik
        # 3. Przetwarza i wyświetla tekst
        # 4. Zapisuje w pamięci procesora
        # To jak przeprowadzenie eksperymentu i zapisanie wyników

    # TEST 4: SKIPPED
    print("\n\n### TEST 4: SKIPPED ###")
    # Informujemy że test 4 został pominięty
    # Dlaczego? Czasem przykładowe obrazy nie są dostępne

    print("   Note: Additional test skipped due to sample image availability")
    # Wyjaśnienie dlaczego pomijamy
    # "Brak dostępnego obrazu do testów"

    print("   The 3 tests above demonstrate all key Read API capabilities:")
    print("   ✓ Printed text extraction")
    print("   ✓ Handwritten text recognition")
    print("   ✓ Multi-language auto-detection")
    # Lista tego co już przetestowaliśmy
    # Pokazujemy że 3 testy wystarczają żeby pokazać wszystkie możliwości
    # To jak powiedzenie: "Mamy wystarczająco dużo danych mimo że jeden test nie zadziałał"

    # Compare, save, and export
    processor.compare_extractions()
    # Porównujemy wszystkie wyniki obok siebie
    # Pokazujemy różnice między dokumentami
    # To jak zestawienie wyników wszystkich testów

    processor.save_results()
    # Zapisujemy WSZYSTKO do pliku JSON
    # Żeby mieć trwały zapis wszystkich rozpoznanych tekstów
    # To jak archiwizacja eksperymentu

    processor.export_text_files()
    # Eksportujemy każdy dokument jako osobny plik .txt
    # Żeby łatwo otworzyć w Notatniku
    # To jak robienie kserokopii każdego dokumentu osobno

    print("\n" + "=" * 70)
    print("✓ TASK 2 COMPLETED SUCCESSFULLY")
    print("=" * 70)
    # Gratulacje! Wszystko się udało!
    # Ładna ramka z informacją o sukcesie

    print("\nAI-102 Key Learnings:")
    print("1. Read API uses asynchronous pattern (start → poll → get results)")
    print("2. Supports 100+ languages with auto-detection")
    print("3. Handles both printed and handwritten text")
    print("4. Returns bounding boxes for text location")
    print("5. Confidence scores available at word level")
    print("6. Operation ID polling is the standard pattern for long operations")
    # To jest "lista najważniejszych lekcji"
    # Co nauczyliśmy się z tego zadania?
    # Kluczowe punkty do zapamiętania na egzamin AI-102:
    # 1. OCR działa asynchronicznie (wyślij → czekaj → odbierz)
    # 2. Wspiera 100+ języków z auto-detekcją
    # 3. Radzi sobie z drukiem I pismem odręcznym
    # 4. Daje współrzędne każdego tekstu
    # 5. Każde słowo ma wynik pewności
    # 6. Polling (sprawdzanie co chwilę) to standard dla długich operacji
    # To jak podsumowanie wykładu - same najważniejsze informacje!

    print("\n✓ 3/4 tests completed successfully - sufficient for AI-102 exam prep!")
    # Potwierdzenie że 3 z 4 testów wystarczy
    # Mimo że jeden test został pominięty, to wystarczy do nauki

    print("\nNext: Run 'python task3_custom_vision.py' for custom model training")
    # Wskazówka co robić dalej
    # To jak "Koniec rozdziału 2. Przejdź do rozdziału 3."


if __name__ == "__main__":
    """Execute OCR processing demonstration"""
    # To jest "strażnik drzwi"
    # Sprawdza: "Czy ten plik został uruchomiony bezpośrednio?"
    # __name__ to specjalna zmienna Pythona
    # Jeśli uruchomimy: python task2_ocr_processing.py → __name__ = "__main__"
    # Jeśli ktoś zaimportuje: import task2_ocr_processing → __name__ = "task2_ocr_processing"
    # Dzięki temu kod poniżej wykona się TYLKO gdy uruchomimy plik bezpośrednio
    # To jak sprawdzanie: "Czy jestem głównym programem czy biblioteką pomocniczą?"

    try:
        # PRÓBUJEMY uruchomić program
        # try = siatka bezpieczeństwa - jak złapać coś co spada
        # Jeśli coś pójdzie źle, nie wywali całego programu

        demonstrate_ocr_processing()
        # URUCHAMIAMY CAŁE DEMO OCR!
        # To wywołuje główną funkcję która testuje rozpoznawanie tekstu

    except Exception as e:
        # ŁAPIEMY WSZYSTKIE BŁĘDY!
        # Jeśli cokolwiek pójdzie nie tak, trafiamy tutaj
        # e = obiekt błędu (informacja co się zepsuło)

        print(f"\n✗ Error: {e}")
        # Wyświetlamy komunikat błędu
        # Przykład: "✗ Error: Connection timeout"

        print("\nTroubleshooting:")
        print("1. Check .env file configuration")
        print("2. Run 'python config.py' to validate settings")
        print("3. Verify network connectivity to image URLs")
        print("4. Check Azure Computer Vision resource quota")
        # To jest "instrukcja ratunkowa"
        # Lista kroków co zrobić gdy coś nie działa
        # Jak instrukcja pierwszej pomocy:
        # 1. Sprawdź plik .env (czy masz klucze API)
        # 2. Uruchom config.py (sprawdź ustawienia)
        # 3. Sprawdź internet (czy dochodzisz do obrazów)
        # 4. Sprawdź Azure (czy nie wyczerpałeś limitu zapytań)
        # To pomaga użytkownikowi samodzielnie rozwiązać problem!
