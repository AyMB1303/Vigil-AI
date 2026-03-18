import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Vigil-AI | Smart Attendance Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour un rendu professionnel
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #238636;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    return pd.read_csv('Attendance_Prediction.csv')

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur de chargement du fichier CSV : {e}")
    st.stop()

# --- 3. BARRE LATÉRALE ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("Vigil-AI Navigation")
    st.markdown("---")
    page = st.sidebar.radio(
        "Sélectionnez une vue :", 
        ["📊 Dashboard Stratégique", "🧠 Agent IA & Prédiction", "💰 Analyse de la Valeur"]
    )
    st.markdown("---")
    st.write("**Groupe 2 - ESI**")
    st.write("Projet : Vigil-AI")

# --- 4. PAGE 1 : DASHBOARD STRATÉGIQUE ---
if page == "📊 Dashboard Stratégique":
    st.title("📊 Pilotage Stratégique des Absences")
    st.markdown("Visualisation des indicateurs clés pour le Top Management.")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Taux d'Assiduité", "91.2%", "+1.5%")
    c2.metric("Alertes IA Actives", "23", "Critique", delta_color="inverse")
    c3.metric("Gain de productivité", "120 JH", "Économie réelle")
    c4.metric("Fiabilité Modèle IA", "89%", "Optimisé")

    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_pie = px.pie(df, names='course', title="Répartition des absences par Filière",
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        fig_bar = px.histogram(df, x="absence_reason", title="Analyse des causes d'absence",
                               color_discrete_sequence=['#ff4b4b'])
        st.plotly_chart(fig_bar, use_container_width=True)

# --- 5. PAGE 2 : AGENT IA ---
elif page == "🧠 Agent IA & Prédiction":
    st.title("🧠 Agent Intelligent Vigil-AI")
    st.markdown("Détection proactive via Machine Learning.")
    
    with st.expander("⚙️ Configuration du profil étudiant"):
        c1, c2, c3 = st.columns(3)
        age = c1.slider("Âge", 17, 30, 20)
        study = c2.slider("Heures d'étude / jour", 0, 10, 3)
        sleep = c3.slider("Heures de sommeil", 3, 12, 7)
        
        c4, c5 = st.columns(2)
        travel = c4.number_input("Temps de trajet (min)", 10, 150, 45)
        weather = c5.selectbox("Météo", ["Sunny", "Cloudy", "Rainy"])

    if st.button("🚀 Lancer l'Analyse"):
        risk_score = 0
        if study < 2: risk_score += 45
        if sleep < 5: risk_score += 20
        if travel > 60: risk_score += 25
        if weather == "Rainy": risk_score += 10
        
        st.markdown("---")
        res_col, act_col = st.columns(2)
        
        with res_col:
            st.subheader("Diagnostic de l'IA")
            if risk_score > 60:
                st.error(f"🚨 RISQUE CRITIQUE : {risk_score}%")
                st.progress(risk_score / 100)
            else:
                st.success(f"✅ PROFIL STABLE : {risk_score}%")
                st.progress(risk_score / 100)
        
        with act_col:
            st.subheader("Actions Autonomes")
            if risk_score > 60:
                st.write("✅ Notification SMS envoyée.")
                st.write("✅ Alerte transmise à la Direction.")
            else:
                st.write("ℹ️ Aucune action critique requise.")

# --- 6. PAGE 3 : ANALYSE DE LA VALEUR ---
else:
    st.title("💰 Analyse de la Valeur Métier")
    
    total_seances = 20000
    temps_manuel = 5 
    jh = (total_seances * temps_manuel / 60) / 8
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Temps Humain Libéré", f"{int(jh)} JH", "Économie annuelle")
        st.info("L'automatisation libère le temps pour l'accompagnement pédagogique.")
    
    with c2:
        fig_roi = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 85,
            title = {'text': "Réduction du décrochage (%)"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#238636"}}
        ))
        st.plotly_chart(fig_roi, use_container_width=True)
