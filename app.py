import streamlit as st
import pandas as pd

st.set_page_config(page_title="Byggfag Portalen", layout="wide")

# --- DATA-HÅNDTERING ---
@st.cache_data
def load_data():
    try:
        # Prøver å lese din Excel/CSV-fil
        return pd.read_csv('sporsmal.csv', sep=';', encoding='utf-8')
    except:
        # Reserve: 15 spørsmål basert på dine kategorier
        data = {
            'id': range(1, 16),
            'tema': ['HMS']*5 + ['Verktøylære']*5 + ['Materiallære']*5,
            'mal': [
                'Verneutstyr', 'Skilt og merking', 'Ansvar', 'Førstehjelp', 'Ergonomi',
                'Håndverktøy', 'Måleverktøy', 'Elektroverktøy', 'Vedlikehold', 'Spesialverktøy',
                'Tevirke', 'Betong', 'Isolasjon', 'Metaller', 'Miljø'
            ],
            'niva': [1, 2, 3, 4, 5] * 3,
            'sporsmal': [
                'Hva er viktigst ved bruk av vinkelsliper?', 'Hva betyr et gult og sort skilt?', 'Hvem har hovedansvaret for sikkerheten?', 'Hva gjør du først ved en ulykke?', 'Hvordan bør du løfte tungt?',
                'Hva brukes et vater til?', 'Hva er fordelen med lasermåler?', 'Hva sjekkes før bytte av sagblad?', 'Hvorfor rengjøre verktøy?', 'Hva brukes en kappsag til?',
                'Hva kjennetegner impregnert tre?', 'Hva er bindemiddelet i betong?', 'Hva er hovedoppgaven til isolasjon?', 'Hvorfor bruke aluminium i beslag?', 'Hva er et bærekraftig materiale?'
            ],
            'alternativ_a': [
                'Vernebriller/hørselvern', 'Advarsel', 'Arbeidsgiver', 'Sikre skadestedet', 'Med beina/rett rygg',
                'Sjekke lodd/vater', 'Høy nøyaktighet', 'At støpselet er ute', 'Levetid/sikkerhet', 'Kappe i vinkel',
                'Tåler fukt bedre', 'Sement', 'Hindre varmetap', 'Rustbestandig', 'Lavt klimaavtrykk'
            ],
            'alternativ_b': [
                'Caps', 'Påbud', 'Lærlingen', 'Ringe hjem', 'Med ryggen',
                'Måle lengde', 'Den er billigere', 'At den er støvete', 'Det ser pent ut', 'Kløyve plank',
                'Er lettere', 'Sand', 'Bære veggen', 'Sterkeste metall', 'Tåler mye vekt'
            ],
            'fasit': ['alternativ_a']*15,
            'forklaring': [
                'Beskyttelse av øyne og hørsel er kritisk.', 'Gule skilt varsler om fare.', 'Arbeidsmiljøloven plasserer ansvaret hos leder.', 'Egen sikkerhet og sikring først.', 'Sparer ryggen for slitasje.',
                'Viktig for rette konstruksjoner.', 'Presisjon er nøkkelen i byggfag.', 'Unngå utilsiktet start av maskin.', 'Forebygger ulykker og rust.', 'Presis kapping på tvers av fiber.',
                'Beskyttet mot råte og sopp.', 'Sement limer stein og sand sammen.', 'Reduserer energibruk i bygget.', 'Tåler vær og vind uten å ruste.', 'Handler om miljø over hele livsløpet.'
            ]
        }
        return pd.DataFrame(data)

df = load_data()

# --- SESJON-STYRING ---
if 'side' not in st.session_state:
    st.session_state.side = "Hjem"
if 'valgt_tema' not in st.session_state:
    st.session_state.valgt_tema = None
if 'niva' not in st.session_state:
    st.session_state.niva = 1
if 'feil_logg' not in st.session_state:
    st.session_state.feil_logg = []

# --- HJEMMESIDE ---
if st.session_state.side == "Hjem":
    st.title("🏗️ Velkommen til Byggfag-treneren")
    st.write("Velg et område du ønsker å bli bedre i:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ HMS", use_container_width=True):
            st.session_state.valgt_tema = "HMS"
            st.session_state.side = "Quiz"
            st.rerun()
    with col2:
        if st.button("🛠️ Verktøylære", use_container_width=True):
            st.session_state.valgt_tema = "Verktøylære"
            st.session_state.side = "Quiz"
            st.rerun()
    with col3:
        if st.button("🌲 Materiallære", use_container_width=True):
            st.session_state.valgt_tema = "Materiallære"
            st.session_state.side = "Quiz"
            st.rerun()

# --- QUIZ-SIDE ---
elif st.session_state.side == "Quiz":
    if st.button("⬅️ Meny"):
        st.session_state.side = "Hjem"
        st.session_state.niva = 1
        st.rerun()
    
    tema_df = df[df['tema'] == st.session_state.valgt_tema]
    aktuelt_spm = tema_df[tema_df['niva'] == st.session_state.niva]

    if not aktuelt_spm.empty:
        spm = aktuelt_spm.iloc[0]
        st.header(f"Område: {st.session_state.valgt_tema}")
        st.subheader(f"Nivå {st.session_state.niva} av 5")
        st.progress(st.session_state.niva / 5)
        
        st.info(spm['sporsmal'])
        valg = st.radio("Ditt svar:", [spm['alternativ_a'], spm['alternativ_b']])

        if st.button("Sjekk svar"):
            valgt_id = "alternativ_a" if valg == spm['alternativ_a'] else "alternativ_b"
            if valgt_id == spm['fasit']:
                st.success("Riktig!")
                st.session_state.niva += 1
                st.rerun()
            else:
                st.error("Ikke helt riktig.")
                st.warning(f"💡 Tips: {spm['forklaring']}")
                if spm['mal'] not in st.session_state.feil_logg:
                    st.session_state.feil_logg.append(spm['mal'])
    else:
        st.balloons()
        st.success(f"Bra jobbet! Du har fullført {st.session_state.valgt_tema}.")
        if st.session_state.feil_logg:
            st.write("### Du bør øve mer på disse målene i NotebookLM:")
            for m in st.session_state.feil_logg: # Rettet 'i' til 'in' her
                st.write(f"- 🔍 {m}")
        else:
            st.write("Fantastisk! Du hadde ingen feil i denne kategorien.")