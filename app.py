import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Oppdatert CSS for bedre synlighet på AI-knapp og hvit skrift
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

    /* Spesifikk stil for AI-popover knappen så den er synlig */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background-color: #FFB300 !important;
        color: #000000 !important;
        border: 2px solid white;
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
    # Gjort AI-hjelperen mer synlig med en tydelig tittel
    with st.popover("🤖 ÅPNE AI-HJELPER", use_container_width=True):
        st.write("### Spør Verksmesteren")
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk på norsk."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("Nøkkel mangler i Secrets!")
            except Exception:
                st.error("Kunne ikke koble til AI.")
        for m in st.session_state.messages[-2:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- TEMAER OG INFO-DATABASE ---
# Basert på Tittel.docx og utdanningsvalg.png
info_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom som hager, parker og idrettsanlegg.",
        "verktoy": "Murersnor, vater, steinkutter, maskiner for graving.",
        "utdanning": "Vg1 Bygg- og anleggsteknikk -> Vg2 Anleggsgartner -> 2 år lærlingid."
    },
    "Anleggsteknikk": {
        "beskrivelse": "Arbeid med veier, tunneler, baner og tomteutgraving.",
        "verktoy": "Gravemaskiner, hjullastere, laserutstyr for måling.",
        "utdanning": "Vg1 Bygg- og anleggsteknikk -> Vg2 Anleggsteknikk -> Lærling i anleggsmaskinførerfaget."
    },
    "Tømrer": {
        "beskrivelse": "Bygger trekonstruksjoner som hus, hytter og takstoler.",
        "verktoy": "Hammer, sag, vinkel, laser, drill, spikerpistol.",
        "utdanning": "Vg1 Bygg- og anleggsteknikk -> Vg2 Tømrer -> 2 år lærlingid for svennebrev."
    },
    "Rørlegger": {
        "beskrivelse": "Installerer og vedlikeholder vann- og avløpssystemer i bygg.",
        "verktoy": "Rørkutter, rørnøkkel, trykktestingsutstyr.",
        "utdanning": "Vg1 Bygg- og anleggsteknikk -> Vg2 Rørlegger -> Lærlingid."
    }
}

# --- FANER ---
tab_quiz, tab_leader, tab_info = st.tabs(["🎮 Quiz", "🏆 Leaderboard", "📚 Infokanal"])

with tab_quiz:
    # (Quiz-logikken forblir den samme som sist)
    st.write("Tren på kompetansemålene!")
    valgt_tema = st.selectbox("Velg tema:", list(info_db.keys()))
    # ... spørsmål vises her ...

with tab_leader:
    st.write("### Toppliste")
    data = {"Navn": [st.session_state.user_name, "Demo-Elev"], "Poeng": [st.session_state.points, 250]}
    st.table(pd.DataFrame(data).sort_values(by="Poeng", ascending=False))

with tab_info:
    st.header("Informasjonskanal for Programfag")
    st.write("Her finner du informasjon om de ulike veiene innen bygg og anlegg.")
    
    valgt_info = st.selectbox("Velg fag for mer info:", list(info_db.keys()), key="info_select")
    
    if valgt_info in info_db:
        fag = info_db[valgt_info]
        st.subheader(f"Om {valgt_info}")
        st.write(f"**Hva gjør man?** {fag['beskrivelse']}")
        st.write(f"**Viktig verktøy:** {fag['verktoy']}")
        st.write(f"**Utdanningsløp:** {fag['utdanning']}")
        
        st.info("💡 Husk at du også kan spørre AI-Hjelperen øverst om spesifikke videreutdanninger som fagskole eller mesterbrev!")
