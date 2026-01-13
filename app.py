import streamlit as st
import time

# Konfigurasjon for lekent design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Custom CSS for å få det "stilrene men lekne" utseendet
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 20px;
        height: 3em;
        width: 100%;
        background-color: #FFB300; /* Oransje fra utdanningsvalg-bildet */
        color: white;
        font-weight: bold;
    }
    .main {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialiser poengsum og nivå i minnet (Session State)
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'level' not in st.session_state:
    st.session_state.level = "Lærling-spire"

# Overskrift basert på Tittel.docx
st.title("🏗️ Byggfagtreneren")
st.subheader(f"Velkommen, {st.session_state.level}! Poeng: {st.session_state.points}")

# Meny basert på Temaene dine
tema = st.selectbox("Hva vil du trene på i dag?", [
    "Arbeidsmiljø og dokumentasjon", 
    "Tømrer", 
    "Anleggsgartner", 
    "Betong og mur"
])

st.divider()

# Eksempel på en Quiz-modul (Nivå 1)
if tema == "Arbeidsmiljø og dokumentasjon":
    st.write("### 🛡️ Nivå 1: Sikkerhet først!")
    q1 = st.radio(
        "Hva skal du gjøre hvis du ser en ulykke på byggeplassen?",
        ["Ringe hjem", "Sikre skadestedet og gi førstehjelp", "Fortsette å jobbe"],
        index=None
    )

    if st.button("Sjekk svar"):
        if q1 == "Sikre skadestedet og gi førstehjelp":
            st.balloons() # Lekent element!
            st.success("Helt riktig! Du er en trygg yrkesutøver.")
            st.session_state.points += 10
        else:
            st.error("Ikke helt. Husk at sikkerhet alltid kommer først!")

# Lærer-dashbord (skjult eller nederst)
with st.expander("🔐 For Lærer (Dashbord)"):
    st.write(f"Elevens progresjon: {st.session_state.points} poeng.")
    if st.session_state.points > 50:
        st.write("✅ Eleven er klar for Nivå 2: Fagarbeider!")
