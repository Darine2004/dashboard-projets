import streamlit as st
import pandas as pd

# ==============================
# Configuration de la page
# ==============================
st.set_page_config(
    page_title="Sofiatech Dashboard",
    page_icon="logo.png",
    layout="wide"
)

# ==============================
# Style élégant avec fond #781E34
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

body, .stApp, .stTextInput, .stButton>button {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background-color: #781E34;  /* Fond principal */
}

h1, h2, h3 {
    color: #000000;  /* Texte noir */
    text-align: center;
}

.stTextInput>div>div>input {
    background-color: rgba(255,255,255,0.9); /* Champs blancs légèrement transparents */
    color: #000000;
    border-radius: 8px;
    padding: 10px;
}

div.stButton>button {
    background-color: #ffffff; /* Boutons blancs */
    color: #781E34;  /* Texte bouton en identité */
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    font-size: 16px;
}

div.stButton>button:hover {
    background-color: rgba(255,255,255,0.8);
    color: #000000;
}

.stAlert {
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Identifiants autorisés
# ==============================
USERNAME = "DarineetNour"
PASSWORD = "PFA"

# ==============================
# Session
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==============================
# Page de connexion
# ==============================
def login_page():
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image("logo.png", width=200)
        st.markdown("<h2>Connexion Sofiatech</h2>", unsafe_allow_html=True)
        
        user = st.text_input("Nom d'utilisateur")
        pwd = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            if user == USERNAME and pwd == PASSWORD:
                st.session_state.logged_in = True
            else:
                st.error("Accès refusé. Vérifiez vos identifiants.")

# ==============================
# Tableau de bord simple
# ==============================
def dashboard():
    st.title("Tableau de bord des projets")
    data = pd.read_excel("projets.xlsx")
    st.dataframe(data, use_container_width=True)

# ==============================
# Navigation
# ==============================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()