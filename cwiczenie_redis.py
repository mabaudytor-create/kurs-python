from flask import Flask, jsonify
import redis
import json
import time

app = Flask(__name__)

# ==============================
# KONFIGURACJA REDIS
# ==============================
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True  # zwracanie stringów zamiast bajtów
)

CACHE_TTL = 60  # czas życia cache w sekundach

# ==============================
# ENDPOINT API
# ==============================
@app.route("/user/<int:user_id>")
def get_user(user_id):
    cache_key = f"user:{user_id}"

    # 1️⃣ Sprawdzenie Redis
    cached = redis_client.get(cache_key)
    if cached:
        print("Zwrócono dane z Redis")
        return jsonify(json.loads(cached))

    # 2️⃣ Symulacja pobrania z bazy
    print("Generowanie danych 'z bazy'")
    user = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "timestamp": time.time()
    }

    # 3️⃣ Zapis do Redis z TTL
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(user))
    print("Dane zapisane do Redis")

    return jsonify(user)

# ==============================
# URUCHOMIENIE APLIKACJI
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
