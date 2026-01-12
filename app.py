import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- KONFIGURASJON & DESIGN ---
st.set_page_config(page_title="Byggmester-Appen", layout="wide")

# CSS for å få "Byggeplass-gul" og store knapper
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    div.stButton > button {
        background-color: #ffcc00; color: black; font-weight: bold;
        border-radius: 10px; border: 2px solid #333; height: 60px;
    }
    .question-box {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 10px solid #ffcc00; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Funksjon for animasjoner
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_build = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_i9mxcD.json") # En gravemaskin/arbeider

# --- SPØRSMÅLSBANK (Eksempel på struktur for 15+ spørsmål) ---
quiz_data = {
    "Tømrer": [
        {"q": "Hva er c/c avstand på stendere?", "a": ["60 cm", "30 cm", "45 cm"], "correct": "60 cm"},
        {"q": "Hvilket verktøy brukes til å sjekke om veggen er loddrett?", "a": ["Vater", "Tommestokk", "Vinkelsliper"], "correct": "Vater"},
        # ... legg til totalt 15 her
    ],
    "Anleggsteknikk": [
        {"q": "Hva betyr det å 'stikke ut' en tomt?", "a": ["Merke av hvor bygget skal stå", "Fjerne stubber", "Grave grøft"], "correct": "Merke av hvor bygget skal stå"},
        # ... legg til totalt 15 her
    ]
}

# --- HOVEDMENY ---
st.title("🚧 Byggfag-Portalen: Fra Lærling til Mester")
st_lottie(lottie_build, height=150)

side = st.sidebar.radio("Meny", ["Hovedside", "Kunnskapstest (Quiz)", "Loggbok Bedrift"])

if side == "Kunnskapstest (Quiz)":
    fag = st.selectbox("Velg ditt fagområde:", list(quiz_data.keys()))
    
    # Session State holder styr på hvilket spørsmål eleven er på
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    if 'score' not in st.session_state: st.session_state.score = 0

    current_q = quiz_data[fag][st.session_state.q_idx]
    
    st.markdown(f"<div class='question-box'><h3>Spørsmål {st.session_state.q_idx + 1} av 15</h3><p>{current_q['q']}</p></div>", unsafe_allow_html=True)
    
    valg = st.radio("Velg riktig svar:", current_q['a'], key=f"q_{st.session_state.q_idx}")
    
    if st.button("Svar"):
        if valg == current_q['correct']:
            st.success("Riktig! 🔨")
            st.session_state.score += 1
        else:
            st.error(f"Feil. Riktig svar var {current_q['correct']}")
        
        if st.session_state.q_idx < len(quiz_data[fag]) - 1:
            st.session_state.q_idx += 1
            st.rerun()
        else:
            st.balloons()
            st.write(f"### Quiz ferdig! Din score: {st.session_state.score} / {len(quiz_data[fag])}")
            if st.button("Start på nytt"):
                st.session_state.q_idx = 0
                st.session_state.score = 0
                st.rerun()
