import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Investiční Dashboard")

# --- CSS PRO DESIGN ---
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Investiční Dashboard")

# Nahrání dat
uploaded_file = st.file_uploader("Nahraj svůj export z Google Sheets (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 1. HLAVNÍ METRIKY (KPIs)
    st.subheader("Přehled portfolia")
    c1, c2, c3 = st.columns(3)
    c1.metric("Celková investice (CZK)", f"{df['Investovaná suma'].sum():,.0f} Kč")
    c2.metric("Aktuální hodnota (USD)", f"{df['aktuální hodnota v USD'].sum():,.2f} $")
    c3.metric("Celkový profit", f"{df['profit'].sum():,.2f} $")

    # 2. VIZUALIZACE
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Diverzifikace podle sektorů")
        fig_pie = px.pie(df, values='aktuální hodnota v USD', names='sektor', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("Výkonnost podle akcií")
        fig_bar = px.bar(df, x='Ticker', y='profit', color='profit', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. TABULKA S DETAILY
    st.subheader("Detailní tabulka")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Nahraj CSV soubor ze svého Google Sheetu pro zobrazení vizualizací.")
