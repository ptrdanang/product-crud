from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

# Setup Logging agar kita bisa lihat detail error di terminal/log pod EKS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load from .env jika running lokal
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Pastikan variable ini sudah di-set di GitHub Secrets & Environment EKS
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")
        data = {
            "id": request.form.get("id"),
            "name": request.form.get("name"),
            "stok": request.form.get("stok"),
            "harga": request.form.get("harga")
        }

        # Bersihkan data (hapus yang kosong)
        clean_data = {k: v for k, v in data.items() if v}

        payload = {
            "action": action,
            "data": clean_data
        }

        # Header WAJIB untuk AWS API Gateway
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        logger.info(f"Mengirim request ke: {API_URL}")

        try:
            # Melakukan request ke API Gateway
            response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
            
            # Jika AWS mengembalikan status sukses (200)
            if response.status_code == 200:
                result = response.json()
            else:
                # Jika 403 atau 401, pesan "Missing Authentication Token" akan tertangkap di sini
                error = f"API Error ({response.status_code}): {response.text}"
                logger.error(error)

        except requests.exceptions.RequestException as e:
            error = f"Gagal terhubung ke API: {str(e)}"
            logger.error(error)

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)