from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja bazy danych SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sklep.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- MODEL – definicja tabeli w bazie danych ---
class Produkt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    cena = db.Column(db.Float, nullable=False)

    def do_slownika(self):
        """Konwertuje obiekt na słownik (do JSON)."""
        return {
            "id": self.id,
            "nazwa": self.nazwa,
            "cena": self.cena
        }


# --- ENDPOINTY CRUD ---
@app.route("/produkty", methods=["GET"])
def pobierz_produkty():
    produkty = Produkt.query.all()
    return jsonify([p.do_slownika() for p in produkty])


@app.route("/produkty/<int:id>", methods=["GET"])
def pobierz_produkt(id):
    produkt = Produkt.query.get_or_404(id)
    return jsonify(produkt.do_slownika())


@app.route("/produkty", methods=["POST"])
def dodaj_produkt():
    dane = request.get_json()
    nowy = Produkt(nazwa=dane["nazwa"], cena=dane["cena"])
    db.session.add(nowy)
    db.session.commit()
    return jsonify(nowy.do_slownika()), 201


@app.route("/produkty/<int:id>", methods=["PUT"])
def aktualizuj_produkt(id):
    produkt = Produkt.query.get_or_404(id)
    dane = request.get_json()
    produkt.nazwa = dane.get("nazwa", produkt.nazwa)
    produkt.cena = dane.get("cena", produkt.cena)
    db.session.commit()
    return jsonify(produkt.do_slownika())


@app.route("/produkty/<int:id>", methods=["DELETE"])
def usun_produkt(id):
    produkt = Produkt.query.get_or_404(id)
    db.session.delete(produkt)
    db.session.commit()
    return jsonify({"komunikat": f"Produkt {id} usunięty"})


# Tworzenie tabel przy starcie
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
