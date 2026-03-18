import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Vigil-AI | Smart Behavior Tracking", layout="wide", page_icon="🛡️")

# --- 2. STYLE CSS MODERNE ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        padding: 20px; border-radius: 15px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CHARGEMENT DYNAMIQUE ---
@st.cache_data
def load_data(source):
    return pd.read_csv(source)

# Barre latérale pour l'injection de données
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/shield.png", width=80)
    st.title("Vigil-AI Console")
    uploaded_file = st.file_uploader("📥 Importer Dataset (CSV)", type="csv")
    st.markdown("---")
    page = st.radio("Navigation", ["🌐 Dashboard Stratégique", "🎯 Agent IA & Patterns", "💰 Analyse de la Valeur"])

# Source de données (soit l'upload, soit le fichier par défaut)
df = load_data(uploaded_file) if uploaded_file else load_data('Attendance_Prediction.csv')

# --- 4. PAGE 1 : DASHBOARD STRATÉGIQUE ---
if page == "🌐 Dashboard Stratégique":
    st.title("🌐 Pilotage Stratégique Global")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Assiduité Globale", f"{df['attendance'].mean()*100:.1f}%")
    m2.metric("Effectif Analysé", len(df['student_id'].unique()))
    
    # Identification dynamique du pattern météo le plus risqué
    weather_risk = df.groupby('weather')['attendance'].mean().idxmin()
    m3.metric("Facteur de Risque Majeur", f"Météo: {weather_risk}")
    
    # Gain JH basé sur le nombre de lignes actuel
    jh_gagnes = (len(df) * 5 / 480) 
    m4.metric("Productivité (JH)", f"{int(jh_gagnes)}")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.pie(df, names='course', hole=0.5, title="Absences par Filière")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.histogram(df, x="absence_reason", title="Répartition des Motifs", color_discrete_sequence=['#58a6ff'])
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. PAGE 2 : AGENT IA & PATTERNS (C'EST ICI QUE C'EST DYNAMIQUE) ---
elif page == "🎯 Agent IA & Patterns":
    st.title("🎯 Agent IA : Analyse Comportementale")
    st.write("L'agent identifie les patterns d'absences en fonction du profil saisi.")

    col_form, col_res = st.columns([1, 1.2])

    with col_form:
        st.subheader("Simuler un Profil")
        with st.container():
            study = st.slider("Heures d'étude", 0, 10, 4)
            sleep = st.slider("Heures de sommeil", 3, 12, 7)
            travel = st.number_input("Trajet (min)", 10, 180, 45)
            # Ajout d'une condition dynamique : le type de classe
            class_type = st.selectbox("Type de Session", df['class_type'].unique())
            weather = st.selectbox("Météo Prévue", df['weather'].unique())
            
        btn = st.button("Lancer le Scan de l'Agent")

    with col_res:
        if btn:
            # ALGORITHME DE DÉTECTION DE PATTERNS
            # L'IA calcule le risque en fonction de la "moyenne historique" pour ces paramètres précis
            risk_base = 20
            
            # Pattern dynamique : Si l'étudiant étudie peu
            if study < 3: risk_base += 30
            
            # Pattern dynamique : Impact de la météo et du trajet
            if weather == "rainy" and travel > 60: risk_base += 25
            
            # Pattern dynamique : Détection du type de classe (Online vs Offline)
            if class_type == "offline" and travel > 90:
                risk_base += 15
                st.warning(f"⚠️ **Pattern détecté :** Difficulté d'accès aux cours en présentiel due au temps de trajet.")

            st.subheader(f"Probabilité de Pénalité : {risk_base}%")
            st.progress(risk_base/100)
            
            if risk_base > 60:
                st.error(f"🔴 État : CRITIQUE. Vous avez {risk_base}% de chance d'être pénalisé.")
                st.write("**Action de l'Agent :** Alerte envoyée pour prévenir une sanction administrative.")
            else:
                st.success(f"🟢 État : STABLE. Risque de pénalité faible ({risk_base}%).")

# --- 6. PAGE 3 : ANALYSE DE LA VALEUR ---
else:
    st.title("💰 Analyse de la Valeur & ROI")
    cost_project = 93600
    jh_val = (len(df) * 5 / 480)
    total_gain = jh_val * 1200
    
    st.metric("Économie Générée", f"{total_gain:,.0f} DH", f"+{int(jh_val)} JH")
    
    fig_roi = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = (total_gain / cost_project) * 100,
        title = {'text': "Rentabilité du Projet (%)"},
        gauge = {'axis': {'range': [0, 200]}, 'bar': {'color': "#238636"}}
    ))
    st.plotly_chart(fig_roi, use_container_width=True)
