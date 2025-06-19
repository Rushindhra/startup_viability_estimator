# 📁 File: app.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from backend import analyze_viability, fetch_trends

st.set_page_config(page_title="Startup/Product Viability Estimator", layout="centered")
st.title("🚀 Startup Viability Estimator")
st.markdown("Analyze your product idea based on real-world trends and financial viability.")

with st.form("input_form"):
    product_name = st.text_input("🛍️ Product Name")
    description = st.text_area("📝 Description")
    cost_price = st.number_input("🏷️ Cost to Make (₹)", min_value=1)
    selling_price = st.number_input("💰 Selling Price (₹)", min_value=1)
    submitted = st.form_submit_button("🔍 Analyze Product")

if submitted:
    result = analyze_viability(product_name, description, cost_price, selling_price)

    st.subheader("📊 Analysis Summary")
    st.metric("Profit Margin (%)", result["profit_margin"])
    st.metric("Quality Score", result["quality_score"])
    st.metric("Market Competition (lower is better)", result["competition_score"])
    st.metric("Sustainability (Months)", result["sustainability_months"])
    st.success(f"Recommendation: {result['recommendation']}")

    if result["trend_score"] is not None:
        st.metric("📈 Google Trend Score (0-100)", result["trend_score"])
        st.subheader("📈 Trend Over Time")
        trend_df = pd.DataFrame({"Month": result["trend_months"], "Trend Score": result["trend_values"]})
        st.line_chart(trend_df.set_index("Month"))
    else:
        st.warning("⚠️ Google Trends data not found for this keyword.")

    st.subheader("📉 Profit Forecast Graph")
    months = list(range(1, result["sustainability_months"] + 1))
    revenue = [selling_price * i for i in months]
    cost = [cost_price * i for i in months]

    fig, ax = plt.subplots()
    ax.plot(months, revenue, label="Revenue", color="green")
    ax.plot(months, cost, label="Cost", color="red")
    ax.fill_between(months, cost, revenue, where=(pd.Series(revenue) > pd.Series(cost)), 
                    color='lightgreen', alpha=0.4)
    ax.set_xlabel("Months")
    ax.set_ylabel("₹")
    ax.set_title("Profit Forecast Over Time")
    ax.legend()
    st.pyplot(fig)
