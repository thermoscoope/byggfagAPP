import streamlit as st

# Konfigurasjon
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# CSS for hvit skrift på mørk bakgrunn (for lesbarhet)
st.markdown("""
    <style>
    .stApp { background-color: #1E1E1E; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { 
        border-radius: 20px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        width: 100%;
        font-size: 18px;
    }
    .stSelectbox label { color: #FFB300 !important; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Initialisering av session state
if 'points' not in st.session_state:
    st.session_state.points = 0

# Overskrift
st.title("🏗️ Byggfagtreneren")
st.write(f"## Din poengsum: {st.session_state.points}")

# Nivå-logikk
if st.session_state.points < 50:
    nivaa_navn = "Nivå 1: Lærling-spire 🌱"
    nivaa_key = "n1"
elif st.session_state.points < 150:
    nivaa_navn = "Nivå 2: Fagarbeider 🛠️"
    nivaa_key = "n2"
else:
    nivaa_navn = "Nivå 3: Mester 🏆"
    nivaa_key = "n3"

st.info(f"Akkurat nå er du på: **{nivaa_navn}**")

# Liste over alle programområder fra Tittel.docx
temaer = [
    "Anleggsgartner", "Anleggsteknikk", "Betong og mur", 
    "Klima, energi og miljøteknikk", "Overflateteknikk", 
    "Rørlegger", "Treteknikk", "Tømrer", 
    "Arbeidsmiljø og dokumentasjon", "Yrkesfaglig fordypning"
]

valgt_tema = st.selectbox("Hva vil du lære om nå?", temaer)

# Database med spørsmål (Eksempler basert på kompetansemål)
quiz_data = {
    "Anleggsgartner": {
        "n1": ("Hva brukes en murer snor til?", ["Lage rette linjer", "Måle temperatur", "Kutte stein"], "Lage rette linjer"),
    },
    "Anleggsteknikk": {
        "n1": ("Hvilket verneutstyr er påbudt i grøft?", ["Hjelm og synlighetsklær", "Badebukse", "Kun hansker"], "Hjelm og synlighetsklær"),
    },
    "Betong og mur": {
        "n1": ("Hva skjer hvis betong tørker for fort?", ["Den blir sterkere", "Den kan sprekke", "Ingenting"], "Den kan sprekke"),
    },
    "Klima, energi og miljøteknikk": {
        "n1": ("Hvorfor isolerer vi rør?", ["For å spare energi", "For at de skal se fine ut", "For at de skal veie mer"], "For å spare energi"),
    },
    "Overflateteknikk": {
        "n1": ("Hva er viktig før man maler en flate?", ["At den er ren og tørr", "At det regner", "At man har på seg hatt"], "At den er ren og tørr"),
    },
    "Rørlegger": {
        "n1": ("Hva betyr 'fall' på et avløpsrør?", ["At røret peker nedover", "At man har mistet røret", "At vannet står stille"], "At røret peker nedover"),
    },
    "Treteknikk": {
        "n1": ("Hvilken tresort brukes mest til konstruksjon i Norge?", ["Gran", "Eik", "Palme"], "Gran"),
    },
    "Tømrer": {
        "n1": ("Hva er standard avstand mellom stendere (c/c)?", ["60 cm", "100 cm", "20 cm"], "60 cm"),
    },
    "Arbeidsmiljø og dokumentasjon": {
        "n1": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Husk Mye Sagmugg", "Hjelp Med Snekring"], "Helse, Miljø og Sikkerhet"),
    },
    "Yrkesfaglig fordypning": {
        "n1": ("Hva er viktigst i møte med en kunde?", ["Å være høflig og profesjonell", "Å snakke høyest", "Å komme for sent"], "Å være høflig og profesjonell"),
    }
}

# Vis quiz basert på valg
if valgt_tema in quiz_data:
    spm, valg, svar = quiz_data[valgt_tema][nivaa_key]
    
    st.write(f"### {spm}")
    bruker_svar = st.radio("Velg ett svar:", valg, key=valgt_tema, index=None)

    if st.button("Send svar"):
        if bruker_svar == svar:
            st.success("RIKTIG! 🌟")
            st.session_state.points += 10
            st.balloons()
            st.rerun()
        else:
            st.error("Feil svar, prøv igjen! Tenk på hva som er sikrest og mest faglig korrekt.")

# Lærer-seksjon (Nederst)
st.divider()
with st.expander("🛠️ Lærertilgang (Lås opp oppgaver)"):
    st.write("Her kan læreren se progresjon og manuelt tildele bonuspoeng.")
    admin_kode = st.text_input("Skriv inn lærerkode:", type="password")
    if admin_kode == "bygg2024":
        st.write("### Elev-oversikt")
        st.write(f"Gjeldende elev har: {st.session_state.points} poeng.")
        if st.button("Gi 50 bonuspoeng"):
            st.session_state.points += 50
            st.rerun()
