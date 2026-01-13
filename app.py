import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Design med hvit skrift og mørk bakgrunn
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
    .stTable { background-color: #1E1E1E; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- INNLOGGING / NAVN ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Skriv inn navnet ditt for å starte:")
    if st.button("Start Trening"):
        if name:
            st.session_state.user_name = name
            st.rerun()
        else:
            st.warning("Vennligst skriv inn et navn.")
    st.stop()

# --- TOPP-RAD: Tittel og AI ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Bruker: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}**")

with col2:
    with st.popover("🤖 AI-Hjelper"):
        st.write("### Spør Verksmesteren")
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk på byggfaglige spørsmål for elever."},
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

# --- HOVEDMENY (ALLE 10 TEMAER) ---
# Basert på Tittel.docx og utdanningsvalg.png 
quiz_db = {
    "Anleggsgartner": {
        "n1": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt", "Kutte stein"], "Lage rette linjer"),
        "n2": ("Hvordan sikre riktig fall på belegningsstein?", ["Bruk av lirer og vater", "Øyemål", "Gummislegge"], "Bruk av lirer og vater"),
        "n3": ("Hvilken type jord gir best drenering?", ["Sandholdig jord", "Leirjord", "Torv"], "Sandholdig jord")
    },
    "Anleggsteknikk": {
        "n1": ("Hvilket verneutstyr er påbudt i grøft?", ["Hjelm og vernesko", "Joggesko", "Ingenting"], "Hjelm og vernesko"),
        "n2": ("Hva er største fare ved graving uten sikring?", ["Rasing av masser", "Støv", "Dårlig vær"], "Rasing av masser"),
        "n3": ("Hva innebærer komprimering av masser?", ["Pakke massene tett", "Løsne massene", "Flytte massene"], "Pakke massene tett")
    },
    "Betong og mur": {
        "n1": ("Hva er hovedingrediensene i betong?", ["Sement, vann og tilslag", "Kun sand", "Tre og lim"], "Sement, vann og tilslag"),
        "n2": ("Hvorfor brukes armering i betong?", ["Øke strekkfasthet", "Gjøre den lettere", "Pynt"], "Øke strekkfasthet"),
        "n3": ("Hva er viktigst ved støping i kulde?", ["Tildekking og varme", "Mer vann", "Hurtig blanding"], "Tildekking og varme")
    },
    "Klima, energi og miljøteknikk": {
        "n1": ("Hvorfor isolerer vi bygninger?", ["For å spare energi", "For at de skal se fine ut", "For tyngden"], "For å spare energi"),
        "n2": ("Hva betyr kildesortering på byggeplassen?", ["Sortere avfall i riktig container", "Kaste alt sammen", "Brenne avfall"], "Sortere avfall i riktig container"),
        "n3": ("Hvordan påvirker TEK17 energikrav til boliger?", ["Stiller krav til isolasjon og tetthet", "Ingen krav", "Kun krav til farge"], "Stiller krav til isolasjon og tetthet")
    },
    "Overflateteknikk": {
        "n1": ("Hva må gjøres før maling av en vegg?", ["Vaske og fjerne støv", "Male rett på", "Bruke vann"], "Vaske og fjerne støv"),
        "n2": ("Hva er hensikten med grunning?", ["Sikre god heft for malingen", "Gjøre veggen glattere", "Gjøre det billigere"], "Sikre god heft for malingen"),
        "n3": ("Hvilken rulle gir glattest overflate?", ["Korthåret rulle", "Langhåret rulle", "Pensel"], "Korthåret rulle")
    },
    "Rørlegger": {
        "n1": ("Hva er vannlåsens viktigste oppgave?", ["Hindre kloakklukt", "Øke vanntrykket", "Rense vannet"], "Hindre kloakklukt"),
        "n2": ("Hva er fordelen med rør-i-rør system?", ["Vannskadesikring", "Billigere deler", "Raskere montering"], "Vannskadesikring"),
        "n3": ("Hva brukes et ekspansjonskar til?", ["Ta opp trykkendringer", "Lagre varmtvann", "Rense vannet"], "Ta opp trykkendringer")
    },
    "Treteknikk": {
        "n1": ("Hvilken tresort brukes mest til reisverk i Norge?", ["Gran", "Eik", "Furu"], "Gran"),
        "n2": ("Hva betyr fingerskjøting av trevirke?", ["Limbundet skjøt for lengde", "Spikring", "Lapping"], "Limbundet skjøt for lengde"),
        "n3": ("Hvordan tørkes trevirke mest kontrollert?", ["I tørkekammer", "Ute i sola", "I regnvær"], "I tørkekammer")
    },
    "Tømrer": {
        "n1": ("Hva er standard c/c avstand for stendere?", ["60 cm", "30 cm", "120 cm"], "60 cm"),
        "n2": ("Hva er vindsperrens hovedoppgave?", ["Hindre trekk inn i isolasjonen", "Bære taket", "Pynt"], "Hindre trekk inn i isolasjonen"),
        "n3": ("Hvilken spiker skal brukes i trykkimpregnert tre?", ["Varmforzinket eller syrefast", "Blank spiker", "Kobberspiker"], "Varmforzinket eller syrefast")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "n1": ("Hva skal man gjøre ved en ulykke?", ["Sikre skadested og gi førstehjelp", "Løpe bort", "Ringe hjem"], "Sikre skadested og gi førstehjelp"),
        "n2": ("Hva er formålet med en SJA?", ["Kartlegge risiko før arbeidet starter", "Planlegge lunsj", "Bestille verktøy"], "Kartlegge risiko før arbeidet starter"),
        "n3": ("Hvem har det øverste HMS-ansvaret på plassen?", ["Arbeidsgiver", "Lærlingen", "Kunden"], "Arbeidsgiver")
    },
    "Yrkesfaglig fordypning": {
        "n1": ("Hva forventes av en profesjonell yrkesutøver?", ["Å møte presis og ha riktig utstyr", "Komme for sent", "Glemme verktøy"], "Å møte presis og ha riktig utstyr"),
        "n2": ("Hvordan dokumentere eget praktisk arbeid?", ["Bilder og skriftlig logg", "Bare huske det", "Ikke dokumentere"], "Bilder og skriftlig logg"),
        "n3": ("Hvorfor er fagterminologi viktig i samhandling?", ["Unngå misforståelser og øke sikkerhet", "Snakke mest", "Vise seg frem"], "Unngå misforståelser og øke sikkerhet")
    }
}

# Nivå-styring
if st.session_state.points < 100:
    n_key, status = "n1", "Lærling-spire 🌱"
elif st.session_state.points < 300:
    n_key, status = "n2", "Fagarbeider 🛠️"
else:
    n_key, status = "n3", "Mester 🏆"

st.write(f"Din nåværende status: **{status}**")

# Tab-visning for Quiz og Leaderboard
tab_quiz, tab_leader = st.tabs(["🎮 Quiz", "🏆 Leaderboard"])

with tab_quiz:
    valgt_tema = st.selectbox("Velg programområde:", list(quiz_db.keys()))
    if valgt_tema in quiz_db:
        spm, valg, svar = quiz_db[valgt_tema][n_key]
        st.write(f"### {spm}")
        bruker_svar = st.radio("Velg svar:", valg, index=None, key=f"q_{valgt_tema}")
        if st.button("Sjekk svar"):
            if bruker_svar == svar:
                st.success("RIKTIG! Du fikk 20 poeng.")
                st.session_state.points += 20
                st.balloons()
                st.rerun()
            elif bruker_svar is None:
                st.warning("Velg et svar.")
            else:
                st.error("Feil svar. Prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    # Her lager vi et eksempel på et leaderboard. 
    # For en ekte klasse bør dette kobles til en database.
    data = {
        "Navn": [st.session_state.user_name, "Lærer (Demo)", "Anlegg-pro"],
        "Poeng": [st.session_state.points, 500, 240]
    }
    df = pd.DataFrame(data).sort_values(by="Poeng", ascending=False)
    st.table(df)

# --- LÆRER DASHBORD ---
with st.expander("🔐 For lærer"):
    pw = st.text_input("Passord:", type="password")
    if pw == "bygg123":
        st.write(f"Elev {st.session_state.user_name} har {st.session_state.points} poeng.")
        if st.button("Nullstill poeng"):
            st.session_state.points = 0
            st.rerun()
