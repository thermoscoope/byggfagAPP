import streamlit as st
import datetime

# Sidetittel og ikon
st.set_page_config(page_title="Bygg-Loggen", page_icon="🏗️")

# Enkel styling for å gjøre den mer "leken"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #ffc107; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Min Praktiske Yrkesutøvelse")
st.write("Dokumenter arbeidet ditt direkte fra byggeplassen.")

# 1. VELG FAG (Basert på utdanningsvalg.png)
fag_liste = ["Tømrer", "Rørlegger", "Betong og mur", "Anleggsteknikk", "Overflateteknikk"]
valgt_fag = st.selectbox("Hvilket fag jobber du med i dag?", fag_liste)

st.divider()

# 2. HMS OG VERNEUTSTYR (Basert på kompetansemål arbeidsmiljø og dokumentasjon.png)
st.subheader("🛡️ HMS og Dokumentasjon")
col1, col2 = st.columns(2)

with col1:
    hms_sjekk = st.checkbox("Jeg har vurdert risiko") # Dekker: "vurdere risiko og utføre forebyggende tiltak"
    ryddig_plass = st.checkbox("Arbeidsplassen er ryddig") # Dekker: "betydningen av orden på bygge- og anleggsplasser"

with col2:
    verneutstyr = st.checkbox("Bruker riktig verneutstyr") # Dekker: "velge ut og bruke personlig verneutstyr"

# 3. PRAKTISK ARBEID (Basert på kompetansemål praktisk yrkesutøvelse.png)
st.subheader("🛠️ Dagens innsats")
beskrivelse = st.text_area("Hva har du gjort i dag?", placeholder="Beskriv arbeidet med fagterminologi...")

# Kamera-funksjon for dokumentasjon
bilde = st.camera_input("Ta bilde av utført arbeid eller arbeidsstilling") # Dekker: "dokumentere eget arbeid"

# 4. REFLEKSJON (Viktig del av vurderingen)
st.subheader("🧐 Egenvurdering")
mestring = st.select_slider(
    "Hvordan gikk det i dag?",
    options=["Trenger hjelp", "Trenger litt veiledning", "Jobber selvstendig", "Kan lære bort til andre"]
)

# LAGRE-KNAPP
if st.button("Lagre loggføring"):
    if bilde and hms_sjekk:
        st.balloons()
        st.success(f"Loggført! {valgt_fag}-oppdraget er lagret.")
        # Her kan man senere legge til logikk for å sende dette til en database eller e-post
    else:
        st.error("Husk å ta bilde og sjekke HMS før du lagrer!")
