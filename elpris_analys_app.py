
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Elprisanalys med solenergi", layout="wide")

st.title("🔋 Elprisanalys med solenergi, Ellevio & Fortum (simulering)")
st.markdown("Simulerad analys av elpris från Nord Pool (Fortum), Ellevios effektavgift, och egen solproduktion.")

# Simulera data för ett dygn (24 timmar)
timmar = list(range(24))

np.random.seed(42)  # för reproducerbarhet

# Simulerat spotpris från Nord Pool (öre/kWh)
spotpris = np.random.normal(loc=80, scale=15, size=24).clip(40, 150)

# Simulerad solproduktion (negativ kostnad)
solproduktion = np.array([0]*6 + [1, 3, 5, 6, 5, 4, 2, 1] + [0]*7)

# Simulerad hushållsförbrukning (kWh)
förbrukning = np.random.normal(loc=1.5, scale=0.5, size=24).clip(0.5, 3)

# Simulerad effektavgift från Ellevio (baserad på maxeffekt)
effektavgift = max(förbrukning) * 10  # t.ex. 10 kr/kW som förenkling

# Total kostnad per timme
# Se till att alla variabler är NumPy-arrays
spotpris = np.array(spotpris)
förbrukning = np.array(förbrukning)
solproduktion = np.array(solproduktion)

# Kontrollera om alla array längder är lika
if len(spotpris) == len(förbrukning) == len(solproduktion):
    # Beräkning av kostnad per timme
    kostnad_per_timme = (spotpris * förbrukning) - (solproduktion * 80)
else:
    st.error("Längderna på spotpris, förbrukning och solproduktion matchar inte!")
    kostnad_per_timme = np.array([0] * len(spotpris))  # Skapa en dummy array för att förhindra kraschen


# Skapa DataFrame
    # Kontrollera om alla variabler har samma längd
if len(spotpris) == len(förbrukning) == len(solproduktion):
    # Skapa DataFrame om längderna är lika
    df = pd.DataFrame({
        'Spotpris': spotpris,
        'Förbrukning': förbrukning,
        'Solproduktion': solproduktion,
        'Kostnad per timme': kostnad_per_timme
    })
else:
    st.error("Längderna på spotpris, förbrukning och solproduktion matchar inte!")
    df = pd.DataFrame()  # Skapa en tom DataFrame för att förhindra kraschen

    "Timme": timmar,
    "Spotpris (öre/kWh)": spotpris,
    "Förbrukning (kWh)": förbrukning,
    "Solproduktion (kWh)": solproduktion,
    "Beräknad kostnad (öre)": kostnad_per_timme
})

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
st.dataframe(df.style.format({"Spotpris (öre/kWh)": "{:.0f}", "Förbrukning (kWh)": "{:.2f}", "Solproduktion (kWh)": "{:.1f}", "Beräknad kostnad (öre)": "{:.0f}"}))

st.markdown("---")
st.markdown(f"💡 **Simulerad effektavgift:** {effektavgift:.2f} kr (baserat på maxförbrukning)")

st.caption("Denna simulering är endast för utbildnings- och planeringssyfte. Spotpriser varierar varje dag.")
