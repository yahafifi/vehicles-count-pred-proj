# ---- Base image ----
FROM python:3.11-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- System deps (optional but useful for some ML libs) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# ---- Install python deps first (better caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose port ----
EXPOSE 5000

# ---- Run with gunicorn (recommended for Docker) ----
# IMPORTANT: this assumes your Flask instance is named "app" inside app/app.py
# i.e. in app/app.py you have: app = Flask(__name__)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app.app:app"]
