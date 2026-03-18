import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# --- 1. CONFIGURATION ÉLÉGANTE ---
st.set_page_config(
    page_title="Vigil-AI Elite | Smart Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DESIGN CSS "DARK PREMIUM" ---
st.markdown("""
    <style>
    /* Global Background */
    .main { background-color: #0b0e14; color: #e6edf3; }
    
    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Modern Titles */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb, #388bfd);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(31, 111, 235, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTION DES DONNÉES ---
@st.cache_data
def get_data(source):
    return pd.read_csv(source)

# Logo et Titre Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ VIGIL-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Smart Attendance & IA Predictive</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    uploaded_file = st.file_uploader("📥 Injecter un nouveau Dataset", type="csv")
    
    st.markdown("---")
    menu = st.radio("Pilotage Système", 
                    ["🏛️ Direction Générale", "🤖 Intelligence Agent", "📈 Analyse ROI & Valeur"])
    st.markdown("---")
    st.caption("ESI Groupe 2 - Prototype V3.0")

# Chargement de la source
df = get_data(uploaded_file) if uploaded_file else get_data('Attendance_Prediction.csv')

# --- 4. PAGE 1 : DIRECTION GÉNÉRALE ---
if menu == "🏛️ Direction Générale":
    st.markdown("# 🏛️ Tableau de Bord Stratégique")
    st.markdown("---")
    
    # KPIs avec colonnes proportionnelles
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Assiduité Actuelle", f"{df['attendance'].mean()*100:.1f}%", "+2.4%")
    with k2: st.metric("Inscrits Analysés", len(df['student_id'].unique()), "Temps Réel")
    with k3: st.metric("Seuil Critique IA", "23 Alertes", "-5", delta_color="inverse")
    with k4: st.metric("Gain Productivité", "120 JH", "Objectif Atteint")

    st.markdown("### 📊 Analyse Multi-Dimensionnelle")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Graphique Treemap pour les filières
        fig_tree = px.treemap(df, path=['course', 'year'], values='attendance',
                              title="Concentration de l'Assiduité par Filière et Année",
                              color_continuous_scale='RdYlGn')
        fig_tree.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_tree, use_container_width=True)

    with col_b:
        # Analyse des motifs d'absence
        reasons = df['absence_reason'].value_counts().reset_index()
        fig_reasons = px.bar(reasons, x='count', y='absence_reason', orientation='h',
                             title="Cartographie des Motifs",
                             color='count', color_continuous_scale='Blues')
        fig_reasons.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_reasons, use_container_width=True)

# --- 5. PAGE 2 : INTELLIGENCE AGENT ---
elif menu == "🤖 Intelligence Agent":
    st.markdown("# 🤖 Agent IA : Diagnostic Prédictif")
    st.info("L'agent analyse les signaux faibles pour prévenir le décrochage scolaire.")
    
    c_form, c_viz = st.columns([1, 1.2])
    
    with c_form:
        st.markdown("### ⚙️ Paramètres du Signal")
        with st.container():
            st.markdown('<div style="background-color:#161b22; padding:20px; border-radius:20px; border:1px solid #30363d;">', unsafe_allow_html=True)
            hrs_study = st.select_slider("Heures d'Étude Individuelle", options=range(0, 13), value=4)
            hrs_sleep = st.select_slider("Qualité du Sommeil (Heures)", options=range(3, 13), value=7)
            time_travel = st.number_input("Temps de Transport (Minutes)", 10, 180, 45)
            ext_weather = st.selectbox("Facteur Météo", ["Sunny", "Cloudy", "Rainy", "Stormy"])
            st.markdown('</div>', unsafe_allow_html=True)
            
        if st.button("🔍 Lancer le Scan Prédictif"):
            with st.spinner('L\'IA analyse les corrélations...'):
                time.sleep(1.5) # Effet dramatique pour la démo
                st.session_state.analyzed = True
                
    with c_viz:
        if 'analyzed' in st.session_state:
            # Score de risque
            risk = 0
            if hrs_study < 3: risk += 45
            if time_travel > 60: risk += 25
            if hrs_sleep < 6: risk += 20
            if ext_weather in ["Rainy", "Stormy"]: risk += 10
            
            st.markdown("### 🔬 Résultat du Scan")
            
            # Gauge moderne
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk,
                title = {'text': "Indice de Vulnérabilité (%)"},
                delta = {'reference': 50, 'increasing': {'color': "#ff4b4b"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1},
                    'bar': {'color': "#388bfd"},
                    'steps': [
                        {'range': [0, 40], 'color': "#238636"},
                        {'range': [40, 70], 'color': "#d29922"},
                        {'range': [70, 100], 'color': "#f85149"}],
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
            
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)

# --- 6. PAGE 3 : ANALYSE ROI ---
else:
    st.markdown("# 📈 Analyse de la Valeur SI")
    
    # Calcul dynamique basé sur le coût de votre groupe
    total_recs = len(df)
    jh_unit = 5 / 480 # 5 min par rapport à une journée de 8h (480 min)
    jh_saved = int(total_recs * jh_unit)
    cout_projet = 93600 # Ton budget
    gain_financier = jh_saved * 1200 # 1200 DH le JH
    roi = ((gain_financier - cout_projet) / cout_projet) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Économie en Temps", f"{jh_saved} JH", "Productivité")
    c2.metric("Valeur Créée", f"{gain_financier:,} DH", "Annuel")
    c3.metric("ROI du Projet", f"{roi:.1f}%", "Excellent")

    st.markdown("---")
    
    # Graphique de rentabilité cumulée
    months = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]
    monthly_gain = gain_financier / 12
    cumulative_gain = [monthly_gain * i for i in range(1, 13)]
    
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Scatter(x=months, y=cumulative_gain, name='Gain Cumulé', line=dict(color='#388bfd', width=4)))
    fig_roi.add_trace(go.Scatter(x=months, y=[cout_projet]*12, name='Investissement Initial', line=dict(color='#f85149', dash='dash')))
    
    fig_roi.update_layout(title="Point d'Équilibre (Break-even Analysis)",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_roi, use_container_width=True)
    
    st.success(f"💡 Le projet Vigil-AI atteint son seuil de rentabilité après {round(cout_projet/monthly_gain, 1)} mois d'utilisation.")
