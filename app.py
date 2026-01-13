import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# CSS for hvit skrift, mørk bakgrunn og gul "Spør verksmesteren"-knapp
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    
    /* Gule hovedknapper */
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }

    /* "Spør verksmesteren"-knappen: Gult felt, SORT tekst (Alltid synlig) */
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
        st.write("### Faglig hjelp")
        user_prompt = st.chat_input("Hva lurer du på?")
        
        if user_prompt:
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("API-nøkkel mangler i Secrets!")
            else:
                try:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester i byggfag. Svar kort og pedagogisk på norsk."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error(f"AI-feil: Sjekk API-nøkkelen din.")

        for m in st.session_state.messages[-3:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE FOR ALLE 10 TEMAER (INFO & QUIZ) ---
# Basert på Tittel.docx og kompetansemål-dokumenter 
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom, parker og hager. Inkluderer arbeid med stein, betong og planter.",
        "verktoy": "Murersnor, laser, steinkutter, vibrasjonsplate.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingid (Svennebrev).",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt", "Kutte stein"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "Graving, transport og vedlikehold av infrastruktur som veier og tunneler.",
        "verktoy": "Gravemaskin, hjullaster, dumper, nivelleringskikkert.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling i maskinførerfaget.",
        "quiz": ("Hva er påbudt verneutstyr i grøft?", ["Hjelm og vernesko", "Hørselsvern", "Ingenting"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "Konstruksjon av grunnmurer, vegger og trapper i betong, tegl og naturstein.",
        "verktoy": "Forskalingsutstyr, blandemaskin, vater, murerkjei.",
        "utdanning": "Vg1 Bygg -> Vg2 Betong og mur -> Lærlingid.",
        "quiz": ("Hvorfor brukes armeringsstål i betong?", ["Øke strekkfasthet", "Gjøre den lettere", "Pynt"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "Tekniske installasjoner som sikrer godt inneklima og lavt energibruk i bygg.",
        "verktoy": "Måleinstrumenter for trykk, isolasjonsverktøy, loddeutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Klima, energi og miljøteknikk -> Lærlingid.",
        "quiz": ("Hvorfor isolerer vi bygninger?", ["For å spare energi", "For utseende", "For tyngden"], "For å spare energi")
    },
    "Overflateteknikk": {
        "beskrivelse": "Beskyttelse og dekor av overflater gjennom maling, tapetsering og gulvlegging.",
        "verktoy": "Sparkel, pensler, slipemaskin, malerulle.",
        "utdanning": "Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid.",
        "quiz": ("Hva må gjøres før maling?", ["Vaske og fjerne støv", "Male rett på", "Bruke vann"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "beskrivelse": "Installasjon av vann, varme og avløpssystemer i alle typer bygg.",
        "verktoy": "Rørkutter, rørnøkkel, trykktestingspumpe.",
        "utdanning": "Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid.",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vannet", "Øke fart"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "Maskinell bearbeiding av treverk til elementer som dører, vinduer og limtre.",
        "verktoy": "CNC-maskiner, høvel, sag, fres.",
        "utdanning": "Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid.",
        "quiz": ("Hvilken tresort brukes mest til reisverk?", ["Gran", "Eik", "Furu"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "Oppføring og rehabilitering av trebygninger, inkludert vegger, tak og gulv.",
        "verktoy": "Hammer, sag, laser, vinkel, spikerpistol.",
        "utdanning": "Vg1 Bygg -> Vg2 Tømrer -> Lærlingid.",
        "quiz": ("Hva er standard c/c på stendere?", ["600 mm", "300 mm", "1200 mm"], "600 mm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "Fokus på HMS, sjekklister og dokumentasjon av eget arbeid.",
        "verktoy": "SJA-skjemaer, verneplaner, sjekklister.",
        "utdanning": "Gjennomgående tema i alle programfag.",
        "quiz": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Husk Mye Sagmugg", "Hjelp Med Snekring"], "Helse, Miljø og Sikkerhet")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "Praktisk trening i bedrift for å bli kjent med yrket.",
        "verktoy": "Varierer etter fagfelt.",
        "utdanning": "En del av Vg1 og Vg2 læreplanen.",
        "quiz": ("Viktigst i praksis?", ["Møte presis", "Dyrt verktøy", "Kunne alt"], "Møte presis")
    }
}

# --- FANER (INFO FØRST, SÅ QUIZ) ---
tab_info, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programområdene")
    selected_fag = st.selectbox("Velg fagområde:", list(data_db.keys()), key="info_box")
    
    if selected_fag in data_db:
        f = data_db[selected_fag]
        st.subheader(f"📍 {selected_fag}")
        
        col_desc, col_tool = st.columns(2)
        with col_desc:
            st.markdown("### 📋 Arbeidsområder")
            st.write(f["beskrivelse"])
        with col_tool:
            st.markdown("### 🛠️ Viktig Verktøy")
            st.write(f["verktoy"])
            
        st.markdown("### 🎓 Utdanning")
        st.info(f["utdanning"])

with tab_quiz:
    st.header("Tren på kompetansemålene")
    valgt_quiz = st.selectbox("Hva vil du trene på?", list(data_db.keys()), key="quiz_box")
    
    if valgt_quiz in data_db:
        spm, valg, svar = data_db[valgt_quiz]["quiz"]
        st.write(f"### {spm}")
        bruker_svar = st.radio("Velg svar:", valg, index=None, key=f"q_{valgt_quiz}")
        
        if st.button("Sjekk svar"):
            if bruker_svar == svar:
                st.success("RIKTIG! +20 poeng")
                st.session_state.points += 20
                st.balloons()
                st.rerun()
            elif bruker_svar is None:
                st.warning("Velg et svar først.")
            else:
                st.error("Feil svar. Prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    leader_data = {"Navn": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]}
    st.table(pd.DataFrame(leader_data).sort_values(by="Poeng", ascending=False))
