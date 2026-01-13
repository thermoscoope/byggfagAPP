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

# --- DATABASE FOR ALLE 10 TEMAER (Basert på vilbli.no) ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "🌱 Bygger og vedlikeholder uterom, parker og hager. Kombinerer levende planter med stein, betong og tre.",
        "verktoy": "Vater, murersnor, steinkutter, lasere, mindre gravemaskiner.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingtid.",
        "videre": "🎓 Fagskole, mesterbrev eller landskapsarkitektur.",
        "motivasjon": "✨ Liker du å se resultater som vokser og blir vakrere med årene? Her setter du spor folk vil nyte i generasjoner!",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 Betjener store maskiner for veibygging, tunneler og utgraving. Legger grunnlaget for samfunnet.",
        "verktoy": "Gravemaskiner, hjullastere, dumpere, GPS-måleutstyr.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling.",
        "videre": "🎓 Maskinentreprenørskolen, fagskole eller ingeniør.",
        "motivasjon": "💪 Fascinert av store krefter? Her får du flytte fjell og bygge veiene som binder landet sammen!",
        "quiz": ("Hvilken maskin brukes til komprimering?", ["Valse/vibrasjonsplate", "Motorsag"], "Valse/vibrasjonsplate")
    },
    "Betong og mur": {
        "beskrivelse": "🏢 Bygger solide konstruksjoner i betong og stein. Fra små grunnmurer til gigantiske bruer.",
        "verktoy": "Forskalingsutstyr, blandemaskin, murerkjei, laser.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Betong og mur -> Lærling.",
        "videre": "🎓 Mesterbrev, fagskole eller byggeteknikk.",
        "motivasjon": "🧱 Vil du bygge noe som står i 100 år? Du er arkitektens høyre hånd i å forme bybildet!",
        "quiz": ("Hvorfor armere betong?", ["Øke strekkfasthet", "For fargen"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "🌡️ Spesialister på inneklima og moderne energisparing. Jobber med ventilasjon og varme.",
        "verktoy": "Måleinstrumenter, loddeutstyr, blikkenslagersaks.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 KEM -> Lærling.",
        "videre": "🎓 KEM-ingeniør, fagskole eller fornybar energi.",
        "motivasjon": "🌍 Vil du ha en nøkkelrolle i det grønne skiftet? Her redder du klimaet, ett bygg om gangen!",
        "quiz": ("Hva er hovedmålet med ventilasjon?", ["God luftkvalitet", "Gjøre rommet lysere"], "God luftkvalitet")
    },
    "Overflateteknikk": {
        "beskrivelse": "🎨 Beskytter og dekorerer bygg utvendig og innvendig. Maling, tapet og gulv.",
        "verktoy": "Sparkel, pensler, slipemaskiner, malerulle.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Overflate -> Lærling.",
        "videre": "🎓 Mesterbrev, interiørdesign eller fargekonsulent.",
        "motivasjon": "🌈 Er du kreativ? Her setter du finishen som kunden ser og tar på hver dag!",
        "quiz": ("Hva gjøres før maling?", ["Vaske og fjerne støv", "Male rett på"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "beskrivelse": "🚿 Installerer vann, varme og avløp. En viktig brikke i alle moderne bygg.",
        "verktoy": "Rørkutter, rørnøkkel, trykkpumpe, varmekamera.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Rørlegger -> Lærling.",
        "videre": "🎓 Fagskole (VVS), mesterbrev eller ingeniør.",
        "motivasjon": "💧 Ingen bygg fungerer uten deg. En sikker jobb med enorme variasjonsmuligheter!",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vann"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "🏭 Industriell produksjon med tre. Bruker høyteknologiske maskiner til å lage bygningsdeler.",
        "verktoy": "CNC-maskiner, automatiske sager, limpresser.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Treteknikk -> Lærling.",
        "videre": "🎓 Fagskole, produksjonsledelse eller ingeniør.",
        "motivasjon": "🌲 Liker du tre og maskiner? Her skaper du fremtidens bærekraftige byggeklosser!",
        "quiz": ("Hva kjennetegner limtre?", ["Lagvis limt for styrke", "Malt hvit"], "Lagvis limt for styrke")
    },
    "Tømrer": {
        "beskrivelse": "🏠 Oppføring av trebygninger fra reisverk til ferdig hus. Den største gruppen i byggfag.",
        "verktoy": "Hammer, sag, kappsag, laser, vinkel.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Tømrer -> Lærling.",
        "videre": "🎓 Mesterbrev, fagskole eller arkitekt.",
        "motivasjon": "🔨 Liker du å se et hus reise seg? Som tømrer skaper du trygge hjem for folk!",
        "quiz": ("Hva er standard c/c på stendere?", ["60 cm", "100 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "🛡️ Sikkerhet og kvalitet. Handler om HMS og å sikre at ingen blir skadet på jobb.",
        "verktoy": "SJA-skjemaer, digitale logger, verneutstyr.",
        "utdanning": "🛡️ Obligatorisk del av alle fagene.",
        "videre": "🎓 HMS-leder eller prosjektleder.",
        "motivasjon": "⚠️ Vil du ha ansvar for at alle kommer trygt hjem? En god leder på plassen er gull verdt!",
        "quiz": ("Hva står SJA for?", ["Sikker jobb-analyse", "Snekker-avtale"], "Sikker jobb-analyse")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "🏢 Praksisperiode i bedrift. Din viktigste sjanse til å få lærlingplass.",
        "verktoy": "Eget verneutstyr, loggbok og nysgjerrighet.",
        "utdanning": "📈 Del av pensum på Vg1 og Vg2.",
        "videre": "🚀 Broen inn til fast jobb.",
        "motivasjon": "🌟 Usikker? Bruk YFF til å teste flere fag før du låser deg til én retning!",
        "quiz": ("Viktigst i praksis?", ["Holdninger og oppmøte", "Eget verktøy"], "Holdninger og oppmøte")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fagområde:", list(data_db.keys()))
    f = data_db[sel_fag]
    st.subheader(f"📍 {sel_fag}")
    st.markdown(f"**Hva gjør man?**\n\n{f['beskrivelse']}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛠️ Viktige verktøy")
        st.write(f["verktoy"])
    with col2:
        st.markdown("### 🎓 Utdanningsløp")
        st.write(f["utdanning"])
    st.success(f"**🚀 Videreutdanning:** {f['videre']}")
    st.info(f"💡 **Tips:** {f['motivasjon']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Volum", "Prosent & Svinn", "Målestokk", "Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets – Veien rundt")
        st.write("Omkrets er summen av alle sidene. Brukes til å beregne lister eller gjerder.")
        st.latex(r"Omkrets = S_1 + S_2 + S_3 + S_4")
        st.write("**Oppgave:** Et rom er 5m langt og 4m bredt. Hvor mye list går med?")
        ans1 = st.radio("Svar:", ["9m", "18m", "20m"], index=None, key="m1")
        if st.button("Sjekk Omkrets"):
            if ans1 == "18m":
                st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal – Flateberegning")
        st.write("Areal (m²) er Lengde x Bredde. Brukes for å kjøpe parkett, maling eller gips.")
        

[Image of area calculation for a rectangle]

        st.latex(r"A = L \times B")
        st.write("**Oppgave:** Du skal legge gips i et tak på 3m x 4m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["7m²", "12m²", "10m²"], index=None, key="m2")
        if st.button("Sjekk Areal"):
            if ans2 == "12m²":
                st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Volum":
        st.write("### 🧊 Volum – Innhold")
        st.write("Volum (m³) er Lengde x Bredde x Høyde. Brukes for å bestille betong.")
        

[Image of volume calculation for a rectangular prism]

        st.latex(r"V = L \times B \times H")
        st.write("**Oppgave:** En såle er 5m lang, 2m bred og 0,2m høy. Hvor mye betong?")
        ans_v = st.radio("Svar:", ["1m³", "2m³", "7m³"], index=None, key="mv")
        if st.button("Sjekk Volum"):
            if ans_v == "2m³":
                st.success("Riktig! 5 * 2 * 0,2 = 2"); st.session_state.points += 10

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("Legg til 10% svinn ved å gange med 1,10.")
        st.write("**Oppgave:** Du trenger 60m panel. Hvor mye bestiller du med 10% svinn?")
        ans3 = st.radio("Svar:", ["66m", "60,1m"], index=None, key="m3")
        if st.button("Sjekk Svinn"):
            if ans3 == "66m":
                st.success("Riktig!"); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("1:50 betyr at virkeligheten er 50 ganger større enn tegningen.")
        st.write("**Oppgave:** 10cm på tegning (1:50). Hvor langt er det i virkeligheten?")
        ans4 = st.radio("Svar:", ["5 meter", "50 cm"], index=None, key="m4")
        if st.button("Sjekk Målestokk"):
            if ans4 == "5 meter":
                st.success("Riktig! 10 * 50 = 500cm = 5m"); st.session_state.points += 10

    elif m_kat == "Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("Hvis sidene er 3 og 4, må diagonalen være 5 for å ha 90 grader.")
        
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave:** Sidene er 60cm og 80cm. Hva må diagonalen være?")
        ans5 = st.radio("Svar:", ["100cm", "140cm"], index=None, key="m5")
        if st.button("Sjekk Vinkel"):
            if ans5 == "100cm":
                st.success("Riktig!"); st.session_state.points += 15; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg tema for quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz-svar"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()
        else:
            st.error("Feil, prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]}).sort_values("Poeng", ascending=False))
