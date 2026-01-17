from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_metrics(df):
    current_assets = df["Current Assets"].sum()
    inventory = df["Inventory"].sum() if "Inventory" in df.columns else 0
    current_liabilities = df["Current Liabilities"].sum()
    total_liabilities = df["Total Liabilities"].sum()
    equity = df["Equity"].sum()
    total_assets = df["Total Assets"].sum()
    revenue = df["Revenue"].sum()
    net_profit = df["Net Profit"].sum()

    current_ratio = current_assets / current_liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities
    debt_equity = total_liabilities / equity
    roa = net_profit / total_assets

    score = 0
    if current_ratio < 1:
        score += 2
    if quick_ratio < 0.8:
        score += 2
    if debt_equity > 2:
        score += 2
    if roa < 0.05:
        score += 1

    if score >= 5:
        health = "RED – High Financial Stress"
    elif score >= 3:
        health = "YELLOW – Moderate Risk"
    else:
        health = "GREEN – Healthy"

    return {
        "Current Ratio": round(current_ratio, 2),
        "Quick Ratio": round(quick_ratio, 2),
        "Debt to Equity": round(debt_equity, 2),
        "ROA (%)": round(roa * 100, 2),
        "Health Status": health
    }

@app.route("/", methods=["GET", "POST"])
def index():
    metrics = None

    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        if file.filename.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        metrics = calculate_metrics(df)

    return render_template("index.html", metrics=metrics)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
