import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Configuration de la page
# ==============================
st.set_page_config(
    page_title="ENSIT junior entreprise Dashboard",
    page_icon="logo.png",
    layout="wide"
)

# ==============================
# Style élégant page de connexion
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

body, .stApp, .stTextInput, .stButton>button {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background: rgba(255, 255, 255, 0.05); /* Fond très léger */
}

h1, h2, h3 {
    color: #781E34;
    text-align: center;
}

.stTextInput>div>div>input {
    background-color: rgba(255,255,255,0.8);
    color: #000000;
    border-radius: 8px;
    padding: 10px;
}

div.stButton>button {
    background-color: #781E34;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    font-size: 16px;
}

div.stButton>button:hover {
    background-color: #5c1429;
}

.stAlert {
    color: #781E34;
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
# Tableau de bord
# ==============================
def dashboard():
    st.title("Tableau de bord des projets")

    data = pd.read_excel("projets.xlsx")

    st.subheader("Liste complète des projets")
    st.dataframe(data, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        statut = st.selectbox("Filtrer par statut", data["Statut"].unique())
        st.dataframe(data[data["Statut"] == statut])

    with col2:
        resp = st.selectbox("Filtrer par responsable", data["Responsable"].unique())
        st.dataframe(data[data["Responsable"] == resp])

    st.subheader("Indicateurs de performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total projets", len(data))
    col2.metric("Terminés", len(data[data["Statut"]=="Terminé"]))
    col3.metric("En cours", len(data[data["Statut"]=="En cours"]))
    col4.metric("En retard", len(data[data["Statut"]=="En retard"]))

    st.subheader("Couleur des graphiques")
    couleur = st.radio("Choisir une couleur", ("Rouge", "Bordeaux", "Noir", "Blanc"), horizontal=True)
    couleurs = {"Rouge":"red", "Bordeaux":"#800000", "Noir":"black", "Blanc":"lightgray"}
    couleur_graph = couleurs[couleur]

    st.subheader("Nombre de projets par statut")
    status_count = data["Statut"].value_counts()
    fig, ax = plt.subplots()
    status_count.plot(kind="bar", color=couleur_graph, ax=ax)
    ax.set_ylabel("Nombre")
    st.pyplot(fig)

    st.subheader("Répartition des projets")
    fig2, ax2 = plt.subplots()
    data["Statut"].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=[couleur_graph]*len(status_count), ax=ax2)
    st.pyplot(fig2)

# ==============================
# Navigation
# ==============================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()