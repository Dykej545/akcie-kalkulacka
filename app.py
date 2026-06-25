import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Investiční Dashboard")
st.title("📈 Investiční Dashboard")

uploaded_file = st.file_uploader("Nahraj svůj export z Google Sheets (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- IGNOROVÁNÍ CELKOVÉHO SOUČTU ---
    # Předpokládám, že ve sloupci 'Ticker' je v řádku se součtem napsáno "Celkem" 
    # Pokud tam máš něco jiného, změň 'Celkem' na tvůj název
    df = df[df['Ticker'] != 'Celkem'] 
    
    # --- FUNKCE PRO ČIŠTĚNÍ DAT ---
    def clean_currency(value):
        if isinstance(value, str):
            value = value.replace('Kč', '').replace('$', '').replace(',', '').replace(' ', '')
        try:
            return float(value)
        except:
            return 0.0

    # Aplikace čištění
    df['suma v CZK'] = df['suma v CZK'].apply(clean_currency)
    df['Aktuální hodnota (USD)'] = df['Aktuální hodnota (USD)'].apply(clean_currency)
    df['Profit'] = df['Profit'].apply(clean_currency)
    
    # 1. HLAVNÍ METRIKY
    st.subheader("Přehled portfolia")
    total_invest_czk = df['suma v CZK'].sum()
    total_val_usd = df['Aktuální hodnota (USD)'].sum()
    total_profit = df['Profit'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Celková investice (CZK)", f"{total_invest_czk:,.0f} Kč")
    c2.metric("Aktuální hodnota (USD)", f"{total_val_usd:,.2f} $")
    c3.metric("Celkový profit", f"{total_profit:,.2f} $")
