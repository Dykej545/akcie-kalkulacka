import streamlit as st
import pandas as pd

st.title("📈 Fundamentální akciová kalkulačka")

# Výběr firmy
firma = st.selectbox("Vyber firmu k analýze", ["Netflix (NFLX)", "Apple (AAPL)", "Nvidia (NVDA)"])

# Nastavení dat podle výběru
if firma == "Netflix (NFLX)":
    current_price, default_eps = 85.85, 3.15
elif firma == "Apple (AAPL)":
    current_price, default_eps = 170.0, 6.50
else:
    current_price, default_eps = 120.0, 2.0

# Vstupní parametry (Side bar)
st.sidebar.header("Uprav parametry")
price = st.sidebar.number_input("Současná cena (USD)", value=current_price)
eps = st.sidebar.number_input("Výchozí EPS (TTM)", value=default_eps)
growth = st.sidebar.slider("Očekávaný roční růst EPS (%)", 0, 50, 15) / 100
pe = st.sidebar.number_input("Cílový P/E poměr", value=25.0)
years = st.sidebar.slider("Počet let projekce", 1, 10, 5)

# Výpočet
data = []
for i in range(1, years + 1):
    proj_eps = eps * ((1 + growth) ** i)
    est_price = proj_eps * pe
    cagr = ((est_price / price) ** (1 / i)) - 1
    data.append({
        "Rok": i, 
        "Projektovaný EPS": round(proj_eps, 2), 
        "Cílové P/E": pe, 
        "Odhadovaná cena": round(est_price, 2), 
        "CAGR": f"{round(cagr * 100, 2)}%"
    })

df = pd.DataFrame(data)

# Zobrazení výsledků
st.subheader(f"Projekce pro {firma}")
st.table(df)

st.line_chart(df.set_index("Rok")["Odhadovaná cena"])
Plaintext
streamlit
pandas
