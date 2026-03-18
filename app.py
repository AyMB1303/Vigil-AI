import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Vigil-AI | Système Dynamique", layout="wide", page_icon="🛡️")

# Style CSS pour le look moderne
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTION DYNAMIQUE DES DONNÉES ---
st.sidebar.image("https://img.icons8.com/fluency/144/shield.png", width=80)
st.sidebar.title("Configuration")

# Zone d'upload pour la démo en direct
uploaded_file = st.sidebar.file_uploader("📥 Importer nouvelles données (CSV)", type="csv")

@st.cache_data
def load_data(source):
    return pd.read_csv(source)

# Logique de sélection de la source
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("✅ Données utilisateur actives")
else:
    # Charge ton fichier par défaut
    try:
        df = load_data('Attendance_Prediction.csv')
        st.sidebar.info("📊 Utilisation de la base historique")
    except:
        st.sidebar.error("⚠️ Fichier par défaut manquant")
        st.stop()

# --- 3. NAVIGATION ---
page = st.sidebar.radio("Navigation", ["🌐 Dashboard Temps Réel", "🎯 Agent IA Expert", "💰 Rentabilité SI"])

# --- 4. PAGE 1 : DASHBOARD TEMPS RÉEL ---
if page == "🌐 Dashboard Temps Réel":
    st.title("🌐 Pilotage Dynamique Vigil-AI")
    
    # Calculs automatiques basés sur le fichier (qu'il soit nouveau ou ancien)
    total_etudiants = len(df['student_id'].unique())
    taux_presence = (df['attendance'].mean() * 100)
    alertes = len(df[df['attendance'] == 0])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Effectif Analysé", f"{total_etudiants}")
    c2.metric("Taux d'Assiduité", f"{taux_presence:.1f}%")
    c3.metric("Absences Détectées", f"{alertes}")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig1 = px.pie(df, names='course', hole=0.4, title="Répartition par Filière")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.histogram(df, x="absence_reason", title="Analyse des motifs", color_discrete_sequence=['#58a6ff'])
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. PAGE 2 : AGENT IA ---
elif page == "🎯 Agent IA Expert":
    st.title("🎯 Diagnostic de l'Agent IA")
    
    with st.form("ia_form"):
        col1, col2 = st.columns(2)
        study = col1.slider("Heures d'étude", 0, 10, 4)
        sleep = col1.slider("Heures de sommeil", 3, 12, 7)
        travel = col2.number_input("Trajet (min)", 10, 180, 30)
        weather = col2.selectbox("Météo", ["Sunny", "Cloudy", "Rainy"])
        submit = st.form_submit_button("Lancer l'Analyse")

    if submit:
        # Simulation d'IA
        risk = 0
        if study < 3: risk += 40
        if travel > 60: risk += 30
        if weather == "Rainy": risk += 10
        
        st.subheader(f"Résultat : Risque de {risk}%")
        if risk > 60:
            st.error("🚨 ALERTE CRITIQUE : L'agent recommande une intervention.")
        else:
            st.success("✅ PROFIL STABLE : Suivi standard.")
        st.progress(risk/100)

# --- 6. PAGE 3 : RENTABILITÉ ---
else:
    st.title("💰 Analyse de la Valeur (ROI)")
    jh_gagnes = (len(df) * 5 / 60) / 8  # 5min par ligne / 60min / 8h
    gain_dh = jh_gagnes * 1200
    
    st.metric("Économie en Jours-Homme (JH)", f"{int(jh_gagnes)} JH")
    st.metric("Valeur Financière Créée", f"{gain_dh:,.0f} DH")
    
    st.info("Ce calcul s'adapte automatiquement au volume du fichier importé.")
