import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Configuration de la page
# ==============================
st.set_page_config(
    page_title="Sofiatech Dashboard",
    page_icon="logo.png",
    layout="wide"
)

# ==============================
# Style Sofiatech (Bleu & Orange)
# ==============================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #0056b3;
    text-align: center;
}

div.stButton > button {
    background-color: #ff7a00;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #e66900;
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
                st.error("Accès refusé")

# ==============================
# Tableau de bord
# ==============================
def dashboard():
    st.title("Tableau de bord des projets")

    # Charger Excel
    data = pd.read_excel("projets.xlsx")

    # ==============================
    # Tableau complet
    # ==============================
    st.subheader("Liste complète des projets")
    st.dataframe(data, use_container_width=True)

    # ==============================
    # Filtres
    # ==============================
    col1, col2 = st.columns(2)

    with col1:
        statut = st.selectbox("Filtrer par statut", data["Statut"].unique())
        st.dataframe(data[data["Statut"] == statut])

    with col2:
        resp = st.selectbox("Filtrer par responsable", data["Responsable"].unique())
        st.dataframe(data[data["Responsable"] == resp])

    # ==============================
    # KPI
    # ==============================
    st.subheader("Indicateurs de performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total projets", len(data))
    col2.metric("Terminés", len(data[data["Statut"]=="Terminé"]))
    col3.metric("En cours", len(data[data["Statut"]=="En cours"]))
    col4.metric("En retard", len(data[data["Statut"]=="En retard"]))

    # ==============================
    # Choix couleur graphique
    # ==============================
    st.subheader("Couleur des graphiques")

    couleur = st.radio(
        "Choisir une couleur",
        ("Rouge", "Bordeaux", "Noir", "Blanc"),
        horizontal=True
    )

    couleurs = {
        "Rouge": "red",
        "Bordeaux": "#800000",
        "Noir": "black",
        "Blanc": "lightgray"
    }

    couleur_graph = couleurs[couleur]

    # ==============================
    # Graphique barre
    # ==============================
    st.subheader("Nombre de projets par statut")

    status_count = data["Statut"].value_counts()
    fig, ax = plt.subplots()
    status_count.plot(kind="bar", color=couleur_graph, ax=ax)
    ax.set_ylabel("Nombre")
    st.pyplot(fig)

    # ==============================
    # Graphique camembert
    # ==============================
    st.subheader("Répartition des projets")

    fig2, ax2 = plt.subplots()
    data["Statut"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=[couleur_graph]*len(status_count),
        ax=ax2
    )
    st.pyplot(fig2)

# ==============================
# Navigation
# ==============================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()