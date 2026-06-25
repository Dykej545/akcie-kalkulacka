import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Investiční Dashboard")

st.title("📈 Investiční Dashboard")

# Nahrání CSV
uploaded_file = st.file_uploader("Nahraj svůj export z Google Sheets (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 1. HLAVNÍ METRIKY (KPIs)
    st.subheader("Přehled portfolia")
    
    # Používáme přesné názvy z tvého exportu
    total_invest_czk = df['suma v CZK'].sum()
    total_val_usd = df['Aktuální hodnota (USD)'].sum()
    total_profit = df['Profit'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Celková investice (CZK)", f"{total_invest_czk:,.0f} Kč")
    c2.metric("Aktuální hodnota (USD)", f"{total_val_usd:,.2f} $")
    c3.metric("Celkový profit", f"{total_profit:,.2f} $")

    # 2. VIZUALIZACE
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Diverzifikace podle sektorů")
        # Používáme sloupec 'Sektor'
        fig_pie = px.pie(df, values='Aktuální hodnota (USD)', names='Sektor', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("Výkonnost podle akcií (Profit)")
        # Používáme sloupce 'Název' a 'Profit'
        fig_bar = px.bar(df, x='Název', y='Profit', color='Profit', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. TABULKA S DETAILY
    st.subheader("Detailní tabulka")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Nahraj CSV soubor ze svého Google Sheetu pro zobrazení vizualizací.")
