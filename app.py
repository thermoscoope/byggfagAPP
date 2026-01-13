import streamlit as st
from openai import OpenAI
import pandas as pd
import math

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
    if st.button("Begynn"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- TOPP-RAD ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Elev: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}**")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar som en erfaren norsk byggmester. Kort og pedagogisk."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except:
                st.error("AI-hjelper utilgjengelig.")
        for m in st.session_state.messages[-2:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE FOR ALLE 10 TEMAER ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "🌱 Bygger og vedlikeholder uterom, parker og hager. 🧱 Kombinerer planter med stein, betong og treverk.",
        "verktoy": "Vater, murersnor, steinkutter, maskiner for graving.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingtid.",
        "videre": "🎓 Fagskole, mesterbrev eller landskapsarkitektur.",
        "motivasjon": "✨ Liker du å se resultater som vokser og blir vakrere med årene? Her setter du spor folk vil nyte i generasjoner!",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 Betjener store maskiner for veibygging, tunneler og utgraving. 🏗️ Legger grunnlaget for samfunnet vårt.",
        "verktoy": "Gravemaskiner, hjullastere, dumpere, GPS-måleutstyr.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærlingid.",
        "videre": "🎓 Maskinentreprenørskolen, fagskole eller ingeniør.",
        "motivasjon": "💪 Er du fascinert av store maskiner? Her får du flytte fjell og bygge veiene som binder landet sammen!",
        "quiz": ("Hva er påbudt i grøft?", ["Hjelm og vernesko", "Hørselsvern"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "🏢 Bygger solide konstruksjoner i betong og stein. 🏗️ Fra grunnmurer til store bruer.",
        "verktoy": "Forskalingsutstyr, blandemaskin, murerkjei, vater.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Betong og mur -> Lærlingid.",
        "videre": "🎓 Mesterbrev, fagskole eller byggeteknikk.",
        "motivasjon": "🧱 Vil du bygge noe som står i 100 år? Her er du arkitektens høyre hånd i å forme bybildet!",
        "quiz": ("Hvorfor armere betong?", ["Øke strekkfasthet", "For fargen"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "🌡️ Spesialister på inneklima og moderne energisparing. ❄️ Ventilasjon, varme og sanitet.",
        "verktoy": "Måleinstrumenter, loddeutstyr, blikkenslagersaks.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Klima, energi og miljøteknikk -> Lærlingid.",
        "videre": "🎓 KEM-ingeniør, fagskole eller energi-spesialisering.",
        "motivasjon": "🌍 Vil du ha en nøkkelrolle i det grønne skiftet? Her jobber du med teknologien som redder klimaet!",
        "quiz": ("Hvorfor isolerer vi bygg?", ["Spare energi", "For tyngden"], "Spare energi")
    },
    "Overflateteknikk": {
        "beskrivelse": "🎨 Beskytter og dekorerer bygg utvendig og innvendig. 🖌️ Maling, tapet og gulvlegging.",
        "verktoy": "Sparkel, pensler, slipemaskin, malerulle.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid.",
        "videre": "🎓 Mesterbrev, interiørdesign eller fargekonsulent.",
        "motivasjon": "🌈 Er du kreativ? Her setter du den siste finishen som kunden faktisk ser og tar på hver dag!",
        "quiz": ("Hva gjøres før maling?", ["Vaske og fjerne støv", "Male rett på"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "beskrivelse": "🚿 Installerer vann, varme og avløpssystemer. 🛠️ Viktig rolle i boliger og industri.",
        "verktoy": "Rørkutter, rørnøkkel, trykkpumpe.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid.",
        "videre": "🎓 Fagskole (VVS), mesterbrev eller ingeniør.",
        "motivasjon": "💧 Ingen bygg fungerer uten rørleggeren. Vil du ha en sikker jobb med varierte utfordringer?",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vann"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "🏭 Industriell produksjon med tre som råstoff. ⚙️ Høyteknologisk produksjon av takstoler, vinduer og dører.",
        "verktoy": "CNC-maskiner, automatiske sager, limpresser.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid.",
        "videre": "🎓 Fagskole, produksjonsledelse eller ingeniør.",
        "motivasjon": "🌲 Trives du best med maskiner og fabrikkdrift? Her skaper du fremtidens bærekraftige byggeklosser!",
        "quiz": ("Hvilken tresort brukes mest?", ["Gran", "Eik"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "🏠 Oppføring av trebygninger fra reisverk til ferdig hus. 🔨 Den største faggruppen i bygg.",
        "verktoy": "Hammer, sag, kappsag, laser, drill, vinkel.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Tømrer -> Lærlingid.",
        "videre": "🎓 Mesterbrev, fagskole eller arkitekt.",
        "motivasjon": "🔨 Liker du å se et hus reise seg fra grunnen? Som tømrer skaper du trygge hjem for folk!",
        "quiz": ("Hva er standard c/c?", ["60 cm", "100 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "🛡️ Sikkerhet og kvalitet. 📋 Planlegge arbeidet for å unngå ulykker.",
        "verktoy": "SJA-skjemaer, sjekklister, verneutstyr.",
        "utdanning": "🛡️ Integrert i alle byggfag (HMS).",
        "videre": "🎓 HMS-leder, prosjektleder eller kvalitetssikrer.",
        "motivasjon": "⚠️ Vil du ha ansvar for at alle kommer trygt hjem? En god leder på plassen er gull verdt!",
        "quiz": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Hele Min Snekker"], "Helse, Miljø og Sikkerhet")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "🏢 Praksisperiode i bedrift. 🤝 Din sjanse til å få lærlingplass.",
        "verktoy": "Eget verneutstyr, loggbok og interesse.",
        "utdanning": "📈 En del av pensum på Vg1 og Vg2.",
        "videre": "🚀 Veien til fast jobb starter her.",
        "motivasjon": "🌟 Er du usikker? Bruk YFF til å teste flere fag før du bestemmer deg!",
        "quiz": ("Viktigst i praksis?", ["Oppmøte og interesse", "Kunne alt"], "Oppmøte og interesse")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fagområde:", list(data_db.keys()))
    f = data_db[sel_fag]
    st.subheader(f"📍 {sel_fag}")
    st.markdown(f"**Hva lærer man?**\n\n{f['beskrivelse']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛠️ Viktige verktøy")
        st.write(f["verktoy"])
    with col2:
        st.markdown("### 🎓 Utdanningsløp")
        st.write(f["utdanning"])
    
    st.success(f"**🚀 Videreutdanning:** {f['videre']}")
    st.info(f"💡 **Til deg som er usikker:** {f['motivasjon']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets – hvor langt det er rundt")
        st.write("Omkretsen er summen av alle sidene. Brukes til lister, gjerder eller grunnmursplast.")
        st.latex(r"Omkrets = S_1 + S_2 + S_3 + S_4")
        st.write("**Oppgave:** Et rom er 4m langt og 3m bredt. Hvor mange meter list trenger du?")
        ans1 = st.radio("Svar:", ["7m", "14m", "12m"], index=None, key="m1")
        if st.button("Sjekk Omkrets"):
            if ans1 == "14m":
                st.success("Riktig! (4+3+4+3)"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal – hvor mye plass noe tar ")
        st.write("Tenk deg at du skal legge gulv på et rom. Arealet sier hvor mange gulvplater som trengs. Enkelt forklart: Areal er hvor mye plass noe tar inni en form. Eksempel: Et teppe som er 4 meter langt og 3 meter bredt: 4 × 3 = 12 kvadratmeter. Det betyr at teppet dekker 12 ruter på 1 m × 1 m.")
        st.latex(r"Areal = L \times B")
        st.write("**Oppgave:** Du skal legge gulv i en bod på 2,5m x 4m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["6,5 m²", "10 m²", "8 m²"], index=None, key="m2")
        if st.button("Sjekk Areal"):
            if ans2 == "10 m²":
                st.success("Helt rett! 2,5 * 4 = 10 m²"); st.session_state.points += 5

    elif m_kat == "Prosent":
        st.write("### 📈 Prosent – deler av hundre")
        st.write("Prosent betyr “av hundre”. Tenk deg 100 godterier. Hvis du får 25 av dem, har du fått 25 %. Formel: Del ÷ helhet × 100. Vi legger ofte til svinn i materialkostnader (ofte 10% eller mer) fordi noe kappes bort. Formel: Gange med 1,10.")
        st.write("**Oppgave:** Du trenger 50 meter kledning. Med 10% svinn, hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["55m", "50,1m"], index=None, key="m3")
        if st.button("Sjekk Svinn"):
            if ans3 == "55m":
                st.success("Riktig! 50 + 5 = 55m."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("Målestokk 1:50 betyr at virkeligheten er 50 ganger større enn tegningen. Formel: Virkelig lengde = tegnet lengde × målestokk")
        st.write("**Oppgave:** På tegning (1:50) måler du 10cm. Hvor langt er det i virkeligheten?")
        ans4 = st.radio("Svar:", ["5 meter", "50 cm"], index=None, key="m4")
        if st.button("Sjekk Målestokk"):
            if ans4 == "5 meter":
                st.success("Riktig! 10cm * 50 = 5m."); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("For å sjekke 90 grader. Hvis sidene er 3 og 4, må diagonalen være 5.")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave:** Sidene er 60cm og 80cm. Hva er diagonalen i vinkel?")
        ans5 = st.radio("Svar:", ["100cm", "140cm"], index=None, key="m5")
        if st.button("Sjekk Vinkel"):
            if ans5 == "100cm":
                st.success("Vinkelen er 90 grader!"); st.session_state.points += 20; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()
        else:
            st.error("Feil svar, prøv igjen!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer"], "Poeng": [st.session_state.points, 400]}).sort_values("Poeng", ascending=False))


