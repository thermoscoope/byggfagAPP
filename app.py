import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    
    /* Gule knapper med sort tekst for maksimal synlighet */
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }

    /* "Spør verksmesteren"-knappen: Gult felt, SORT tekst (alltid synlig) */
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* Justering for tekst i AI-chat slik at den er lesbar i hvite felt */
    .stChatMessage { color: #000000 !important; }
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
        user_prompt = st.chat_input("Hva lurer du på om byggfag?")
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk på norsk om byggfag VG1-VG3."},
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
# Basert på Tittel.docx og kompetansemål-dokumenter
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom, parker og hager. Inkluderer arbeid med stein, betong og beplantning.",
        "verktoy": "Murersnor, laser, steinkutter, vibrasjonsplate (hoppetusse).",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingid (Svennebrev).",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt", "Kutte stein"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "Graving, transport og vedlikehold av infrastruktur som veier og tunneler.",
        "verktoy": "Gravemaskin, hjullaster, dumper, nivelleringskikkert.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling i maskinførerfaget.",
        "quiz": ("Hva er påbudt verneutstyr i grøft dypere enn 2 meter?", ["Hjelm og vernesko", "Hørselsvern", "Ingenting"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "Konstruksjon av grunnmurer, vegger og trapper i betong, tegl og naturstein.",
        "verktoy": "Forskalingsutstyr, blandemaskin, vater, murerkjei.",
        "utdanning": "Vg1 Bygg -> Vg2 Betong og mur -> Lærlingid.",
        "quiz": ("Hvorfor brukes armeringsstål i betong?", ["Øke strekkfasthet", "Gjøre betongen lettere", "Pynt"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "Tekniske installasjoner som sikrer godt inneklima og lavt energibruk i bygg.",
        "verktoy": "Måleinstrumenter for trykk, isolasjonsverktøy, loddeutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Klima, energi og miljøteknikk -> Lærlingid.",
        "quiz": ("Hvorfor er det viktig å isolere rør i kalde soner?", ["Spare energi og hindre frost", "Pynte rørene", "Øke vanntrykket"], "Spare energi og hindre frost")
    },
    "Overflateteknikk": {
        "beskrivelse": "Beskyttelse og dekor av overflater gjennom maling, tapetsering og gulvlegging.",
        "verktoy": "Sparkel, pensler, slipemaskin, malerulle.",
        "utdanning": "Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid.",
        "quiz": ("Hva må gjøres med en gipsvegg før maling?", ["Sparkle og slipe skjøter", "Male rett på", "Vaske med såpe"], "Sparkle og slipe skjøter")
    },
    "Rørlegger": {
        "beskrivelse": "Installasjon av vann, varme og avløpssystemer i alle typer bygg.",
        "verktoy": "Rørkutter, rørnøkkel, trykktestingspumpe, loddebolt.",
        "utdanning": "Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid.",
        "quiz": ("Hvilken funksjon har en vannlås i et avløp?", ["Hindre kloakklukt", "Rense vannet", "Øke farten på vannet"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "Maskinell bearbeiding av treverk til elementer som dører, vinduer og limtre.",
        "verktoy": "CNC-maskiner, høvel, sag, fres.",
        "utdanning": "Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid.",
        "quiz": ("Hvilken tresort brukes mest til bærekonstruksjoner i Norge?", ["Gran", "Eik", "Furu"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "Oppføring og rehabilitering av trebygninger, inkludert vegger, tak og gulv.",
        "verktoy": "Hammer, sag, laser, vinkel, spikerpistol.",
        "utdanning": "Vg1 Bygg -> Vg2 Tømrer -> Lærlingid.",
        "quiz": ("Hva er standard avstand (c/c) mellom stendere i en vegg?", ["600 mm", "300 mm", "1200 mm"], "600 mm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "Systematisk arbeid med HMS for å sikre en trygg og effektiv byggeplass.",
        "verktoy": "Risikovurderingsskjema (SJA), sjekklister, verneplaner.",
        "utdanning": "Integrert i alle programområder på Vg1 og Vg2.",
        "quiz": ("Hva står forkortelsen SJA for?", ["Sikker jobb-analyse", "Snekkerens jobb-avtale", "Sikker jording-ansvar"], "Sikker jobb-analyse")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "Praktisk trening ute i bedrift for å bli kjent med yrket og krav i arbeidslivet.",
        "verktoy": "Varierer etter valgt bedrift/fagfelt.",
        "utdanning": "En del av både Vg1 og Vg2.",
        "quiz": ("Hva er det viktigste når du skal ut i praksis i en bedrift?", ["Møte presis og vise interesse", "Ha dyrt verktøy", "Kunne alt fra før"], "Møte presis og vise interesse")
    }
}

# --- FANER (INFO FØRST, SÅ QUIZ) ---
tab_info, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    st.write("Her kan du lære om de ulike fagene før du tar quizen.")
    
    selected_fag = st.selectbox("Velg fagområde:", list(data_db.keys()), key="info_box")
    
    if selected_fag in data_db:
        f = data_db[selected_fag]
        st.subheader(f"📍 {selected_fag}")
        
        # Kategoriserte felt
        col_desc, col_tool = st.columns(2)
        with col_desc:
            st.markdown("### 📋 Arbeidsområder")
            st.write(f["beskrivelse"])
        with col_tool:
            st.markdown("### 🛠️ Viktig Verktøy")
            st.write(f["verktoy"])
            
        st.markdown("### 🎓 Utdanning og Videreutdanning")
        st.info(f["utdanning"])
        st.write("Etter svennebrev kan du ta fagskole (toårig teknisk utdanning) eller mesterbrev.")

with tab_quiz:
    st.header("Tren på kompetansemålene")
    valgt_quiz = st.selectbox("Hva vil du trenge på?", list(data_db.keys()), key="quiz_box")
    
    # Status-logikk
    if st.session_state.points < 100:
        status = "Lærling-spire 🌱"
    elif st.session_state.points < 300:
        status = "Fagarbeider 🛠️"
    else:
        status = "Mester 🏆"
    st.write(f"Din status: **{status}**")

    if valgt_quiz in data_db:
        spm, valg, svar = data_db[valgt_quiz]["quiz"]
        st.write(f"### {spm}")
        bruker_svar = st.radio("Velg riktig svar:", valg, index=None, key=f"q_{valgt_quiz}")
        
        if st.button("Sjekk svar"):
            if bruker_svar == svar:
                st.success("RIKTIG! Du fikk 20 poeng.")
                st.session_state.points += 20
                st.balloons()
                st.rerun()
            elif bruker_svar is None:
                st.warning("Velg et alternativ før du sjekker.")
            else:
                st.error("Feil svar. Se i Infokanalen eller spør Verksmesteren!")

with tab_leader:
    st.write("### Toppliste")
    leader_data = {"Navn": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]}
    st.table(pd.DataFrame(leader_data).sort_values(by="Poeng", ascending=False))
