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
        user_prompt = st.chat_input("Spør om fag...")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar som en norsk byggmester. Kort og lærerikt."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except: st.error("AI-hjelper er utilgjengelig.")
        for m in st.session_state.messages[-2:]: st.write(f"🗨️ {m['content']}")

st.divider()

# --- UTVIDET DATABASE (10 PROGRAMFAG) ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "🌱 Bygger og vedlikeholder uterom, parker, hager og idrettsanlegg. 🧱 Du kombinerer levende materialer som planter med harde materialer som stein, betong og treverk. 🚜 Innebærer bruk av maskiner for å forme landskapet.",
        "oppgaver": "✨ Legge brostein og skifer, bygge murer, plante trær/busker og montere utstyr som lekeapparater.",
        "utdanning": "📜 Fagbrev som anleggsgartner etter Vg2 og 2 år lærlingtid. Gir mulighet for videreutdanning til fagskole eller mesterbrev.",
        "quiz": ("Hva er en sentral del av arbeidet som anleggsgartner?", ["Overvannshåndtering og drenering", "Sikre sikringsskap", "Tegne datachips"], "Overvannshåndtering og drenering")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 Betjener store maskiner for å bygge infrastruktur som veier, tunneler og baner. 🏗️ Legger grunnlaget for alle typer bygg- og anleggsprosjekter.",
        "oppgaver": "💥 Sprengningsarbeid, graving av grøfter for rør og kabler, og massetransport.",
        "utdanning": "📜 Fagbrev som anleggsmaskinfører, asfaltør eller fjell- og bergverksarbeider.",
        "quiz": ("Hva betyr det å utføre 'massetransport'?", ["Flytte stein, jord og pukk", "Bære murstein", "Kjøre verktøy"], "Flytte stein, jord og pukk")
    },
    "Betong og mur": {
        "beskrivelse": "🧱 Bygger solide konstruksjoner som tåler ekstreme laster. 🏢 Arbeider med alt fra grunnmur på eneboliger til store bruer og oljeplattformer.",
        "oppgaver": "🏗️ Forskaling, armering og støping av betong. Muring av vegger med tegl eller blokker.",
        "utdanning": "📜 Fagbrev i betongfaget eller murerfaget.",
        "quiz": ("Hva er 'forskaling'?", ["En form som holder betongen på plass", "Et lag med maling", "En type spiker"], "En form som holder betongen på plass")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "🌡️ Spesialister på inneklima og moderne energisparing. 💧 Sikrer at bygg er varme om vinteren, svale om sommeren og har frisk luft.",
        "oppgaver": "❄️ Montering av ventilasjon, varmepumper, kuldeanlegg og blikkenslagerarbeid på fasade.",
        "utdanning": "📜 Fagbrev som ventilasjons- og blikkenslager, kuldemontør eller isolatør.",
        "quiz": ("Hvorfor er ENØK (energiøkonomisering) viktig i dette faget?", ["For å redusere energibruk i bygg", "For å bygge raskere", "For utseendet"], "For å redusere energibruk i bygg")
    },
    "Overflateteknikk": {
        "beskrivelse": "🎨 Beskytter og dekorerer bygg utvendig og innvendig. 🛠️ Ekspert på grunnarbeid som sparkling og sliping for å få perfekt finish.",
        "oppgaver": "🖌️ Maling, tapetsering og legging av ulike typer gulv (belegg, teppe, herdeplast).",
        "utdanning": "📜 Fagbrev som maler eller gulvlegger.",
        "quiz": ("Hvorfor må man sparkle skjøter på gipsplater før maling?", ["For å få en jevn og slett overflate", "For å lime platene sammen", "For brannsikring"], "For å få en jevn og slett overflate")
    },
    "Rørlegger": {
        "beskrivelse": "🚿 Installerer vann, avløp og varmeanlegg. ⚡ Viktig rolle i det grønne skiftet med montering av vannbåren varme.",
        "oppgaver": "🛠️ Montering av sanitærutstyr, sprinkelanlegg og utvendig ledningsnett.",
        "utdanning": "📜 Svennebrev som rørlegger.",
        "quiz": ("Hva er hovedoppgaven til et sprinkelanlegg?", ["Brannslokking", "Vanning av blomster", "Kjøling"], "Brannslokking")
    },
    "Treteknikk": {
        "beskrivelse": "🪑 Industriell produksjon med tre som råstoff. ⚙️ Du bruker høyteknologiske maskiner til å produsere elementer til byggemarkedet.",
        "oppgaver": "🏭 Betjene CNC-freser, høvler og sager. Produsere takstoler, vinduer og dører.",
        "utdanning": "📜 Fagbrev som trelastoperatør eller i trevare- og møbelfaget.",
        "quiz": ("Hva kjennetegner industriell treteknikk?", ["Masseproduksjon med maskiner", "Håndspikring av hus", "Muring"], "Masseproduksjon med maskiner")
    },
    "Tømrer": {
        "beskrivelse": "🏠 Oppføring av trekonstruksjoner. 🔨 Den største faggruppen som følger bygget fra reisverk til ferdigstillelse.",
        "oppgaver": "📐 Montere stendere, bjelkelag, taksperrer, vinduer og dører.",
        "utdanning": "📜 Svennebrev som tømrer.",
        "quiz": ("Hva kaller vi de stående stenderne i en vegg?", ["Reisverk/Bindingsverk", "Grunnmur", "Listverk"], "Reisverk/Bindingsverk")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "⚠️ Sikkerhet og kvalitet. 📋 Handler om å følge lover og regler for å unngå ulykker og sikre at kunden får det de betaler for.",
        "oppgaver": "📝 Utføre risikovurdering, bruke verneutstyr og skrive logg.",
        "utdanning": "🛡️ En obligatorisk del av alle fagområder (HMS).",
        "quiz": ("Hvem har ansvaret for å bruke personlig verneutstyr (PVU)?", ["Den enkelte arbeidstaker", "Bare læreren", "Borgermesteren"], "Den enkelte arbeidstaker")
    },
    "Yrkesfaglig fordypning (YFF)": {
        "beskrivelse": "🏢 Praksisperiode der du får prøve deg i en bedrift. 🤝 Dette er din sjanse til å få lærlingplass.",
        "oppgaver": "👷 Delta i daglig drift på en ekte byggeplass under veiledning.",
        "utdanning": "📈 En del av læreplanen på Vg1 og Vg2.",
        "quiz": ("Hva er lurt å gjøre hvis du er ferdig med en oppgave i praksis?", ["Spørre etter en ny oppgave", "Sette seg på telefonen", "Gå hjem"], "Spørre etter en ny oppgave")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg område:", list(data_db.keys()))
    f = data_db[sel_fag]
    st.subheader(f"📍 {sel_fag}")
    st.markdown(f"**Hva lærer man?**\n\n{f['beskrivelse']}")
    st.markdown(f"**Typiske arbeidsoppgaver:**\n\n{f['oppgaver']}")
    st.success(f"**Utdanningsvei:** {f['utdanning']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.subheader("📏 Omkrets - Lengden rundt")
        st.write("Omkretsen er summen av alle sidene i en figur. I byggfag bruker vi dette når vi skal beregne lengden på lister, gjerder eller grunnmursplast.")
        st.latex(r"Omkrets = S_1 + S_2 + S_3 + S_4")
        st.write("💡 **Tips:** Se for deg at du går en tur langs kanten av rommet. Hvor langt har du gått når du er tilbake til start?")
        st.write("**Oppgave:** Du skal legge fotlister i en bod som er 4 meter lang og 2,5 meter bred. Hvor mange meter list trenger du (se bort fra døråpning)?")
        ans1 = st.radio("Svar:", ["6,5m", "13m", "10m"], index=None, key="omk_q")
        if st.button("Sjekk Omkrets"):
            if ans1 == "13m": st.success("Helt korrekt! (4 + 2,5 + 4 + 2,5)"); st.session_state.points += 5
    
    elif m_kat == "Areal":
        st.subheader("⬛ Areal - Overflaten")
        st.write("Arealet forteller hvor stor en flate er i kvadratmeter ($m^2$). Vi bruker dette for å beregne mengden maling, parkett, gipsplater eller belegningsstein.")
        st.latex(r"Areal (m^2) = Lengde \times Bredde")
        

[Image of area calculation for a rectangle]

        st.write("💡 **Tips:** Hvis du har et rom på 3m x 3m, betyr arealet at du kan tegne ni firkanter på 1x1 meter på gulvet.")
        st.write("**Oppgave:** En terrasse skal dekkes med bord. Terrassen er 6 meter bred og 4 meter dyp. Hva er arealet?")
        ans2 = st.radio("Svar:", ["10 m²", "24 m²", "20 m²"], index=None, key="areal_q")
        if st.button("Sjekk Areal"):
            if ans2 == "24 m²": st.success("Riktig! 6 * 4 = 24"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.subheader("📈 Prosent og Svinn")
        st.write("I byggfag må vi alltid beregne 'svinn'. Det er ekstra materialer vi bestiller fordi vi kapper bort biter eller noe blir ødelagt. Standard svinn er ofte 10%.")
        st.write("💡 **Slik regner du 10%:** Del tallet på 10. (F.eks: 10% av 500 er 50).")
        st.write("**Oppgave:** Du har regnet ut at du trenger nøyaktig 60 meter kledning. Læreren ber deg legge til 10% svinn. Hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["66m", "61m", "70m"], index=None, key="pro_q")
        if st.button("Sjekk Svinn"):
            if ans3 == "66m": st.success("Riktig! 60m + 6m = 66m."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.subheader("🗺️ Målestokk - Fra papir til bygg")
        st.write("Målestokk 1:50 betyr at virkeligheten er 50 ganger større enn tegningen. 1:100 betyr at den er 100 ganger større.")
        st.write("📐 **Huskeregel:** 1 cm på tegningen i 1:100 er nøyaktig 1 meter i virkeligheten.")
        
        st.write("**Oppgave:** På en tegning i målestokk 1:50 måler du en vegg til 8 cm. Hvor lang er veggen i virkeligheten?")
        ans4 = st.radio("Svar:", ["4 meter", "40 cm", "8 meter"], index=None, key="mal_q")
        if st.button("Sjekk Målestokk"):
            if ans4 == "4 meter": st.success("Riktig! 8cm * 50 = 400cm = 4m."); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.subheader("📐 Pytagoras - 3-4-5 regelen")
        st.write("For å sjekke om et hjørne på en grunnmur eller et bygg er nøyaktig 90 grader, bruker vi Pytagoras' læresetning. Den enkleste måten er 3-4-5 regelen.")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("💡 **I praksis:** Mål 3 meter ut på den ene siden, og 4 meter ut på den andre. Hvis diagonalen i mellom er nøyaktig 5 meter, er vinkelen perfekt!")
        
        st.write("**Oppgave:** Du skal sette ut vinkelen til en garasje. Du måler opp 30 cm og 40 cm langs veggene. Hva skal diagonalen være for at vinkelen er 90 grader?")
        ans5 = st.radio("Svar:", ["50 cm", "70 cm", "100 cm"], index=None, key="pyt_q")
        if st.button("Sjekk Vinkel"):
            if ans5 == "50 cm": st.success("Helt rett! Dette fungerer uansett om det er cm eller meter."); st.session_state.points += 20; st.balloons()

with tab_quiz:
    st.header("🎮 Quiz: Test kunnskapen")
    q_fag = st.selectbox("Velg tema for quiz:", list(data_db.keys()), key="q_sel")
    spm, valg, svar = data_db[q_fag]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Ditt svar:", valg, index=None)
    if st.button("Sjekk Quiz-svar"):
        if res == svar:
            st.success("Riktig! +20 poeng"); st.session_state.points += 20; st.balloons(); st.rerun()
        else: st.error("Feil svar, sjekk infokanalen og prøv igjen!")

with tab_leader:
    st.write("### Toppliste")
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Demo-elev"], "Poeng": [st.session_state.points, 350]}).sort_values("Poeng", ascending=False))
