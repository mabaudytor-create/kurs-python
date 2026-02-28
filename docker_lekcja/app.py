from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "wiadomosc": "Witaj z kontenera Docker!",
        "status": "dziala"
    })


@app.route("/zdrowie")
def zdrowie():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
