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
    
    /* Hovedknapper */
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
        height: 3em;
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
if 'startet' not in st.session_state:
    st.session_state.startet = False

# --- FORSIDE (Vises før start) ---
if not st.session_state.startet:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    
    # Her simulerer vi det genererte bildet
    st.info("🔨 Din digitale assistent på byggeplassen")
    
    st.markdown("""
    ### Klar for å starte arbeidsdagen?
    Dette verktøyet hjelper deg med å bli trygg på byggeplassen. Vi skal gå gjennom:
    * **Verktøy og fagområder** for de 10 ulike retningene.
    * **Praktisk matte** som måling, areal og vinkler.
    * **Sikkerhet og HMS** så alle kommer trygt hjem.
    """)
    
    navn = st.text_input("Skriv navnet ditt her for å starte:", placeholder="Ditt navn...")
    
    if st.button("🚀 GÅ VIDERE TIL TRENING"):
        if navn:
            st.session_state.user_name = navn
            st.session_state.startet = True
            st.rerun()
        else:
            st.warning("Vennligst skriv inn navnet ditt først.")
    st.stop()

# --- TOPP-RAD (Vises etter start) ---
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
        "beskrivelse": "🌱 Bygger og vedlikeholder uterom, parker og hager. 🧱 Kombinerer levende planter med stein, betong og tre. [cite: 9, 10]",
        "verktoy": "Vater, murersnor, steinkutter, gravemaskin. [cite: 10]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsgartner -> 2 år lærlingtid. [cite: 10]",
        "videre": "🎓 Fagskole, mesterbrev eller landskapsarkitektur. [cite: 10]",
        "motivasjon": "✨ Liker du å se resultater som vokser? Her setter du spor folk vil nyte i generasjoner! [cite: 10, 11]",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 Betjener store maskiner for veibygging, tunneler og utgraving. 🏗️ Legger grunnlaget for samfunnet. [cite: 11, 12]",
        "verktoy": "Gravemaskiner, hjullastere, dumper, GPS-måleutstyr. [cite: 12]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling. [cite: 12]",
        "videre": "🎓 Maskinentreprenørskolen, fagskole eller ingeniør. [cite: 12]",
        "motivasjon": "💪 Fascinert av store krefter? Her får du flytte fjell og bygge veiene som binder landet sammen! [cite: 12, 13]",
        "quiz": ("Hva er påbudt i grøft?", ["Hjelm og vernesko", "Joggesko"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "beskrivelse": "🏢 Bygger solide konstruksjoner i betong og stein. 🏗️ Fra grunnmurer til store bruer. [cite: 13, 14]",
        "verktoy": "Forskalingsutstyr, blandemaskin, murerkjei, vater. [cite: 14]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Betong og mur -> Lærling. [cite: 14]",
        "videre": "🎓 Mesterbrev, fagskole eller byggeteknikk. [cite: 14]",
        "motivasjon": "🧱 Vil du bygge noe som står i 100 år? Du er arkitektens høyre hånd i å forme bybildet! [cite: 14, 15]",
        "quiz": ("Hvorfor armere betong?", ["Øke strekkfasthet", "For fargen"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "🌡️ Spesialister på inneklima og moderne energisparing. ❄️ Ventilasjon, varme og sanitet. [cite: 15, 16]",
        "verktoy": "Måleinstrumenter, loddeutstyr, blikkenslagersaks. [cite: 16]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Klima, energi og miljøteknikk -> Lærlingid. [cite: 16]",
        "videre": "🎓 KEM-ingeniør, fagskole eller energi-spesialisering. [cite: 16]",
        "motivasjon": "🌍 Vil du ha en nøkkelrolle i det grønne skiftet? Her jobber du med teknologien som redder klimaet! [cite: 16, 17]",
        "quiz": ("Hvorfor isolerer vi bygg?", ["Spare energi", "For tyngden"], "Spare energi")
    },
    "Overflateteknikk": {
        "beskrivelse": "🎨 Beskytter og dekorerer bygg utvendig og innvendig. 🖌️ Maling, tapet og gulvlegging. [cite: 17, 18]",
        "verktoy": "Sparkel, pensler, slipemaskin, malerulle. [cite: 18]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid. [cite: 18]",
        "videre": "🎓 Mesterbrev, interiørdesign eller fargekonsulent. [cite: 18]",
        "motivasjon": "🌈 Er du kreativ? Her setter du den siste finishen som kunden faktisk ser hver dag! [cite: 18, 19]",
        "quiz": ("Hva gjøres før maling?", ["Vaske og fjerne støv", "Male rett på"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "beskrivelse": "🚿 Installerer vann, varme og avløpssystemer. 🛠️ Viktig rolle i boliger og industri. [cite: 19, 20]",
        "verktoy": "Rørkutter, rørnøkkel, trykkpumpe. [cite: 20]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid. [cite: 20]",
        "videre": "🎓 Fagskole (VVS), mesterbrev eller ingeniør. [cite: 20]",
        "motivasjon": "💧 Ingen bygg fungerer uten rørleggeren. Vil du ha en sikker jobb med varierte utfordringer? [cite: 20, 21]",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vann"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "beskrivelse": "🏭 Industriell produksjon med tre som råstoff. ⚙️ Høyteknologisk produksjon av takstoler, vinduer og dører. [cite: 21, 22]",
        "verktoy": "CNC-maskiner, automatiske sager, limpresser. [cite: 22]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid. [cite: 22]",
        "videre": "🎓 Fagskole, produksjonsledelse eller ingeniør. [cite: 22]",
        "motivasjon": "🌲 Trives du best med maskiner og fabrikkdrift? Her skaper du fremtidens bærekraftige byggeklosser! [cite: 22, 23]",
        "quiz": ("Hvilken tresort brukes mest til reisverk?", ["Gran", "Eik"], "Gran")
    },
    "Tømrer": {
        "beskrivelse": "🏠 Oppføring av trebygninger fra reisverk til ferdig hus. 🔨 Den største faggruppen i bygg. [cite: 23, 24]",
        "verktoy": "Hammer, sag, kappsag, laser, drill, vinkel. [cite: 24]",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Tømrer -> Lærlingid. [cite: 24]",
        "videre": "🎓 Mesterbrev, fagskole eller arkitekt. [cite: 24]",
        "motivasjon": "🔨 Liker du å se et hus reise seg fra grunnen? Som tømrer skaper du trygge hjem for folk! [cite: 24, 25]",
        "quiz": ("Hva er standard c/c på stendere?", ["60 cm", "100 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "🛡️ Sikkerhet og kvalitet. 📋 Planlegge arbeidet for å unngå ulykker. [cite: 25, 26]",
        "verktoy": "SJA-skjemaer, sjekklister, verneutstyr. [cite: 26]",
        "utdanning": "🛡️ Integrert i alle byggfag (HMS). [cite: 26]",
        "videre": "🎓 HMS-leder, prosjektleder eller kvalitetssikrer. [cite: 26]",
        "motivasjon": "⚠️ Vil du ha ansvar for at alle kommer trygt hjem? En god leder på plassen er gull verdt! [cite: 26, 27]",
        "quiz": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Hele Min Snekker"], "Helse, Miljø og Sikkerhet")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "🏢 Praksisperiode i bedrift. 🤝 Din sjanse til å få lærlingplass. [cite: 27, 28]",
        "verktoy": "Eget verneutstyr, loggbok og interesse. [cite: 28]",
        "utdanning": "📈 En del av pensum på Vg1 og Vg2. [cite: 28]",
        "videre": "🚀 Veien til fast jobb starter her. [cite: 28]",
        "motivasjon": "🌟 Er du usikker? Bruk YFF til å teste flere fag før du bestemmer deg! [cite: 28, 29]",
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
    
    col_v, col_u = st.columns(2)
    with col_v:
        st.markdown("### 🛠️ Viktige verktøy")
        st.write(f["verktoy"])
    with col_u:
        st.markdown("### 🎓 Utdanningsløp")
        st.write(f["utdanning"])
    
    st.success(f"**🚀 Videreutdanning:** {f['videre']}")
    st.info(f"💡 **Til deg som er usikker:** {f['motivasjon']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Volum", "Prosent & Svinn", "Målestokk", "Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets – Hvor langt er det rundt?")
        st.write("Omkretsen er summen av alle sidene. [cite: 31, 32]")
        st.latex(r"Omkrets = S_1 + S_2 + S_3 + S_4")
        st.write("**Oppgave:** Et rom er 4m langt og 3m bredt. Hvor mange meter list trenger du?")
        ans1 = st.radio("Svar:", ["7m", "14m", "12m"], index=None, key="m1")
        if st.button("Sjekk Omkrets"):
            if ans1 == "14m":
                st.success("Riktig! (4+3+4+3)"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal – Hvor stor er en flate?")
        st.write("Areal forteller hvor stor en flate er ($m^2$). [cite: 33]")
        st.latex(r"Areal = L \times B")
        st.write("**Oppgave:** Du skal legge gulv i en bod på 2,5m x 4m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["6,5 m²", "10 m²", "8 m²"], index=None, key="m2")
        if st.button("Sjekk Areal"):
            if ans2 == "10 m²":
                st.success("Helt rett! 2,5 * 4 = 10 m²"); st.session_state.points += 5

    elif m_kat == "Volum":
        st.write("### 🧊 Volum – Innhold")
        st.write("Volum forteller hvor mye en gjenstand rommer ($m^3$). Brukes for å beregne betong. [cite: 35]")
        st.latex(r"Volum = L \times B \times H")
        st.write("**Oppgave:** En såle er 5m lang, 2m bred og 0,2m høy. Hvor mange m³ betong trenger du?")
        ans_vol = st.radio("Svar:", ["2,0 m³", "1,0 m³", "7,2 m³"], index=None, key="m_vol")
        if st.button("Sjekk Volum"):
            if ans_vol == "2,0 m³":
                st.success("Riktig! 5 * 2 * 0,2 = 2,0 m³."); st.session_state.points += 10

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("Vi legger til svinn (ofte 10%-15%) fordi noe kappes bort. [cite: 37, 38]")
        st.write("**Oppgave:** Du trenger 50 meter kledning. Med 10% svinn, hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["55m", "50,1m"], index=None, key="m3")
        if st.button("Sjekk Svinn"):
            if ans3 == "55m":
                st.success("Riktig! 50 + 5 = 55m."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("Målestokk 1:50 betyr at virkeligheten er 50 ganger større enn tegningen. [cite: 39]")
        st.write("**Oppgave:** På tegning (1:50) måler du 10cm. Hvor langt er det i virkeligheten?")
        ans4 = st.radio("Svar:", ["5 meter", "50 cm"], index=None, key="m4")
        if st.button("Sjekk Målestokk"):
            if ans4 == "5 meter":
                st.success("Riktig! 10cm * 50 = 5m."); st.session_state.points += 10

    elif m_kat == "Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("Hvis sidene er 3 og 4, må diagonalen være 5 for å sjekke 90 grader. [cite: 40, 41]")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave:** Sidene er 60cm og 80cm. Hva er diagonalen i vinkel?")
        ans5 = st.radio("Svar:", ["100cm", "140cm"], index=None, key="m5")
        if st.button("Sjekk Vinkel"):
            if ans5 == "100cm":
                st.success("Vinkelen er 90 grader!"); st.session_state.points += 20; st.balloons()

with tab_quiz:
    st.header("🎮 Quiz: Test kunnskapen")
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Ditt svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()
        else:
            st.error("Feil svar, prøv igjen!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer"], "Poeng": [st.session_state.points, 400]}).sort_values("Poeng", ascending=False))
