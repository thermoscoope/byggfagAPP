import streamlit as st

# Konfigurasjon
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Design-innstillinger (Mørk bakgrunn, hvit skrift, gule knapper)
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { 
        border-radius: 15px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }
    .stTextInput>div>div>input { color: white; }
    </style>
    """, unsafe_allow_html=True)

# Session State for poeng og chat
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: PROGRESSJON ---
st.sidebar.title("📊 Din Fremdrift")
st.sidebar.write(f"Poengsum: **{st.session_state.points}**")

if st.session_state.points < 100:
    st.sidebar.success("Nivå 1: Lærling-spire 🌱")
    nivaa_key = "n1"
elif st.session_state.points < 300:
    st.sidebar.warning("Nivå 2: Fagarbeider 🛠️")
    nivaa_key = "n2"
else:
    st.sidebar.error("Nivå 3: Mester 🏆")
    nivaa_key = "n3"

# --- HOVEDINNHOLD ---
st.title("🏗️ Byggfagtreneren")

tab1, tab2 = st.tabs(["🎮 Quiz & Trening", "🤖 Spør AI-Hjelperen"])

with tab1:
    temaer = ["Anleggsgartner", "Anleggsteknikk", "Betong og mur", "Klima, energi og miljøteknikk", 
              "Overflateteknikk", "Rørlegger", "Treteknikk", "Tømrer", "Arbeidsmiljø og dokumentasjon"]
    valgt_tema = st.selectbox("Velg tema:", temaer)

    # Utvidet database med Nivå 1, 2 og 3
    quiz_db = {
        "Tømrer": {
            "n1": ("Hva er standard c/c på stendere i en bærevegg?", ["60 cm", "30 cm", "120 cm"], "60 cm"),
            "n2": ("Hvilken type spiker bør brukes utendørs for å unngå rust?", ["Varmforzinket", "Blank spiker", "Kobberspiker"], "Varmforzinket"),
            "n3": ("Du skal bygge en taksperre. Hvilken beregning er viktigst for snølast?", ["Dimensjonering av tverrsnitt", "Fargen på undertaket", "Lengden på utstikk"], "Dimensjonering av tverrsnitt")
        },
        "Arbeidsmiljø og dokumentasjon": {
            "n1": ("Hva skal en SJA (Sikker Jobb Analyse) inneholde?", ["Risikovurdering av oppgaven", "Matpause-plan", "Navn på alle på bygget"], "Risikovurdering av oppgaven"),
            "n2": ("Hvem har ansvaret for at verneutstyr faktisk blir BRUKT?", ["Både arbeidsgiver og arbeidstaker", "Kun lærlingen", "Politiet"], "Både arbeidsgiver og arbeidstaker"),
            "n3": ("Hva er kravet til rekkverkshøyde ved arbeid over 2 meter?", ["1.0 meter", "0.5 meter", "2.0 meter"], "1.0 meter")
        },
        "Rørlegger": {
            "n1": ("Hva brukes en rørkutter til?", ["Kutte rør nøyaktig", "Varme opp rør", "Gjenge rør"], "Kutte rør nøyaktig"),
            "n2": ("Hvorfor legger vi inn en vannlås i avløpet?", ["For å hindre lukt", "For å rense vannet", "For å øke trykket"], "For å hindre lukt"),
            "n3": ("Hva er viktigst ved montering av rør-i-rør system?", ["At varerøret er utskiftbart", "At fargen er blå", "At det er limt fast"], "At varerøret er utskiftbart")
        }
        # Flere spørsmål kan legges inn her på samme format
    }

    # Vis spørsmål basert på tema og poengnivå
    if valgt_tema in quiz_db:
        data = quiz_db[valgt_tema].get(nivaa_key, quiz_db[valgt_tema]["n1"])
        st.write(f"### {data[0]}")
        svar = st.radio("Velg svar:", data[1], index=None)
        
        if st.button("Sjekk svar"):
            if svar == data[2]:
                st.success("Riktig! +20 poeng")
                st.session_state.points += 20
                st.balloons()
                st.rerun()
            else:
                st.error("Feil. Tenk deg om en gang til!")

with tab2:
    st.subheader("🤖 Din digitale Verksmester")
    st.write("Spør om alt fra Vg1 verktøy til Vg3 fagbrev-teori.")
    
    user_input = st.text_input("Hva lurer du på?")
    if st.button("Spør AI"):
        if user_input:
            # Her kobles AI-en på. For nå lager vi et "lekent" standardsvar:
            st.info(f"Verksmesteren sier: 'Godt spørsmål om {user_input}! For å svare som en proff: Husk alltid å sjekke TEK17 og produsentens monteringsanvisning. Vil du at jeg skal forklare mer om dette?'")
            # Logikk for ekte AI (API) legges her.
