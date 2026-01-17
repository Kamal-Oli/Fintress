from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def safe_sum(df, col):
    return df[col].sum() if col in df.columns else 0

def calculate_metrics(df):
    def calculate_metrics(df):
    current_assets = safe_sum(df, "Current Assets")
    inventory = safe_sum(df, "Inventory")
    current_liabilities = safe_sum(df, "Current Liabilities")
    total_liabilities = safe_sum(df, "Total Liabilities")
    equity = safe_sum(df, "Equity")
    total_assets = safe_sum(df, "Total Assets")
    revenue = safe_sum(df, "Revenue")
    net_profit = safe_sum(df, "Net Profit")

    current_ratio = ...
    quick_ratio = ...
    debt_equity = ...
    roa = ...

    score = ...
    current_assets = safe_sum(df, "Current Assets")
    inventory = safe_sum(df, "Inventory")
    current_liabilities = safe_sum(df, "Current Liabilities")
    total_liabilities = safe_sum(df, "Total Liabilities")
    equity = safe_sum(df, "Equity")
    total_assets = safe_sum(df, "Total Assets")
    revenue = safe_sum(df, "Revenue")
    net_profit = safe_sum(df, "Net Profit")
    def altman_z_score(df):
    wc = safe_sum(df, "Current Assets") - safe_sum(df, "Current Liabilities")
    ta = safe_sum(df, "Total Assets")
    tl = safe_sum(df, "Total Liabilities")
    equity = safe_sum(df, "Equity")
    retained_earnings = safe_sum(df, "Retained Earnings")
    ebit = safe_sum(df, "EBIT")

    if ta == 0 or tl == 0:
        return 0, "Insufficient data"

    z = (
        6.56 * (wc / ta)
        + 3.26 * (retained_earnings / ta)
        + 6.72 * (ebit / ta)
        + 1.05 * (equity / tl)
    )

    if z < 1.1:
        status = "Distress Zone"
    elif z < 2.6:
        status = "Grey Zone"
    else:
        status = "Safe Zone"

    return round(z, 2), status

    current_ratio = current_assets / current_liabilities if current_liabilities else 0
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else 0
    debt_equity = total_liabilities / equity if equity else 0
    roa = net_profit / total_assets if total_assets else 0

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
    error = None

    if request.method == "POST":
        try:
            file = request.files.get("file")
            if not file:
                raise ValueError("No file uploaded")

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            if file.filename.endswith(".csv"):
                df = pd.read_csv(path)
            elif file.filename.endswith(".xlsx"):
                df = pd.read_excel(path)
            else:
                raise ValueError("Unsupported file format")

            metrics = calculate_metrics(df)

        except Exception as e:
            error = str(e)

    return render_template("index.html", metrics=metrics, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
