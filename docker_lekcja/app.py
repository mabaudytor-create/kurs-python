from fastapi import FastAPI

app = FastAPI(title="FastAPI Example")

# Przykładowy endpoint główny
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Przykładowy endpoint użytkownika
@app.get("/user/{user_id}")
def read_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }
