# 📁 File: backend.py
import random
import numpy as np
from pytrends.request import TrendReq

def fetch_trends(keyword):
    try:
        pytrends = TrendReq(hl='en-US', tz=330)
        pytrends.build_payload([keyword], timeframe='today 12-m')
        df = pytrends.interest_over_time()
        if df.empty or 'isPartial' not in df.columns:
            return None
        trend_values = df[keyword].values.tolist()
        months = df.index.strftime('%b %Y').tolist()
        return trend_values, months
    except Exception:
        return None

def analyze_viability(product_name, description, cost_price, selling_price):
    profit = selling_price - cost_price
    profit_margin = profit / cost_price * 100 if cost_price > 0 else 0

    quality_score = min(100, (cost_price / 10) * random.uniform(0.8, 1.2))
    competition_score = random.choice([20, 40, 60, 80])
    sustainability_months = round((profit * (100 - competition_score)) / 10)

    trends = fetch_trends(product_name)
    trend_score = None
    trend_values = []
    trend_months = []
    if trends:
        trend_values, trend_months = trends
        trend_score = int(np.mean(trend_values))

    return {
        "profit_margin": round(profit_margin, 2),
        "quality_score": round(quality_score, 2),
        "competition_score": competition_score,
        "sustainability_months": sustainability_months,
        "recommendation": "Go Ahead 🚀" if profit_margin > 20 and quality_score > 50 else "High Risk ⚠️",
        "trend_score": trend_score,
        "trend_values": trend_values,
        "trend_months": trend_months
    }
