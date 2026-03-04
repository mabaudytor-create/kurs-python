import pyodbc

# Połączenie – zmień tylko NAZWA_BAZY jeśli chcesz
BAZA = "master"          # możesz zmienić na nazwę swojej bazy, np. "MojaFirma"

polaczenie = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=AUDYTOR\\SQLEXPRESS2022;"  # kropka + \\ + SQLEXPRESS = lokalny serwer Express
    f"DATABASE={BAZA};"
    "Trusted_Connection=yes;"            # używa Twojego konta Windows
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"        # na testy lokalne – pomija ostrzeżenia o certyfikacie
)

try:
    conn = pyodbc.connect(polaczenie)
    print("Połączenie działa! Super! 🎉")

    # Mały test – pokaże wersję SQL Servera
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    wersja = cursor.fetchone()[0]
    print("Twoja wersja SQL Server:")
    print(wersja)

    conn.close()
except Exception as e:
    print("Coś poszło nie tak 😔")
    print("Błąd:", e)
