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
    }
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisering
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Ditt navn:")
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
        user_prompt = st.chat_input("Spør om byggfag...")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar som en erfaren norsk byggmester. Kort og lærerikt."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except: st.error("AI-hjelper er utilgjengelig.")
        for m in st.session_state.messages[-2:]: st.write(f"🗨️ {m['content']}")

st.divider()

# --- KOMPLETT DATABASE FOR ALLE 10 PROGRAMOMRÅDER ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "Bygger og vedlikeholder uterom, parker og hager. Bruker stein, planter og treverk.",
        "verktoy": "Murersnor, laser, steinkutter, vibrasjonsplate.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsgartner -> Lærlingid.",
        "quiz": ("Hva er hovedoppgaven til en anleggsgartner?", ["Bygge uterom og parker", "Male hus", "Installere rør"], "Bygge uterom og parker")
    },
    "Anleggsteknikk": {
        "beskrivelse": "Graving, veibygging og tunnelarbeid. Fokus på store maskiner og infrastruktur.",
        "verktoy": "Gravemaskin, dumper, hjullaster, nivelleringsutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærlingid.",
        "quiz": ("Hvilken maskin brukes mest til å flytte store mengder løsmasse?", ["Dumper", "Hammer", "Pensel"], "Dumper")
    },
    "Betong og mur": {
        "beskrivelse": "Konstruksjon i betong, tegl og naturstein. Fra grunnmur til ferdige bygg.",
        "verktoy": "Forskalingsutstyr, murerkjei, blandemaskin, vater.",
        "utdanning": "Vg1 Bygg -> Vg2 Betong og mur -> Lærlingid.",
        "quiz": ("Hvorfor må betong herde under plast hvis det er veldig varmt?", ["For å ikke tørke for fort", "For å bli blank", "For å endre farge"], "For å ikke tørke for fort")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "Inneklima, ventilasjon og energisparing i moderne bygg.",
        "verktoy": "Måleinstrumenter, loddeutstyr, isolasjonsverktøy.",
        "utdanning": "Vg1 Bygg -> Vg2 Klima, energi og miljøteknikk -> Lærlingid.",
        "quiz": ("Hva er viktigst for et godt inneklima?", ["Ventilasjon og luftutskifting", "Maling", "Tykke vegger"], "Ventilasjon og luftutskifting")
    },
    "Overflateteknikk": {
        "beskrivelse": "Maling, tapetsering og gulvlegging. Beskytter og dekorerer bygg.",
        "verktoy": "Sparkel, pensler, slipemaskin, malerulle.",
        "utdanning": "Vg1 Bygg -> Vg2 Overflateteknikk -> Lærlingid.",
        "quiz": ("Hvorfor bruker man grunning på nytt treverk?", ["For å gi bedre heft til malingen", "For å spare maling", "For lukten"], "For å gi bedre heft til malingen")
    },
    "Rørlegger": {
        "beskrivelse": "Installasjon av vann, varme og sanitæranlegg i boliger og industri.",
        "verktoy": "Rørkutter, rørnøkkel, trykkpumpe, loddeutstyr.",
        "utdanning": "Vg1 Bygg -> Vg2 Rørlegger -> Lærlingid.",
        "quiz": ("Hva brukes en trykkpumpe til?", ["Sjekke for lekkasjer i rør", "Rense rørene", "Kutte rør"], "Sjekke for lekkasjer i rør")
    },
    "Treteknikk": {
        "beskrivelse": "Industriell bearbeiding av treverk til ferdige produkter som limtre og vinduer.",
        "verktoy": "CNC-maskiner, høvler, sager, limpresser.",
        "utdanning": "Vg1 Bygg -> Vg2 Treteknikk -> Lærlingid.",
        "quiz": ("Hva kalles treverk som er limt sammen for å tåle store laster?", ["Limtre", "Spon", "Finer"], "Limtre")
    },
    "Tømrer": {
        "beskrivelse": "Oppføring av trebygninger. Reisverk, kledning, tak og interiør.",
        "verktoy": "Hammer, sag, laser, drill, vinkel.",
        "utdanning": "Vg1 Bygg -> Vg2 Tømrer -> Lærlingid.",
        "quiz": ("Hva betyr det at stenderne står 'c/c 60'?", ["60 cm fra senter til senter", "60 cm lang", "60 stk totalt"], "60 cm fra senter til senter")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "Fokus på HMS, sjekklister og sikkerhet på arbeidsplassen.",
        "verktoy": "SJA-skjemaer, verneplaner, hjelm og vernesko.",
        "utdanning": "Integrert i alle fagområder.",
        "quiz": ("Når skal en SJA (Sikker Jobb-analyse) utføres?", ["Før en risikofylt jobb starter", "Etter jobben", "Aldri"], "Før en risikofylt jobb starter")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "Praktisk utplassering i bedrift for å prøve ut ulike yrker.",
        "verktoy": "Arbeidsklær og egen interesse.",
        "utdanning": "En del av både Vg1 og Vg2.",
        "quiz": ("Hva er mest verdifullt for en lærling i praksis?", ["Være lærevillig og presis", "Eie dyrt verktøy", "Kunne alt fra før"], "Være lærevillig og presis")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om alle programfag")
    sel_fag = st.selectbox("Velg område:", list(data_db.keys()))
    f = data_db[sel_fag]
    st.subheader(f"📍 {sel_fag}")
    col_a, col_b = st.columns(2)
    with col_a: st.write(f"**Beskrivelse:** {f['beskrivelse']}")
    with col_b: st.write(f"**Viktig verktøy:** {f['verktoy']}")
    st.info(f"**Veien videre:** {f['utdanning']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.subheader("📏 Omkrets - Rundt figuren")
        st.write("Omkretsen er den totale lengden av alle sidene. Tenk deg at du skal legge en list langs gulvet i et rom. Da må du måle alle veggene og legge dem sammen.")
        st.latex(r"L + B + L + B = Omkrets")
        st.write("**Oppgave 1:** Et rom er 4m langt og 3m bredt. Hvor mange meter list går med?")
        ans1 = st.radio("Svar:", ["7m", "14m", "12m"], index=None, key="m1")
        if st.button("Sjekk 1"):
            if ans1 == "14m": st.success("Riktig! (4+3+4+3)"); st.session_state.points += 5
    
    elif m_kat == "Areal":
        st.subheader("⬛ Areal - Overflaten")
        st.write("Arealet forteller hvor stor en flate er i kvadratmeter (m²). Vi bruker dette for å beregne mengden maling, parkett eller gipsplater.")
        st.latex(r"Lengde \times Bredde = m^2")
        st.write("**Oppgave 2:** Du skal legge gulv i en bod som er 2,5m bred og 3m lang. Hvor mange m² gulv må du kjøpe?")
        ans2 = st.radio("Svar:", ["5,5 m²", "7,5 m²", "10 m²"], index=None, key="m2")
        if st.button("Sjekk 2"):
            if ans2 == "7,5 m²": st.success("Stemmer! 2,5 * 3 = 7,5"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.subheader("📈 Prosent og Svinn")
        st.write("I byggfag regner vi ofte 10% svinn. Det betyr at vi bestiller 10% ekstra fordi noe alltid kappes bort eller blir ødelagt.")
        st.write("**Oppgave 3:** Du trenger egentlig 50m² kledning, men må legge til 10% svinn. Hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["55 m²", "51 m²", "60 m²"], index=None, key="m3")
        if st.button("Sjekk 3"):
            if ans3 == "55 m²": st.success("Riktig! 10% av 50 er 5. 50 + 5 = 55."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.subheader("🗺️ Målestokk - Fra tegning til virkelighet")
        st.write("Målestokk 1:50 betyr at 1 cm på papiret er 50 cm i virkeligheten. For å finne virkelig lengde, ganger du tallet på linjalen med 50.")
        st.write("**Oppgave 4:** På en tegning i 1:100 måler du en vegg til 8cm. Hvor lang er den i virkeligheten?")
        ans4 = st.radio("Svar:", ["80 cm", "8 meter", "80 meter"], index=None, key="m4")
        if st.button("Sjekk 4"):
            if ans4 == "8 meter": st.success("Riktig! 8cm * 100 = 800cm = 8m."); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.subheader("📐 Pytagoras - Sjekk av rett vinkel")
        st.write("For å sjekke om et hjørne er 90 grader, bruker vi 3-4-5 metoden. Hvis de to sidene er 3 og 4 enheter, må diagonalen være nøyaktig 5.")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave 5:** Du måler 60cm på en vegg og 80cm på den andre. Hva må diagonalen være for at det skal være vinkel?")
        ans5 = st.radio("Svar:", ["100 cm", "120 cm", "150 cm"], index=None, key="m5")
        if st.button("Sjekk 5"):
            if ans5 == "100 cm": st.success("Perfekt! (Dette er 3-4-5 regelen doblet)"); st.session_state.points += 20; st.balloons()

with tab_quiz:
    st.header("🎮 Quiz: Test kunnskapen")
    q_fag = st.selectbox("Velg tema:", list(data_db.keys()), key="q_sel")
    spm, valg, svar = data_db[q_fag]["quiz"]
    st.write(f"### {spm}")
    bruker_svar = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz-svar"):
        if bruker_svar == svar:
            st.success("Riktig! +20 poeng"); st.session_state.points += 20; st.balloons(); st.rerun()
        else: st.error("Feil svar, prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]}).sort_values("Poeng", ascending=False))
