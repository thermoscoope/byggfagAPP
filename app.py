import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }
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
            # Sjekk om hemmeligheter er satt opp
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("Feil: API-nøkkel mangler i Streamlit Secrets!")
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
                    st.error(f"AI-feil: {str(e)}")

        for m in st.session_state.messages[-3:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE (INFO & QUIZ) ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom, parker og hager.",
        "verktoy": "Murersnor, laser, steinkutter.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsgartner -> Lærling.",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt", "Kutte stein"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "Graving, transport og vedlikehold av infrastruktur.",
        "verktoy": "Gravemaskin, hjullaster, dumper.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling.",
        "quiz": ("Hva er påbudt i grøft?", ["Hjelm og vernesko", "Hørselsvern", "Ingenting"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "Konstruksjon i betong, tegl og naturstein.",
        "verktoy": "Forskalingsutstyr, murerkjei.",
        "utdanning": "Vg1 Bygg -> Vg2 Betong og mur -> Lærling.",
        "quiz": ("Hvorfor brukes armering?", ["Øke strekkfasthet", "Gjøre lettere", "Pynt"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "Inneklima og energibruk i bygg.",
        "verktoy": "Måleinstrumenter, isolasjonsverktøy.",
        "utdanning": "Vg1 Bygg -> Vg2 Klima/Energi -> Lærling.",
        "quiz": ("Hvorfor isolere rør?", ["Spare energi", "Pynt", "Øke trykk"], "Spare energi")
    },
    "Overflateteknikk": {
        "beskrivelse": "Maling, tapetsering og gulvlegging.",
        "verktoy": "Sparkel, pensler, slipemaskin.",
        "utdanning": "Vg1 Bygg -> Vg2 Overflate -> Lærling.",
        "quiz": ("Hva gjøres før maling?", ["Sparkle og slipe", "Male rett på", "Vaske med såpe"], "Sparkle og slipe")
    },
    "Rørlegger": {
        "beskrivelse": "Vann, varme og avløpssystemer.",
        "verktoy": "Rørkutter, rørnøkkel, trykkpumpe.",
        "utdanning": "Vg1 Bygg -> Vg2 Rørlegger -> Lærling.",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vannet", "Øke fart"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "Industriell bearbeiding av treverk.",
        "verktoy": "CNC-maskiner, høvel, sag.",
        "utdanning": "Vg1 Bygg -> Vg2 Treteknikk -> Lærling.",
        "quiz": ("Hvilken tresort brukes mest?", ["Gran", "Eik", "Furu"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "Oppføring av trebygninger.",
        "verktoy": "Hammer, sag, laser, drill.",
        "utdanning": "Vg1 Bygg -> Vg2 Tømrer -> Lærling.",
        "quiz": ("Hva er standard c/c?", ["600 mm", "300 mm", "1200 mm"], "600 mm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "Systematisk arbeid med HMS.",
        "verktoy": "SJA, sjekklister, verneplaner.",
        "utdanning": "Integrert i alle programfag.",
        "quiz": ("Hva står SJA for?", ["Sikker jobb-analyse", "Snekker-avtale", "Sikker jord"], "Sikker jobb-analyse")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "Praktisk trening ute i bedrift.",
        "verktoy": "Varierer etter fagfelt.",
        "utdanning": "Vg1 og Vg2.",
        "quiz": ("Viktigst i praksis?", ["Møte presis", "Dyrt verktøy", "Kunne alt"], "Møte presis")
    }
}

# --- FANER ---
tab_info, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    selected_fag = st.selectbox("Velg fagområde:", list(data_db.keys()), key="info_box")
    if selected_fag in data_db:
        f = data_db[selected_fag]
        st.subheader(f"📍 {selected_fag}")
        col_desc, col_tool = st.columns(2)
        with col_desc:
            st.markdown("### 📋 Arbeidsområder")
            st.write(f["beskrivelse"])
        with col_tool:
            st.markdown("### 🛠️ Verktøy")
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
            else:
                st.error("Feil svar. Prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    leader_data = {"Navn": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]}
    st.table(pd.DataFrame(leader_data).sort_values(by="Poeng", ascending=False))
