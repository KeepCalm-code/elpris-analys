import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Elprisanalys", layout="wide")
st.sidebar.header("🔧 Ange egna data")

# Fast avgift (t.ex. öre/kWh)
fast_avgift = st.sidebar.number_input("Fast avgift (öre/kWh)", value=20.0, min_value=0.0)

# Skapa interaktiva sliders för varje timme (0-23)
timmar = list(range(24))
förbrukning = []
solproduktion = []

st.sidebar.markdown("### ⚡ Elförbrukning och ☀️ Solproduktion per timme")
for t in timmar:
    f = st.sidebar.number_input(f"Förbrukning kl {t}:00 (kWh)", min_value=0.0, value=1.0, step=0.1, key=f"f_{t}")
    s = st.sidebar.number_input(f"Solproduktion kl {t}:00 (kWh)", min_value=0.0, value=0.0, step=0.1, key=f"s_{t}")
    förbrukning.append(f)
    solproduktion.append(s)


st.title("🔌 Anderssons Elprisanalys med Solproduktion")

# Välj elnätsbolag
nätbolag = st.selectbox("Välj elnätsbolag", ["Fortum", "Ellevio"])

# Sätt fast avgift beroende på val
if nätbolag == "Fortum":
    fast_avgift = 15  # öre/kWh
else:
    fast_avgift = 25  # öre/kWh

# Simulerade data
timmar = list(range(24))
spotpris = np.random.uniform(30, 80, size=24)
förbrukning = np.random.uniform(0.5, 2.0, size=24)
solproduktion = [0]*6 + list(np.random.uniform(0.2, 1.5, size=10)) + [0]*8

# Kostnadsberäkning
# Konvertera alla listor till float arrays för att undvika datatypfel
spotpris = np.array(spotpris, dtype=float)
förbrukning = np.array(förbrukning, dtype=float)
solproduktion = np.array(solproduktion, dtype=float)

# Kostnadsberäkning
kostnad_per_timme = ((spotpris + fast_avgift) * förbrukning) - (solproduktion * 80)


# Kontrollera att alla listor har samma längd
if len(spotpris) == len(förbrukning) == len(solproduktion) == len(timmar):
    df = pd.DataFrame({
        "Timme": timmar,
        "Spotpris (öre/kWh)": spotpris,
        "Förbrukning (kWh)": förbrukning,
        "Solproduktion (kWh)": solproduktion,
        "Beräknad kostnad (öre)": kostnad_per_timme
    })
else:
    st.error("Längderna på listorna matchar inte!")
    df = pd.DataFrame()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Elpris & Förbrukning")
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(df["Timme"], df["Spotpris (öre/kWh)"], 'g-', label="Spotpris")
    ax2.plot(df["Timme"], df["Förbrukning (kWh)"], 'b--', label="Förbrukning")
    ax1.set_xlabel("Timme")
    ax1.set_ylabel("Spotpris (öre/kWh)", color='g')
    ax2.set_ylabel("Förbrukning (kWh)", color='b')
    st.pyplot(fig)

with col2:
    st.subheader("☀️ Solproduktion och kostnad")
    fig2, ax3 = plt.subplots()
    ax4 = ax3.twinx()
    ax3.bar(df["Timme"], df["Solproduktion (kWh)"], color='orange', label="Solproduktion")
    ax4.plot(df["Timme"], df["Beräknad kostnad (öre)"], 'r-', label="Kostnad")
    ax3.set_xlabel("Timme")
    ax3.set_ylabel("Solproduktion (kWh)", color='orange')
    ax4.set_ylabel("Beräknad kostnad (öre)", color='r')
    st.pyplot(fig2)

# Visar data
st.subheader("📄 Dataöversikt")
st.dataframe(df.style.format({
    "Spotpris (öre/kWh)": "{:.0f}",
    "Förbrukning (kWh)": "{:.2f}",
    "Solproduktion (kWh)": "{:.1f}",
    "Beräknad kostnad (öre)": "{:.0f}"
}))

# Effektavgiftssimulering
effektavgift = max(förbrukning) * 20  # Exempelvärde för simulering

st.markdown("---")
st.markdown(f"💡 **Simulerad effektavgift:** {effektavgift:.2f} kr (baserat på maxförbrukning)")
st.caption("Denna simulering är endast för utbildnings- och planeringssyfte. Spotpriser varierar varje dag.")
