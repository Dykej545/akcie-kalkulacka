import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💰 Portfolio v CZK & Srovnání se S&P 500")

@st.cache_data(ttl=3600)
def get_exchange_rates():
    data = yf.download(["USDCZK=X", "EURCZK=X"], period="1d", progress=False)
    if not data.empty:
        rates = data['Close'].iloc[-1]
        return rates['USDCZK=X'], rates['EURCZK=X']
    return 23.5, 25.0

uploaded_file = st.file_uploader("Nahraj svůj CSV soubor", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- ČIŠTĚNÍ DAT: Odstranění řádků se součty ---
    # Odstraní řádky, kde je 'Název' prázdný, nebo obsahuje "Celkem", "Total"
    df = df.dropna(subset=['Název'])
    df = df[~df['Název'].str.contains("Celkem|Total", case=False, na=False)]
    
    # Přepočet na CZK
    usd_rate, eur_rate = get_exchange_rates()
    
    def clean_and_convert(val, rate):
        if isinstance(val, str):
            val = val.replace('$','').replace('€','').replace(',','').replace(' ','')
        try:
            return float(val) * rate
        except:
            return 0.0

    df['Hodnota v CZK'] = 0.0
    if 'Aktuální hodnota (USD)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (USD)'].apply(lambda x: clean_and_convert(x, usd_rate))
    if 'Aktuální hodnota (EUR)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (EUR)'].apply(lambda x: clean_and_convert(x, eur_rate))

    # Zobrazení očištěných dat
    st.subheader("Aktuální stav portfolia (bez součtů)")
    st.dataframe(df, use_container_width=True)

    # Metriky
    total_czk = df['Hodnota v CZK'].sum()
    st.metric("Celková hodnota očištěného portfolia (CZK)", f"{total_czk:,.0f} Kč")

else:
    st.info("Nahraj prosím CSV soubor.")
