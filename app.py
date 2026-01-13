import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# CSS for hvit skrift, mørk bakgrunn og synlig "Spør verksmesteren"-knapp
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    
    /* Hovedknapper */
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }

    /* Gult felt for Spør verksmesteren-knappen */
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }
    
    .stSelectbox label { color: #FFB300 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Skriv inn navnet ditt for å starte:")
    if st.button("Start Trening"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- TOPP-RAD ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Bruker: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}**")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        st.write("### Verksmesteren")
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk på norsk om byggfag."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("API-nøkkel mangler i Secrets!")
            except:
                st.error("Kunne ikke koble til AI.")
        for m in st.session_state.messages[-2:]:
            st.write(f"**Verksmesteren:** {m['content']}")

st.divider()

# --- DATABASE FOR ALLE 10 TEMAER ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom, parker, hager og idrettsanlegg. Arbeid med stein, betong og planter.",
        "verktoy": "Vater, murersnor, steinkutter, maskiner for graving og komprimering.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingtid (Svennebrev).",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt", "Kutte stein"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "Drift og vedlikehold av veier, tunneler, og utgraving av tomter. Fokus på maskiner.",
        "verktoy": "Gravemaskiner, hjullastere, laserutstyr for måling, dumper.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling i maskinførerfaget.",
        "quiz": ("Hva er påbudt verneutstyr i grøft?", ["Hjelm og vernesko", "Joggesko", "Ingenting"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "Oppføring av grunnmurer, vegger og konstruksjoner i betong, tegl og naturstein.",
        "verktoy": "Blandemaskin, murerkjei, vater, forskalingsutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Betong og mur -> 2 år lærlingtid.",
        "quiz": ("Hvorfor brukes armering i betong?", ["Øke strekkfasthet", "Gjøre den lettere", "Pynt"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "Fokus på tekniske installasjoner som ventilasjon, varme og energiøkonomisering (ENØK).",
        "verktoy": "Måleinstrumenter for luftstrøm, isolasjonsverktøy, loddeutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Klima, energi og miljø -> Lærlingid.",
        "quiz": ("Hvorfor isolerer vi bygg?", ["For å spare energi", "For utseende", "For tyngden"], "For å spare energi")
    },
    "Overflateteknikk": {
        "beskrivelse": "Maling, tapetsering og gulvlegging. Beskytter og dekorerer overflater.",
        "verktoy": "Pensler, ruller, sparkel, slipemaskiner.",
        "utdanning": "Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid.",
        "quiz": ("Hva må gjøres før maling?", ["Vaske og fjerne støv", "Male rett på", "Bruke vann"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "beskrivelse": "Montering av vann, avløp og varmeanlegg i boliger og industri.",
        "verktoy": "Rørkutter, rørnøkkel, trykktestingspumpe.",
        "utdanning": "Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid.",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Øke trykket", "Rense vannet"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "Industriell produksjon av treelementer, vinduer, dører og møbler.",
        "verktoy": "Stasjonære sager, høvelmaskiner, CNC-maskiner.",
        "utdanning": "Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid.",
        "quiz": ("Hvilken tresort brukes mest til reisverk?", ["Gran", "Eik", "Furu"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "Bygging og rehabilitering av hus og konstruksjoner i tre.",
        "verktoy": "Hammer, sag, vinkel, laser, drill, spikerpistol.",
        "utdanning": "Vg1 Bygg -> Vg2 Tømrer -> 2 år lærlingtid.",
        "quiz": ("Hva er standard c/c på stendere?", ["60 cm", "30 cm", "120 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "Fokus på HMS, lover og regler, og dokumentasjon av utført arbeid.",
        "verktoy": "Sjekklister, SJA-skjemaer, nettbrett for rapportering.",
        "utdanning": "Gjennomgående tema i alle byggfag.",
        "quiz": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Hele Min Snekker", "Husk Mye Sagmugg"], "Helse, Miljø og Sikkerhet")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "Praksis i bedrift eller skoleprosjekter for å teste ulike fagfelt.",
        "verktoy": "Varierer etter valgt fagområde.",
        "utdanning": "Del av Vg1 og Vg2 læreplanen.",
        "quiz": ("Hva er viktigst i møte med bedrift?", ["Å møte presis", "Å ha penest klær", "Å snakke høyest"], "Å møte presis")
    }
}

# --- FANER (BYTTET PLASS PÅ INFO OG QUIZ) ---
tab_info, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programområdene")
    st.write("Velg et fag for å se detaljer om arbeidsoppgaver, verktøy og utdanning.")
    valgt_info = st.selectbox("Velg fag:", list(data_db.keys()), key="info_select")
    
    if valgt_info in data_db:
        f = data_db[valgt_info]
        st.subheader(f"📍 {valgt_info}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📋 Beskrivelse")
            st.write(f["beskrivelse"])
        with c2:
            st.markdown("### 🛠️ Verktøy")
            st.write(f["verktoy"])
        
        st.markdown("### 🎓 Utdanningsvei")
        st.info(f["utdanning"])

with tab_quiz:
    st.header("Tren på kompetansemålene")
    valgt_tema = st.selectbox("Velg tema for quiz:", list(data_db.keys()), key="quiz_select")
    
    # Progresjons-logikk
    if st.session_state.points < 100:
        status = "Lærling-spire 🌱"
    elif st.session_state.points < 300:
        status = "Fagarbeider 🛠️"
    else:
        status = "Mester 🏆"
    st.write(f"Din status: **{status}**")

    if valgt_tema in data_db:
        spm, valg, svar = data_db[valgt_tema]["quiz"]
        st.write(f"### {spm}")
        bruker_svar = st.radio("Velg svar:", valg, index=None, key=f"q_{valgt_tema}")
        if st.button("Sjekk svar"):
            if bruker_svar == svar:
                st.success("RIKTIG! +20 poeng")
                st.session_state.points += 20
                st.balloons()
                st.rerun()
            elif bruker_svar is None:
                st.warning("Vennligst velg et svar.")
            else:
                st.error("Feil svar. Prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    data = {"Navn": [st.session_state.user_name, "Lærer (Demo)"], "Poeng": [st.session_state.points, 500]}
    st.table(pd.DataFrame(data).sort_values(by="Poeng", ascending=False))
