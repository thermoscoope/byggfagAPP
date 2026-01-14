import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Konfigurasjon
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Initialisering av session_state for navigasjon
if 'startet' not in st.session_state:
    st.session_state.startet = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- FORSIDE (Vises kun hvis ikke startet) ---
if not st.session_state.startet:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    
    st.markdown("""
    ### Din guide til bygg- og anleggsteknikk
    Dette verktøyet er laget for å hjelpe deg med å forstå fagene våre bedre. 
    Her skal vi kombinere praktisk erfaring med smart teknologi!
    
    **Hva skal vi gjøre i dag?**
    * **Lære om de 10 ulike fagretningene**[cite: 9, 11, 23, 27].
    * **Øve på matte** som vi faktisk bruker på byggeplassen[cite: 31, 33, 35, 40].
    * **Teste oss selv** med quizer og samle poeng[cite: 3, 42].
    * **Få hjelp av AI-verksmesteren** når vi står fast[cite: 5, 7].
    """)
    
    st.info("Logg inn under for å starte din treningsøkt.")
    
    navn = st.text_input("Hva heter du?", placeholder="Skriv navnet ditt her...")
    
    if st.button("🚀 START TRENINGEN"):
        if navn:
            st.session_state.user_name = navn
            st.session_state.startet = True
            st.rerun()
        else:
            st.warning("Vennligst skriv inn navnet ditt først.")
            
    st.stop() # Stopper her slik at resten av appen ikke vises før man trykker på knappen

# --- RESTEN AV DIN KODE STARTER HER ---
# (Her limer du inn resten av logikken for tabs, matte og quiz)
st.success(f"Velkommen, {st.session_state.user_name}! Du er nå i gang.")
