import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💰 Portfolio v CZK & Srovnání se S&P 500")

# --- Funkce pro kurzy ---
@st.cache_data(ttl=3600)
def get_exchange_rates():
    # Stáhneme oba kurzy najednou
    data = yf.download(["USDCZK=X", "EURCZK=X"], period="1d", progress=False)
    # Zajištění, že máme data
    if not data.empty:
        rates = data['Close'].iloc[-1]
        return rates['USDCZK=X'], rates['EURCZK=X']
    return 23.5, 25.0 # Záložní kurzy pokud yfinance selže

# --- Nahrání souboru ---
uploaded_file = st.file_uploader("Nahraj svůj CSV soubor", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Debug: Zobrazení, co jsme načetli
    st.write(f"Načteno řádků: {len(df)}")
    
    # 1. PŘEVOD NA CZK (podle toho, co v tabulce máš)
    # Předpokládáme, že sloupce mají názvy 'Aktuální hodnota (USD)' a 'Aktuální hodnota (EUR)'
    usd_rate, eur_rate = get_exchange_rates()
    
    # Funkce pro vyčištění a převod
    def clean_and_convert(val, rate):
        if isinstance(val, str):
            val = val.replace('$','').replace('€','').replace(',','').replace(' ','')
        try:
            return float(val) * rate
        except:
            return 0.0

    # Přepočet na CZK
    df['Hodnota v CZK'] = 0.0
    if 'Aktuální hodnota (USD)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (USD)'].apply(lambda x: clean_and_convert(x, usd_rate))
    if 'Aktuální hodnota (EUR)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (EUR)'].apply(lambda x: clean_and_convert(x, eur_rate))

    # 2. ZOBRAZENÍ DAT
    st.subheader("Aktuální stav portfolia")
    st.dataframe(df, use_container_width=True)

    # 3. METRIKY (Součty)
    total_czk = df['Hodnota v CZK'].sum()
    st.metric("Celková hodnota celého portfolia (CZK)", f"{total_czk:,.0f} Kč")

else:
    st.info("Nahraj prosím CSV soubor ze svého Google Sheetu.")
