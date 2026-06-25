import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📈 Investiční Dashboard")

# 1. ČÁST: PORTFOLIO
st.header("💰 Portfolio Tracker")
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Akcie", "Počet", "Nákupní cena", "Měna"])

with st.expander("Přidat novou akcii"):
    with st.form("add_stock"):
        akcie = st.text_input("Ticker")
        pocet = st.number_input("Počet akcií", min_value=1)
        cena = st.number_input("Nákupní cena")
        mena = st.selectbox("Měna", ["USD", "CZK", "EUR"])
        if st.form_submit_button("Přidat"):
            new_row = pd.DataFrame([{"Akcie": akcie, "Počet": pocet, "Nákupní cena": cena, "Měna": mena}])
            st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)
            st.rerun()

st.table(st.session_state.portfolio)

# 2. ČÁST: ANALÝZA
st.header("📊 Fundamentální analýza")
col1, col2, col3 = st.columns(3)
with col1:
    growth = st.slider("Roční růst EPS (%)", 0, 50, 15) / 100
    base_eps = st.number_input("Výchozí EPS (TTM)", value=3.15)
with col2:
    pe = st.number_input("Cílový P/E poměr", value=25.0)
    years = st.slider("Počet let projekce", 1, 10, 5)
with col3:
    usd_czk = st.number_input("Kurz USD/CZK", value=23.50)
    eur_czk = st.number_input("Kurz EUR/CZK", value=25.20)

data = []
for i in range(1, years + 1):
    eps = base_eps * ((1 + growth) ** i)
    price_usd = eps * pe
    data.append({
        "Rok": i,
        "Cena (USD)": round(price_usd, 2),
        "Cena (CZK)": round(price_usd * usd_czk, 2),
        "Cena (EUR)": round(price_usd * (usd_czk / eur_czk), 2)
    })

df_calc = pd.DataFrame(data)
st.table(df_calc)
st.line_chart(df_calc.set_index("Rok")["Cena (USD)"])
