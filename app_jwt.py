from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)

# Klucz szyfrowania tokenów – w prawdziwej aplikacji trzymaj go w .env!
app.config["JWT_SECRET_KEY"] = "super-tajny-klucz-2026"

jwt = JWTManager(app)

# Prosta baza użytkowników
uzytkownicy = {
    "mirek": "haslo123",
    "anna": "haslo456"
}


# --- LOGOWANIE – zwraca token JWT ---
@app.route("/login", methods=["POST"])
def login():
    dane = request.get_json()
    login = dane.get("login")
    haslo = dane.get("haslo")

    if login not in uzytkownicy or uzytkownicy[login] != haslo:
        return jsonify({"blad": "Nieprawidłowy login lub hasło"}), 401

    # Tworzenie tokenu JWT
    token = create_access_token(identity=login)
    return jsonify({"token": token})


# --- ENDPOINT CHRONIONY – wymaga tokenu ---
@app.route("/profil", methods=["GET"])
@jwt_required()
def profil():
    aktualny_uzytkownik = get_jwt_identity()
    return jsonify({
        "uzytkownik": aktualny_uzytkownik,
        "wiadomosc": f"Witaj {aktualny_uzytkownik}! To jest chroniony endpoint."
    })


# --- ENDPOINT PUBLICZNY – nie wymaga tokenu ---
@app.route("/publiczny", methods=["GET"])
def publiczny():
    return jsonify({"wiadomosc": "Ten endpoint jest dostępny dla wszystkich!"})


if __name__ == "__main__":
    app.run(debug=True)
# Testowanie JWT w test_jwt.py:python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Logowanie – pobieramy token
odpowiedz = requests.post(f"{BASE_URL}/login", json={
    "login": "mirek",
    "haslo": "haslo123"
})
token = odpowiedz.json()["token"]
print("Token:", token[:50], "...")

# Endpoint publiczny – bez tokenu
odpowiedz = requests.get(f"{BASE_URL}/publiczny")
print("Publiczny:", odpowiedz.json())

# Endpoint chroniony – bez tokenu (błąd!)
odpowiedz = requests.get(f"{BASE_URL}/profil")
print("Bez tokenu:", odpowiedz.status_code)  # 401

# Endpoint chroniony – z tokenem (działa!)
headers = {"Authorization": f"Bearer {token}"}
odpowiedz = requests.get(f"{BASE_URL}/profil", headers=headers)
print("Z tokenem:", odpowiedz.json())
