from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, wait_for_sqlserver, r
from . import crud, models, database

app = FastAPI(title="FastAPI + SQL Server + Redis Example")

# Utworzenie tabel w bazie
wait_for_sqlserver()
models.Base.metadata.create_all(bind=database.engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpointy
@app.get("/")
def root():
    return {"message": "Hello FastAPI + SQL Server + Redis"}


@app.get("/clients")
def read_clients(db: Session = Depends(get_db)):
    # Próba pobrania z Redis
    cache_key = "clients"
    cached = r.get(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    clients = crud.get_clients(db)
    r.setex(cache_key, 60, str([{"id": c.id, "name": c.name, "email": c.email} for c in clients]))
    return {"source": "db", "data": [{"id": c.id, "name": c.name, "email": c.email} for c in clients]}


@app.get("/clients/{client_id}/orders")
def read_client_orders(client_id: int, db: Session = Depends(get_db)):
    cache_key = f"client_orders:{client_id}"
    cached = r.get(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    orders = crud.get_client_orders(db, client_id)
    r.setex(cache_key, 60, str([{"id": o.id, "client_id": o.client_id, "amount": o.amount} for o in orders]))
    return {"source": "db", "data": [{"id": o.id, "client_id": o.client_id, "amount": o.amount} for o in orders]}
