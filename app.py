from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

EXCEL_FILE = "products.xlsx"
JSON_FILE = "products.json"

def convert_excel_to_json():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Excel file '{EXCEL_FILE}' not found.")
        return
    df = pd.read_excel(EXCEL_FILE)
    products = df.to_dict(orient="records")
    with open(JSON_FILE, "w") as f:
        json.dump(products, f, indent=4)
    print("✅ Converted Excel to JSON.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products")
def get_products():
    if not os.path.exists(JSON_FILE):
        return jsonify({"error": "products.json not found"}), 404
    with open(JSON_FILE, "r") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    convert_excel_to_json()
    app.run(debug=True)
