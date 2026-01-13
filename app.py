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
    name = st.text_input("Ditt navn for loggen:")
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
                    messages=[{"role": "system", "content": "Svar kort som en norsk byggmester."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except: st.error("AI utilgjengelig.")
        for m in st.session_state.messages[-2:]: st.write(f"🗨️ {m['content']}")

st.divider()

# --- UTVIDET DATABASE (10 PROGRAMFAG) ---
data_db = {
    "Anleggsgartner": {
        "beskrivelse": "🌱 Bygger og vedlikeholder uterom. 🧱 Kombinerer levende materialer (planter) med harde materialer (stein/betong). 🚜 Bruker maskiner for å forme landskapet.",
        "oppgaver": "✨ Legge brostein, bygge murer, plante trær og montere lekeutstyr.",
        "utdanning": "📜 Fagbrev som anleggsgartner etter Vg2 og 2 år lærlingtid.",
        "quiz": ("Hva er en viktig del av jobben som anleggsgartner?", ["Drenering og overvannshåndtering", "Montere sikringsskap", "Tegne kretskort"], "Drenering og overvannshåndtering")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 Betjener store maskiner for graving, sprengning og veibygging. 🏗️ Legger grunnlaget for alt fra boligfelt til jernbane.",
        "oppgaver": "💥 Sprengningsarbeid, graving av grøfter, vegbygging og masseflytting.",
        "utdanning": "📜 Mulighet for fagbrev som maskinfører, asfaltør eller fjell- og bergverksarbeider.",
        "quiz": ("Hvilken maskin brukes til å komprimere løsmasser?", ["Valse/Vibrasjonsplate", "Motorsag", "Hammer"], "Valse/Vibrasjonsplate")
    },
    "Betong og mur": {
        "beskrivelse": "🧱 Bygger solide konstruksjoner som tåler ekstreme laster. 🏢 Arbeider med forskaling, armering og muring av vegger.",
        "oppgaver": "🏗️ Støpe grunnmurer, mure fasader og sette opp elementbygg.",
        "utdanning": "📜 Fagbrev i betongfaget eller murerfaget.",
        "quiz": ("Hvorfor legger man stål (armering) inn i betongen?", ["For å øke strekkfastheten", "For fargen", "For å spare sement"], "For å øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "beskrivelse": "🌡️ Spesialister på inneklima og energiløsninger. 💧 Sikrer at bygg har riktig varme, ventilasjon og sanitet.",
        "oppgaver": "❄️ Montere varmepumper, ventilasjon og styringssystemer.",
        "utdanning": "📜 Fagbrev som ventilasjons- og blikkenslager eller kuldemontør.",
        "quiz": ("Hva er hovedformålet med ventilasjon?", ["Sikre god luftkvalitet", "Gjøre rommet lysere", "Øke lyden"], "Sikre god luftkvalitet")
    },
    "Overflateteknikk": {
        "beskrivelse": "🎨 Beskytter og dekorerer bygg utvendig og innvendig. 🛠️ Ekspert på grunnarbeid, maling, tapet og gulv.",
        "oppgaver": "🖌️ Helsparkling, sprøytemaling, legging av industrigulv.",
        "utdanning": "📜 Fagbrev som maler eller gulvlegger.",
        "quiz": ("Hvorfor er forarbeid (sliping/vask) så viktig?", ["For å sikre god heft for malingen", "For å bruke mer tid", "For å lage støv"], "For å sikre god heft for malingen")
    },
    "Rørlegger": {
        "beskrivelse": "🚿 Legger vann og avløp i alle typer bygg. ⚡ Arbeider med moderne varmesystemer og sprinkelanlegg.",
        "oppgaver": "🛠️ Montere bad, koble til varmepumper og legge utvendig VA.",
        "utdanning": "📜 Fagbrev som rørlegger.",
        "quiz": ("Hva brukes et rør-i-rør system til?", ["Sikre mot vannskader", "Øke lydnivået", "Varme opp huset"], "Sikre mot vannskader")
    },
    "Treteknikk": {
        "beskrivelse": "🪑 Industriell produksjon av treprodukter. ⚙️ Bruker avanserte maskiner til å lage alt fra dører til takstoler.",
        "oppgaver": "🏭 Betjene CNC-maskiner og produsere treelementer.",
        "utdanning": "📜 Fagbrev som trelastoperatør eller i trevare- og møbelfaget.",
        "quiz": ("Hva kalles det når man limer tynne trelag sammen til sterke bjelker?", ["Limtre", "Sponplate", "Gips"], "Limtre")
    },
    "Tømrer": {
        "beskrivelse": "🏠 Den mest kjente byggherren. 🔨 Bygger reisverk, monterer vinduer og ferdigstiller hus.",
        "oppgaver": "📐 Konstruksjon av tak, vegger og innredning i tre.",
        "utdanning": "📜 Svennebrev som tømrer.",
        "quiz": ("Hvilken avstand er standard mellom stendere i en vegg?", ["60 cm (c/c 60)", "100 cm", "20 cm"], "60 cm (c/c 60)")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "beskrivelse": "⚠️ Sikkerhet først! 📋 Handler om å planlegge arbeidet slik at ingen blir skadet.",
        "oppgaver": "📝 Utføre SJA, bruke verneutstyr og dokumentere avvik.",
        "utdanning": "🛡️ En obligatorisk del av alle byggfag.",
        "quiz": ("Hva skal du gjøre hvis du ser en farlig situasjon?", ["Melde fra og stoppe arbeidet", "Ignorere det", "Gå hjem"], "Melde fra og stoppe arbeidet")
    },
    "Yrkesfaglig fordypning": {
        "beskrivelse": "🏢 Broen mellom skole og arbeidsliv. 🤝 Her får du vist hvem du er for en bedrift.",
        "oppgaver": "👷 Praksis i bedrift og lære seg rutiner i arbeidslivet.",
        "utdanning": "📈 Avgjørende for å få lærlingplass.",
        "quiz": ("Hva er det viktigste en bedrift ser etter hos en elev i YFF?", ["Holdninger og oppmøte", "At man har dyrt verktøy", "Hvor fort man løper"], "Holdninger og oppmøte")
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
    st.success(f"**Utdanningsløp:** {f['utdanning']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.subheader("📏 Omkrets - Rundt figuren")
        st.write("Omkretsen er den totale lengden av alle sidene. Tenk deg at du skal legge en list langs gulvet i et rom. Da må du måle alle veggene og legge dem sammen.")
        st.latex(r"Omkrets = S_1 + S_2 + S_3 + S_4")
        st.write("🏠 **Praktisk eksempel:** Hvis du har en bod på 3m x 2m, må du huske at det er to langvegger og to kortvegger.")
        st.write("**Oppgave:** Et rom er 5m langt og 4m bredt. Hvor mange meter list går med?")
        ans1 = st.radio("Svar:", ["9m", "18m", "20m"], index=None)
        if st.button("Sjekk 1"):
            if ans1 == "18m": st.success("Riktig! (5+4+5+4)"); st.session_state.points += 5
    
    elif m_kat == "Areal":
        st.subheader("⬛ Areal - Overflaten")
        st.write("Arealet forteller hvor stor en flate er i kvadratmeter (m²). Vi bruker dette for å beregne mengden maling, parkett eller gipsplater.")
        st.latex(r"Areal = Lengde \times Bredde")
        st.write("📦 **Praktisk eksempel:** Skal du legge gulv i et rom på 4m x 3m, trenger du 12m² parkett.")
        

[Image of area calculation for a rectangle]

        st.write("**Oppgave:** Du skal male en vegg som er 6m lang og 2,5m høy. Hvor mange m² er veggen?")
        ans2 = st.radio("Svar:", ["15 m²", "8,5 m²", "12 m²"], index=None)
        if st.button("Sjekk 2"):
            if ans2 == "15 m²": st.success("Stemmer! 6 * 2,5 = 15"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.subheader("📈 Prosent og Svinn")
        st.write("I byggfag regner vi ofte 10% svinn. Det betyr at vi bestiller 10% ekstra fordi noe alltid kappes bort.")
        st.write("💰 **Formel:** `Trengs * 1.10 = Bestilling`")
        st.write("**Oppgave:** Du trenger 80m² panel. Læreren sier du må legge til 10% svinn. Hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["88 m²", "80,1 m²", "90 m²"], index=None)
        if st.button("Sjekk 3"):
            if ans3 == "88 m²": st.success("Riktig! 10% av 80 er 8. 80 + 8 = 88."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.subheader("🗺️ Målestokk")
        st.write("Målestokk 1:50 betyr at virkeligheten er 50 ganger større enn på tegningen.")
        st.write("📐 **Tips:** 1 cm på tegningen = 50 cm (0,5 meter) i virkeligheten.")
        
        st.write("**Oppgave:** På en tegning i 1:50 måler du en vegg til 10cm. Hvor lang er den i virkeligheten?")
        ans4 = st.radio("Svar:", ["50 cm", "5 meter", "50 meter"], index=None)
        if st.button("Sjekk 4"):
            if ans4 == "5 meter": st.success("Riktig! 10cm * 50 = 500cm = 5m."); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.subheader("📐 Pytagoras - Sjekk av rett vinkel")
        st.write("For å sjekke om et hjørne er 90 grader, bruker vi 3-4-5 metoden. Hvis de to sidene er 3 og 4 enheter, må diagonalen være nøyaktig 5.")
        st.latex(r"a^2 + b^2 = c^2")
        
        st.write("**Oppgave:** Du måler 30cm på en vegg og 40cm på den andre. Hva må diagonalen være for at det skal være vinkel?")
        ans5 = st.radio("Svar:", ["50 cm", "70 cm", "100 cm"], index=None)
        if st.button("Sjekk 5"):
            if ans5 == "50 cm": st.success("Perfekt! Dette er 'tømrer-trikset'."); st.session_state.points += 20; st.balloons()

with tab_quiz:
    st.header("🎮 Quiz: Test kunnskapen")
    q_fag = st.selectbox("Velg tema:", list(data_db.keys()), key="q_sel")
    spm, valg, svar = data_db[q_fag]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz-svar"):
        if res == svar:
            st.success("Riktig! +20 poeng"); st.session_state.points += 20; st.balloons(); st.rerun()
        else: st.error("Feil svar!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Demo"], "Poeng": [st.session_state.points, 400]}).sort_values("Poeng", ascending=False))
