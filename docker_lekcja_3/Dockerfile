FROM python:3.13-slim-bookworm

WORKDIR /app

# Instalacja zależności + aktualny (2025/2026) sposób dodawania repo Microsoft
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list | \
       tee /etc/apt/sources.list.d/mssql-release.list \
    && echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Wymagane pakiety Python (bez cache)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy kod aplikacji
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


