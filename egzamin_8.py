# Stwórz API dla systemu zarządzania zadaniami
# (TODO list) z endpointami GET /zadania, POST /zadania, PUT /zadania/<id>,
#  DELETE /zadania/<id>. Użyj SQLAlchemy do przechowywania danych.

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from typing import List, Optional

Base = declarative_base()


class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True, index=True)
    tytul = Column(String, nullable=False)
    opis = Column(String, nullable=True)
    status = Column(String, default="oczekuje")


class ZadanieCreate(BaseModel):
    tytul: str
    opis: Optional[str] = None
    status: Optional[str] = "oczekuje"


class ZadanieResponse(BaseModel):
    id: int
    tytul: str
    opis: Optional[str] = None
    status: str

    class Config:
        orm_mode = True


def get_db():
    raise RuntimeError("Dependency get_db musi być nadpisane.")


app = FastAPI()


# --- KLUCZOWE: automatyczne tworzenie tabel dla aktualnego engine ---
def ensure_tables(db: Session):
    engine = db.get_bind()
    Base.metadata.create_all(bind=engine)


@app.post("/zadania", response_model=ZadanieResponse)
def create_zadanie(zadanie: ZadanieCreate, db: Session = Depends(get_db)):
    ensure_tables(db)

    db_zadanie = Zadanie(**zadanie.dict())
    db.add(db_zadanie)
    db.commit()
    db.refresh(db_zadanie)
    return db_zadanie


@app.get("/zadania", response_model=List[ZadanieResponse])
def read_zadania(db: Session = Depends(get_db)):
    ensure_tables(db)
    return db.query(Zadanie).all()


@app.put("/zadania/{zadanie_id}", response_model=ZadanieResponse)
def update_zadanie(zadanie_id: int, zadanie: ZadanieCreate, db: Session = Depends(get_db)):
    ensure_tables(db)

    db_zadanie = db.query(Zadanie).filter(Zadanie.id == zadanie_id).first()
    if not db_zadanie:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")

    for key, value in zadanie.dict(exclude_unset=True).items():
        setattr(db_zadanie, key, value)

    db.commit()
    db.refresh(db_zadanie)
    return db_zadanie


@app.delete("/zadania/{zadanie_id}")
def delete_zadanie(zadanie_id: int, db: Session = Depends(get_db)):
    ensure_tables(db)

    db_zadanie = db.query(Zadanie).filter(Zadanie.id == zadanie_id).first()
    if not db_zadanie:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")

    db.delete(db_zadanie)
    db.commit()

    return {"komunikat": "Zadanie usunięte"}

