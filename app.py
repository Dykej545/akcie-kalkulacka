import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Analýza akcií", layout="wide")

st.title("Finanční dashboard akcií")

ticker = st.sidebar.text_input("Zadej ticker (např. TSLA, AAPL):", "AAPL")
period = st.sidebar.selectbox("Období", ["5y", "max"])

if ticker:
    stock = yf.Ticker(ticker)
    
    # Stažení dat
    financials = stock.quarterly_financials.transpose()
    
    if not financials.empty:
        st.subheader(f"Finanční data pro {ticker}")
        
        # Výběr klíčových metrik
        metrics = ['Total Revenue', 'Net Income', 'Total Debt']
        
        for metric in metrics:
            if metric in financials.columns:
                st.write(f"### {metric}")
                fig = px.bar(financials, x=financials.index, y=metric, 
                             title=f"Vývoj {metric}", labels={'x': 'Datum', metric: 'Hodnota'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Metrika {metric} nebyla pro tuto akcii nalezena.")
    else:
        st.error("Nepodařilo se načíst data. Zkontroluj ticker.")
