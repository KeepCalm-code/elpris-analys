import streamlit as st
import requests
from datetime import datetime

# Hämta dagens datum
idag = datetime.now().date()
år = idag.strftime("%Y")
månad = idag.strftime("%m")
dag = idag.strftime("%d")

# Välj prisområde
prisområde = st.sidebar.selectbox("Välj prisområde", ["SE1", "SE2", "SE3", "SE4"], index=2)  # SE3 förval

# Hämta spotpriser från API
api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{år}/{månad}-{dag}_{prisområde}.json"
try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    
    # Extrahera spotpriser från API-data
    spotpris = [round(entry["SEK_per_kWh"] * 100, 2) for entry in data]  # konvertera till öre/kWh
    st.write(f"**Spotpriser för {dag}-{månad}-{år} i {prisområde}:**")
    
    # Visa spotpriser som en lista per timme
    for t, pris in enumerate(spotpris):
        st.write(f"Timme {t}: {pris} öre/kWh")
        
except:
    st.error("Kunde inte hämta data från elprisetjustnu.se – använder slumpade priser.")
    spotpris = [round(50 + t * 2, 2) for t in range(24)]  # Slumpade priser för test
    st.write(f"Slumpade spotpriser: {spotpris}")


