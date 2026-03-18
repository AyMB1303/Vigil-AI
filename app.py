import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

# Configuration de la page
st.set_page_config(page_title="Vigil-AI | Dashboard SI", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv('Attendance_Prediction.csv')

df = load_data()

# Sidebar - Navigation
st.sidebar.title("🛡️ Vigil-AI Navigation")
page = st.sidebar.radio("Aller à :", ["Tableau de bord Global", "Agent IA : Analyse des Risques"])

if page == "Tableau de bord Global":
    st.header("📊 Pilotage Stratégique (Top Management)")
    
    # KPIs - Valeur Opérationnelle
    c1, c2, c3 = st.columns(3)
    c1.metric("Taux d'Assiduité Moyen", "91.7%", "+2.1%")
    c2.metric("Gain de temps estimé", "120 JH", "Cible: 200 JH")
    c3.metric("Alertes IA Critiques", "23", "Action requise")

    # Graphique interactif
    fig = px.pie(df, names='course', title="Répartition des absences par filière")
    st.plotly_chart(fig)

else:
    st.header("🧠 Agent Intelligent : Détection des Risques")
    
    col_input, col_res = st.columns([1, 1])
    
    with col_input:
        st.subheader("Simuler un profil étudiant")
        age = st.slider("Âge", 17, 25, 20)
        study = st.slider("Heures d'étude", 0, 10, 4)
        sleep = st.slider("Heures de sommeil", 4, 12, 7)
        travel = st.number_input("Temps de trajet (min)", 10, 120, 30)
        
        btn = st.button("Lancer l'analyse de l'Agent")

    with col_res:
        if btn:
            # Simulation de décision de l'agent
            if study < 2 or travel > 60:
                st.error("⚠️ ALERTE : Risque de décrochage élevé (85%)")
                st.write("**Action de l'agent :** Convocation pédagogique générée.")
            else:
                st.success("✅ PROFIL STABLE : Risque faible (12%)")
                st.write("**Action de l'agent :** Suivi standard activé.")
