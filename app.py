import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Identifiants autorisés
# ==========================
AUTHORIZED_USERNAME = "DarineetNour"
AUTHORIZED_PASSWORD = "PFA"

# ==========================
# Initialiser la session
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # pas connecté par défaut

# ==========================
# Fenêtre de connexion
# ==========================
def show_login():
    st.title("Connexion au Tableau de bord")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_btn = st.button("Se connecter")

    if login_btn:
        if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect. Vous n'avez pas accès.")

# ==========================
# Afficher le tableau de bord
# ==========================
def show_dashboard():
    st.title("Tableau de bord des projets - ENSIT JE")

    # Charger les données Excel
    data = pd.read_excel("projets.xlsx")

    # Tableau complet
    st.subheader("Liste complète des projets")
    st.dataframe(data)

    # Filtres interactifs
    st.subheader("Filtrer les projets")
    status = st.selectbox("Choisir un statut", data["Statut"].unique())
    filtered_status = data[data["Statut"] == status]
    st.subheader(f"Projets avec statut : {status}")
    st.dataframe(filtered_status)

    responsable = st.selectbox("Choisir un responsable", data["Responsable"].unique())
    filtered_responsable = data[data["Responsable"] == responsable]
    st.subheader(f"Projets du responsable : {responsable}")
    st.dataframe(filtered_responsable)

    # KPI
    st.subheader("Indicateurs de performance (KPI)")
    st.write("Nombre total de projets :", len(data))
    st.write("Projets terminés :", len(data[data["Statut"]=="Terminé"]))
    st.write("Projets en cours :", len(data[data["Statut"]=="En cours"]))
    st.write("Projets en retard :", len(data[data["Statut"]=="En retard"]))

    # Choix des couleurs
    st.subheader("Choisir la couleur des graphiques")
    couleur = st.radio("Couleur du graphique", ("Rouge", "Bordeaux", "Noir", "Blanc"))
    couleurs_dict = {"Rouge":"red", "Bordeaux":"#800000", "Noir":"black", "Blanc":"white"}
    couleur_graph = couleurs_dict[couleur]

    # Graphique barre
    st.subheader("Graphique : Nombre de projets par statut")
    status_count = data["Statut"].value_counts()
    fig, ax = plt.subplots()
    status_count.plot(kind="bar", color=couleur_graph, ax=ax)
    ax.set_ylabel("Nombre de projets")
    st.pyplot(fig)

    # Graphique camembert
    st.subheader("Graphique : Répartition des projets (camembert)")
    fig2, ax2 = plt.subplots()
    data["Statut"].value_counts().plot(
        kind="pie",
        autopct='%1.1f%%',
        colors=[couleur_graph]*len(data["Statut"].unique()),
        ax=ax2
    )
    st.pyplot(fig2)

# ==========================
# Logique principale
# ==========================
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()