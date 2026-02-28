FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        make \
        curl \
        gnupg \
        unixodbc-dev \
        libodbc1 && \
    rm -rf /var/lib/apt/lists/*

# Instalacja sterownika ODBC MS
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
