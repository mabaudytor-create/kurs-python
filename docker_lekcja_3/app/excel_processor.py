# app/excel_processor.py

import pandas as pd
from io import BytesIO
from sqlalchemy.engine import Engine
from fastapi import HTTPException
from typing import List, Dict, Optional


def process_and_save_excel(
        excel_data_buffer: BytesIO,
        sql_engine: Engine,
        table_name: str,
        decimal_separator: str = '.',  # Domyślna kropka
        numeric_columns: Optional[List[str]] = None,
        column_rename_map: Optional[Dict[str, str]] = None
) -> int:
    """
    Wczytuje dane z bufora pliku Excela, przetwarza je i zapisuje do określonej tabeli w SQL Serverze.

    Args:
        excel_data_buffer (BytesIO): Bufor danych pliku Excela.
        sql_engine (Engine): Obiekt silnika SQLAlchemy do połączenia z bazą danych.
        table_name (str): Nazwa tabeli w SQL Serverze, do której mają zostać zapisane dane.
        decimal_separator (str): Separator dziesiętny używany w pliku Excela (domyślnie '.').
        numeric_columns (Optional[List[str]]): Lista nazw kolumn, które powinny być liczbami.
                                               Wartości nienumeryczne zostaną skonwertowane na 0.
        column_rename_map (Optional[Dict[str, str]]): Słownik mapujący nazwy kolumn z Excela
                                                       na nazwy kolumn w tabeli SQL (np. {'StaryNazwa': 'NowaNazwa'}).

    Returns:
        int: Liczba wczytanych rekordów.

    Raises:
        HTTPException: W przypadku błędu podczas przetwarzania lub zapisu danych.
    """
    try:
        # Wczytanie danych z Excela za pomocą pandas
        # Używamy parametru 'decimal' do określenia separatora dziesiętnego
        # Wartość 'engine=openpyxl' jest domyślna dla.xlsx, ale można ją jawnie podać,
        # jeśli masz problemy z odczytem niektórych plików
        df = pd.read_excel(excel_data_buffer, decimal=decimal_separator)

        # 1. Zmiana nazw kolumn, jeśli zdefiniowano mapowanie
        if column_rename_map:
            # Użyj errors='ignore' aby uniknąć błędów, jeśli kolumna do zmiany nie istnieje
            df.rename(columns=column_rename_map, inplace=True, errors='ignore')

        # 2. Konwersja kolumn numerycznych na odpowiedni typ (float/decimal)
        if numeric_columns:
            for col_name in numeric_columns:
                if col_name in df.columns:
                    # Zamieniamy spacje (separatory tysięcy) jeśli występują i potem konwertujemy
                    df[col_name] = df[col_name].astype(str).str.replace(' ', '', regex=False)
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')  # 'coerce' zamieni błędy na NaN
                    df[col_name] = df[col_name].fillna(0)  # Zamień NaN na 0 (lub inną wartość)
                else:
                    print(
                        f"Ostrzeżenie (excel_processor): Kolumna numeryczna '{col_name}' nie została znaleziona w pliku Excela.")

        # Tutaj można dodać inne ogólne walidacje/transformacje danych
        # np. usunięcie pustych wierszy, walidacja formatu dat itp.

        # Zapisanie danych do tabeli w SQL Serverze
        # if_exists='replace' dla testów, w produkcji rozważ 'append' lub inną logikę
        with sql_engine.connect() as conn:
            df.to_sql(table_name, con=conn, if_exists='replace', index=False)
            conn.commit()

        return len(df)

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Plik Excela jest pusty lub zawiera tylko nagłówki.")
    except Exception as e:
        # Wypisanie szczegółowego błędu do logów kontenera
        print(f"Błąd w excel_processor.py: {e}")
        raise HTTPException(status_code=500, detail=f"Wystąpił błąd podczas przetwarzania pliku: {str(e)}")
