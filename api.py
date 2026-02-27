# Pierwsze API

from flask import Flask, jsonify, request

# Tworzenie aplikacji Flask
app = Flask(__name__)

# Prosta baza danych w pamięci (lista słowników)
produkty = [
    {"id": 1, "nazwa": "Chleb", "cena": 4.50},
    {"id": 2, "nazwa": "Mleko", "cena": 3.20},
    {"id": 3, "nazwa": "Masło", "cena": 7.80},
]


# --- ENDPOINT GET – pobierz wszystkie produkty ---
@app.route("/produkty", methods=["GET"])
def pobierz_produkty():
    return jsonify(produkty)


# --- ENDPOINT GET – pobierz jeden produkt ---
@app.route("/produkty/<int:id>", methods=["GET"])
def pobierz_produkt(id):
    produkt = next((p for p in produkty if p["id"] == id), None)
    if produkt is None:
        return jsonify({"blad": "Produkt nie istnieje"}), 404
    return jsonify(produkt)


# --- ENDPOINT POST – dodaj nowy produkt ---
@app.route("/produkty", methods=["POST"])
def dodaj_produkt():
    dane = request.get_json()
    nowy = {
        "id": len(produkty) + 1,
        "nazwa": dane["nazwa"],
        "cena": dane["cena"]
    }
    produkty.append(nowy)
    return jsonify(nowy), 201


# --- ENDPOINT PUT – zaktualizuj produkt ---
@app.route("/produkty/<int:id>", methods=["PUT"])
def aktualizuj_produkt(id):
    produkt = next((p for p in produkty if p["id"] == id), None)
    if produkt is None:
        return jsonify({"blad": "Produkt nie istnieje"}), 404
    dane = request.get_json()
    produkt["nazwa"] = dane.get("nazwa", produkt["nazwa"])
    produkt["cena"] = dane.get("cena", produkt["cena"])
    return jsonify(produkt)


# --- ENDPOINT DELETE – usuń produkt ---
@app.route("/produkty/<int:id>", methods=["DELETE"])
def usun_produkt(id):
    global produkty
    produkt = next((p for p in produkty if p["id"] == id), None)
    if produkt is None:
        return jsonify({"blad": "Produkt nie istnieje"}), 404
    produkty = [p for p in produkty if p["id"] != id]
    return jsonify({"komunikat": f"Produkt {id} usunięty"}), 200


if __name__ == "__main__":
    app.run(debug=True)



