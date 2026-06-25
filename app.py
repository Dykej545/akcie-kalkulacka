import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💰 Portfolio v CZK & Srovnání se S&P 500")

# 1. Stažení aktuálních kurzů
@st.cache_data(ttl=3600) # Kurz se aktualizuje jednou za hodinu
def get_exchange_rates():
    data = yf.download(["USDCZK=X", "EURCZK=X"], period="1d")
    rates = data['Close'].iloc[-1]
    return rates['USDCZK=X'], rates['EURCZK=X']

usd_czk, eur_czk = get_exchange_rates()
st.sidebar.write(f"Aktuální kurz: 1 USD = {usd_czk:.2f} CZK")

# 2. Nahrání portfolia
uploaded_file = st.file_uploader("Nahraj CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Čištění (jen akcie)
    df = df[df['Sektor'] == 'Akcie'] 
    
    # Převod na CZK
    def to_czk(row):
        val = float(str(row['Aktuální hodnota (USD)']).replace('$','').replace(',',''))
        return val * usd_czk
    
    df['Hodnota v CZK'] = df.apply(to_czk, axis=1)
    
    # Metriky
    total_czk = df['Hodnota v CZK'].sum()
    profit_czk = (df['Profit'].str.replace('$','').astype(float) * usd_czk).sum()
    profit_pct = (profit_czk / (total_czk - profit_czk)) * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Celková hodnota (CZK)", f"{total_czk:,.0f} Kč")
    c2.metric("Celkový profit", f"{profit_czk:,.0f} Kč")
    c3.metric("Profit v %", f"{profit_pct:.2f} %")

    # 3. Srovnání se S&P 500
    st.subheader("Srovnání s S&P 500 (Vývoj 1 rok)")
    sp500 = yf.download("^GSPC", period="1y")['Close']
    st.line_chart(sp500)

    st.dataframe(df)
