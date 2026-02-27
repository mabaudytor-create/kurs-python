from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# =========================================================
# KONFIGURACJA JWT
# =========================================================

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================================================
# KONFIGURACJA BAZY (produkcyjna)
# =========================================================

DATABASE_URL = "sqlite:///./zadania.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =========================================================
# MODEL ORM
# =========================================================

class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True, index=True)
    tytul = Column(String, nullable=False)
    opis = Column(String, nullable=True)
    status = Column(String, default="oczekuje")


# =========================================================
# UŻYTKOWNIK (prosty model demonstracyjny)
# =========================================================

fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
    }
}


# =========================================================
# MODELE Pydantic
# =========================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class ZadanieCreate(BaseModel):
    tytul: str
    opis: Optional[str] = None
    status: Optional[str] = "oczekuje"


class ZadanieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tytul: str
    opis: Optional[str] = None
    status: str


# =========================================================
# FUNKCJE POMOCNICZE JWT
# =========================================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nieprawidłowe dane uwierzytelniające",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = fake_user_db.get(username)
    if user is None:
        raise credentials_exception
    return user


# =========================================================
# DEPENDENCY DB
# =========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# APLIKACJA
# =========================================================

app = FastAPI()

Base.metadata.create_all(bind=engine)

# =========================================================
# ENDPOINT LOGOWANIA
# =========================================================

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Błędny login lub hasło",
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# =========================================================
# ENDPOINTY CRUD
# =========================================================

# 🔓 PUBLICZNY
@app.get("/zadania", response_model=List[ZadanieResponse])
def read_zadania(db: Session = Depends(get_db)):
    return db.query(Zadanie).all()


# 🔐 WYMAGA JWT
@app.post("/zadania", response_model=ZadanieResponse)
def create_zadanie(
    zadanie: ZadanieCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_zadanie = Zadanie(**zadanie.model_dump())
    db.add(db_zadanie)
    db.commit()
    db.refresh(db_zadanie)
    return db_zadanie


# 🔐 WYMAGA JWT
@app.put("/zadania/{zadanie_id}", response_model=ZadanieResponse)
def update_zadanie(
    zadanie_id: int,
    zadanie: ZadanieCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_zadanie = db.query(Zadanie).filter(Zadanie.id == zadanie_id).first()
    if not db_zadanie:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")

    for key, value in zadanie.model_dump(exclude_unset=True).items():
        setattr(db_zadanie, key, value)

    db.commit()
    db.refresh(db_zadanie)
    return db_zadanie


# 🔐 WYMAGA JWT
@app.delete("/zadania/{zadanie_id}")
def delete_zadanie(
    zadanie_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_zadanie = db.query(Zadanie).filter(Zadanie.id == zadanie_id).first()
    if not db_zadanie:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")

    db.delete(db_zadanie)
    db.commit()

    return {"komunikat": "Zadanie usunięte"}
