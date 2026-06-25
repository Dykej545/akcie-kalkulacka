import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide", page_title="Moje Portfolio")

st.title("📈 Profesionální Portfolio Dashboard")

# Funkce pro stažení kurzů
@st.cache_data(ttl=3600)
def get_exchange_rates():
    data = yf.download(["USDCZK=X", "EURCZK=X"], period="1d", progress=False)
    rates = data['Close'].iloc[-1]
    return rates['USDCZK=X'], rates['EURCZK=X']

uploaded_file = st.file_uploader("Nahraj svůj aktuální CSV export z Google Sheets", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # ČIŠTĚNÍ DAT
    df = df.dropna(subset=['Název'])
    df = df[~df['Název'].str.contains("Celkem|Total", case=False, na=False)]
    
    usd_rate, eur_rate = get_exchange_rates()
    
    # Funkce pro převod měn
    def clean_and_convert(val, rate):
        if isinstance(val, str):
            val = val.replace('$','').replace('€','').replace(',','').replace(' ','')
        try: return float(val) * rate
        except: return 0.0

    # Přepočet na CZK
    df['Hodnota v CZK'] = 0.0
    if 'Aktuální hodnota (USD)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (USD)'].apply(lambda x: clean_and_convert(x, usd_rate))
    if 'Aktuální hodnota (EUR)' in df.columns:
        df['Hodnota v CZK'] += df['Aktuální hodnota (EUR)'].apply(lambda x: clean_and_convert(x, eur_rate))
    
    # METRIKY
    total_val = df['Hodnota v CZK'].sum()
    total_profit = df['Profit'].apply(lambda x: clean_and_convert(x, usd_rate)).sum()
    
    c1, c2 = st.columns(2)
    c1.metric("Celková hodnota (CZK)", f"{total_val:,.0f} Kč")
    c2.metric("Celkový profit (CZK)", f"{total_profit:,.0f} Kč")
    
    # GRAFY
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Diverzifikace sektorů")
        fig = px.pie(df, values='Hodnota v CZK', names='Sektor')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_b:
        st.subheader("Profit dle pozic")
        fig_bar = px.bar(df, x='Název', y='Profit', color='Profit', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.dataframe(df, use_container_width=True)

else:
    st.info("Nahraj prosím CSV soubor pro aktivaci dashboardu.")
