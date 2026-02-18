from flask import Flask, render_template, request, redirect, flash
import requests
import os

# Load from .env only if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
app.secret_key = "secret"

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

        clean_data = {k: v for k, v in data.items() if v}

        payload = {
            "action": action,
            "data": clean_data
        }

        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)


application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
