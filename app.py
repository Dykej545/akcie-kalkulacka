import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Investiční Dashboard: Profesionální Tracker")

# 1. Nahrání portfolia z CSV
st.subheader("📁 Nahrát portfolio z Google Sheets (CSV)")
uploaded_file = st.file_uploader("Vyber svůj CSV soubor exportovaný z Google Sheets", type="csv")

if uploaded_file is not None:
    # Načtení dat
    df = pd.read_csv(uploaded_file)
    st.session_state.portfolio = df
    st.success("Portfolio úspěšně načteno!")

# Zobrazení dat, pokud existují
if 'portfolio' in st.session_state:
    st.subheader("Aktuální stav portfolia")
    st.dataframe(st.session_state.portfolio, use_container_width=True)

    # 2. Fundamentální analýza (pro vybranou akcii z nahraného CSV)
    st.subheader("🔍 Fundamentální analýza")
    tickers = st.session_state.portfolio["Ticker"].unique()
    selected_ticker = st.selectbox("Vyber akcii k analýze", tickers)
    
    col1, col2 = st.columns(2)
    with col1:
        pe = st.number_input("Cílový P/E poměr", value=25.0)
        growth = st.slider("Roční růst EPS (%)", 0, 50, 15) / 100
    with col2:
        base_eps = st.number_input("Výchozí EPS (TTM)", value=3.0)
        years = st.slider("Horizont (roky)", 1, 10, 5)

    # Výpočet projekce
    budouci_cena = (base_eps * (1 + growth)**years) * pe
    st.metric(label=f"Odhadovaná cena {selected_ticker} za {years} let", value=f"{round(budouci_cena, 2)} USD")

else:
    st.info("Nahraj prosím svůj CSV soubor z Google Sheets pro zobrazení portfolia.")
