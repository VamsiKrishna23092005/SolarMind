FROM python:3.12-slim

# Setup primary app directory
WORKDIR /app

# Ensure native compiling for sqlite/chroma if required
RUN apt-get update && apt-get install -y build-essential sqlite3 libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-create ChromaDB local directory structure
RUN mkdir -p chroma_db

COPY . .

# Ports mapping (FastAPI and Streamlit)
EXPOSE 8501 8000

# Defaults to start UI stream graph dashboard
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
