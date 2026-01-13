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
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Navn på elev:")
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
                    messages=[{"role": "system", "content": "Svar som en norsk byggmester. Kort og pedagogisk."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except: st.error("AI-hjelper er utilgjengelig.")
        for m in st.session_state.messages[-2:]: st.write(f"🗨️ {m['content']}")

st.divider()

# --- UTVIDET DATABASE (INFO, VERKTØY, UTDANNING OG MOTIVASJON) ---
data_db = {
    "Anleggsgartner": {
        "info": "🌱 **Hva lærer man?** Du lærer å skape vakre og funksjonelle uterom. Dette er faget for deg som trives ute og vil kombinere tekniske ferdigheter med levende natur.",
        "verktoy": "🧱 Belegningssteinutstyr, murersnor, vater, steinkutter, laser og mindre gravemaskiner.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Anleggsgartner -> 2 år lærlingtid.",
        "videre": "🎓 Fagskole (anleggsgartnertekniker), mesterbrev eller landskapsarkitektur via Y-veien.",
        "motivasjon": "✨ Liker du å se resultater som vokser og blir vakrere med årene? Som anleggsgartner setter du spor i miljøet som folk vil nyte i generasjoner!",
        "quiz": ("Hva er en sentral del av arbeidet som anleggsgartner?", ["Overvannshåndtering og drenering", "Montere sikringsskap"], "Overvannshåndtering og drenering")
    },
    "Anleggsteknikk": {
        "info": "🚜 **Hva lærer man?** Du lærer å betjene enorme maskiner og bygge fundamentet for samfunnet vårt: veier, tunneler og baner.",
        "verktoy": "🏗️ Gravemaskiner, hjullastere, dumpere, vals og avansert GPS-måleutstyr.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Anleggsteknikk -> Lærling i maskinførerfaget.",
        "videre": "🎓 Maskinentreprenørskolen, fagskole (anlegg) eller ingeniørstudier.",
        "motivasjon": "💪 Er du fascinert av store krefter og store maskiner? Her får du flytte fjell og bygge veiene som binder landet sammen!",
        "quiz": ("Hvilken maskin brukes til komprimering av masser?", ["Valse eller vibrasjonsplate", "Motorsag"], "Valse eller vibrasjonsplate")
    },
    "Betong og mur": {
        "info": "🏢 **Hva lærer man?** Du lærer å bygge de mest solide konstruksjonene vi har. Her handler det om styrke, presisjon og varighet.",
        "verktoy": "🏗️ Forskalingsutstyr, blandemaskin, murerkjei, vinkelsliper og laser.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Betong og mur -> Lærlingid.",
        "videre": "🎓 Mesterbrev (Murmester), fagskole eller byggeteknikk.",
        "motivasjon": "🧱 Vil du bygge noe som står i 100 år? Som murer eller betongarbeider er du arkitektens høyre hånd i å forme bybildet!",
        "quiz": ("Hvorfor legger man armeringsstål i betong?", ["For å øke strekkfastheten", "For fargen"], "For å øke strekkfastheten")
    },
    "Klima, energi og miljøteknikk": {
        "info": "🌡️ **Hva lærer man?** Fremtidens bygg må være miljøvennlige. Du lærer om ventilasjon, varme og tekniske løsninger som sparer energi.",
        "verktoy": "❄️ Måleinstrumenter for luft og temperatur, loddeutstyr, blikkenslagersaks og isolasjonsverktøy.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Klima, energi og miljøteknikk -> Lærlingid.",
        "videre": "🎓 KEM-ingeniør, fagskole eller spesialisering innen fornybar energi.",
        "motivasjon": "🌍 Vil du ha en nøkkelrolle i det grønne skiftet? Her jobber du med teknologien som redder klimaet, ett bygg om gangen!",
        "quiz": ("Hva er hovedformålet med ventilasjon?", ["God luftkvalitet og fjerning av fukt", "Gjøre rommet lysere"], "God luftkvalitet og fjerning av fukt")
    },
    "Overflateteknikk": {
        "info": "🎨 **Hva lærer man?** Du gir byggene sjel! Du lærer å beskytte materialer og skape vakre rom med maling, tapet og gulv.",
        "verktoy": "🖌️ Helsparklingsutstyr, sprøytemaler, avanserte gulvslipere og fargemålere.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Overflateteknikk -> Lærlingid.",
        "videre": "🎓 Mesterbrev (Malermester), interiørdesign eller fargekonsulent.",
        "motivasjon": "🌈 Er du kreativ og har øye for detaljer? Her er det du som setter den siste finishen som kunden faktisk ser og tar på hver dag!",
        "quiz": ("Hvorfor sparkle skjøter på gips?", ["Få slett overflate", "Lime platene"], "Få slett overflate")
    },
    "Rørlegger": {
        "info": "🚿 **Hva lærer man?** Vann er liv. Du lærer å installere kompliserte systemer for sanitær, varme og brannslokking.",
        "verktoy": "🛠️ Rørkuttere, trykktestingsutstyr, gjengeverktøy og varmekamera.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Rørlegger -> Lærlingid.",
        "videre": "🎓 Fagskole (VVS), mesterbrev eller rørleggeringeniør.",
        "motivasjon": "💧 Ingen bygg fungerer uten rørleggeren. Vil du ha en sikker jobb med varierte utfordringer i alt fra bad til storindustri?",
        "quiz": ("Hva gjør en vannlås?", ["Hindrer kloakklukt", "Renser vann"], "Hindrer kloakklukt")
    },
    "Treteknikk": {
        "info": "🏭 **Hva lærer man?** Du lærer moderne industriell produksjon av treelementer. Her møtes tradisjonelt treverk og høyteknologi.",
        "verktoy": "⚙️ CNC-maskiner, automatiske sager, limpresser og tegneprogrammer.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Treteknikk -> Lærlingid.",
        "videre": "🎓 Fagskole (treteknikk), produksjonsledelse eller ingeniør.",
        "motivasjon": "🌲 Liker du tre som materiale, men trives best med maskiner og fabrikkdrift? Her skaper du fremtidens bærekraftige byggeklosser!",
        "quiz": ("Hva er limtre?", ["Laminerte trelag for styrke", "Papir"], "Laminerte trelag for styrke")
    },
    "Tømrer": {
        "info": "🏠 **Hva lærer man?** Du er selve ryggraden i byggeprosjektet. Du lærer å bygge alt fra reisverk til detaljert listverk i tre.",
        "verktoy": "🔨 Hammer, sag, kappsag, laser, drill, vinkel og spikerpistol.",
        "utdanning": "📜 Vg1 Bygg- og anleggsteknikk -> Vg2 Tømrer -> Lærlingid.",
        "videre": "🎓 Mesterbrev (Tømrermester), fagskole (bygg) eller arkitekt.",
        "motivasjon": "🔨 Er du nevenyttig og liker å se et hus reise seg fra grunnen? Som tømrer skaper du trygge hjem for folk og får jobbe med hendene hver dag!",
        "quiz": ("Hva er standard c/c på stendere?", ["60 cm", "20 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "info": "🛡️ **Hva lærer man?** Du lærer hvordan man leder en trygg byggeplass. HMS og dokumentasjon er det som skiller amatøren fra den profesjonelle.",
        "verktoy": "📝 Sjekklister, digitale loggsystemer, SJA-verktøy og verneutstyr.",
        "utdanning": "🛡️ Integrert i alle byggfag (HMS-kort/Sertifisering).",
        "videre": "🎓 HMS-leder, prosjektleder eller kvalitetssikrer.",
        "motivasjon": "⚠️ Vil du ha ansvar for at alle kommer trygt hjem fra jobb? En god leder på byggeplassen er gull verdt for alle fagene!",
        "quiz": ("Hva står SJA for?", ["Sikker jobb-analyse", "Snekker-avtale"], "Sikker jobb-analyse")
    },
    "Yrkesfaglig fordypning": {
        "info": "🤝 **Hva lærer man?** Dette er din 'testkjøring' av arbeidslivet. Du lærer å samarbeide med profesjonelle og finne din plass.",
        "verktoy": "👷 Eget verneutstyr, loggbok og gode spørsmål til veilederen.",
        "utdanning": "📈 En del av pensum som fører rett til læreplass.",
        "videre": "🚀 Veien til fast jobb starter her.",
        "motivasjon": "🌟 Er du usikker? Bruk YFF til å teste flere fag! Dette er din sjanse til å 'smake' på yrket før du bestemmer deg for resten av livet.",
        "quiz": ("Viktigst i praksis?", ["Oppmøte og interesse", "Ny mobil"], "Oppmøte og interesse")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fag for å utforske:", list(data_db.keys()))
    st.subheader(f"📍 {sel_fag}")
    
    st.markdown(data_db[sel_fag]["info"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛠️ Viktige verktøy")
        st.write(data_db[sel_fag]["verktoy"])
    with col2:
        st.markdown("### 🎓 Utdanningsløp")
        st.write(data_db[sel_fag]["utdanning"])
    
    st.success(f"**🚀 Videreutdanning:** {data_db[sel_fag]['videre']}")
    
    st.info(f"💡 **Til deg som er usikker:** {data_db[sel_fag]['motivasjon']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets (Lengden rundt)")
        st.write("Bruk dette når du skal beregne lister langs gulvet eller gjerder.")
        st.latex(r"Formel: L + B + L + B")
        st.write("**Oppgave:** Et rom er 5m x 4m. Hvor mange meter list trenger du?")
        ans1 = st.radio("Svar:", ["9m", "18m", "20m"], index=None, key="m1")
        if st.button("Sjekk 1"):
            if ans1 == "18m": st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal (Overflaten)")
        st.write("Bruk dette for gulv, maling eller steinlegging.")
        st.latex(r"Formel: L \times B = m^2")
        

[Image of area calculation for a rectangle]

        st.write("**Oppgave:** Du skal legge gulv i en bod på 2,5m x 3m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["5,5 m²", "7,5 m²", "10 m²"], index=None, key="m2")
        if st.button("Sjekk 2"):
            if ans2 == "7,5 m²": st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("Vi legger til 10% svinn ved å gange behovet med 1,10.")
        st.write("**Oppgave:** Du trenger 80m kledning. Hvor mye bestiller du med 10% svinn?")
        ans3 = st.radio("Svar:", ["88m", "80,1m"], index=None, key="m3")
        if st.button("Sjekk 3"):
            if ans3 == "88m": st.success("Riktig!"); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("Målestokk 1:50 betyr at 1cm på tegningen er 50cm i virkeligheten.")
        st.write("**Oppgave:** På en tegning i 1:50 måler du 10cm. Hvor langt er det i virkeligheten?")
        ans4 = st.radio("Svar:", ["5 meter", "50 cm"], index=None, key="m4")
        if st.button("Sjekk 4"):
            if ans4 == "5 meter": st.success("Riktig! 10 * 50 = 500cm = 5m"); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("For å sjekke 90 grader. Hvis sidene er 3 og 4, må diagonalen være 5.")
        st.latex(r"a^2 + b^2 = c^2")
        
        st.write("**Oppgave:** Sidene er 60cm og 80cm. Hva er diagonalen i vinkel?")
        ans5 = st.radio("Svar:", ["100cm", "140cm"], index=None, key="m5")
        if st.button("Sjekk 5"):
            if ans5 == "100cm": st.success("Vinkelen er 90 grader!"); st.session_state.points += 20; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer"], "Poeng": [st.session_state.points, 400]}))
