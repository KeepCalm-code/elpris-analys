import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Elprisanalys", layout="wide")
st.title("🔌 Anderssons Solenergi Onsala")
st.markdown("Simulera och jämför elpriser från spotmarknaden med din egen solenergi.")

# Inmatning av användardata
st.sidebar.header("🔧 Inmatning")
fast_avgift = st.sidebar.number_input("Fast avgift (öre/kWh)", min_value=0, value=30)

# Skapa tomma listor för 24 timmar
förbrukning = []
solproduktion = []
timmar = list(range(24))

for t in timmar:
    f = st.sidebar.number_input(f"Förbrukning kl {t}:00 (kWh)", min_value=0.0, value=0.5, step=0.1, key=f"f_{t}")
    s = st.sidebar.number_input(f"Solproduktion kl {t}:00 (kWh)", min_value=0.0, value=0.2, step=0.1, key=f"s_{t}")
    förbrukning.append(f)
    solproduktion.append(s)

# Simulerade spotpriser per timme
np.random.seed(42)
spotpris = np.random.uniform(20, 120, size=24)  # i öre/kWh

# Kostnadsberäkning per timme
kostnad_per_timme = []
for i in range(24):
    kostnad = (spotpris[i] + fast_avgift) * förbrukning[i] - solproduktion[i] * 80
    kostnad_per_timme.append(kostnad)

# Simulerad effektavgift (kan anpassas)
effektavgift = max(förbrukning) * 100

# Skapa DataFrame
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

# Visualisering: Timmar med lägst kostnad
st.subheader("⏱️ Timmar med lägst kostnad")
min_kostnad_idx = df["Beräknad kostnad (öre)"].nsmallest(3).index
st.write("**Top 3 billigaste timmarna att använda el:**")
st.table(df.loc[min_kostnad_idx, ["Timme", "Beräknad kostnad (öre)"]].reset_index(drop=True))

# Besparing från solproduktion
total_besparing = sum([produktion * 80 for produktion in solproduktion])
st.subheader("💸 Besparing från solenergi")
st.markdown(f"Du har sparat **{total_besparing:.0f} öre ({total_besparing/100:.2f} kr)** tack vare dina solpaneler idag.")

st.markdown("---")
st.markdown(f"💡 **Simulerad effektavgift:** {effektavgift:.2f} kr (baserat på maxförbrukning)")
st.caption("Denna simulering är endast för utbildnings- och planeringssyfte. Spotpriser varierar varje dag.")
