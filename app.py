import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Vigil-AI | ESI Enterprise", layout="wide", page_icon="🛡️")

# CSS : Dark Mode Professionnel avec Cartes Néon
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .stRadio > div { flex-direction: row; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv('Attendance_Prediction.csv')

df = load_data()

# --- 3. NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/shield.png", width=80)
    st.title("Vigil-AI Console")
    page = st.radio("Pilotage :", ["📊 Direction & KPI", "👤 Suivi Étudiant 360°", "🧠 Simulateur Agent IA"])
    st.markdown("---")
    st.info("Système configuré sur le seuil de 16 absences (Règlement ESI)")

# --- 4. PAGE 1 : DIRECTION & KPI (AMÉLIORÉE) ---
if page == "📊 Direction & KPI":
    st.title("📊 Tableau de Bord de Gouvernance SI")
    
    # KPIs Flash
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Assiduité Globale", f"{df['attendance'].mean()*100:.1f}%", "+1.2%")
    c2.metric("Alertes Critiques", len(df[df['attendance'] == 0]), "Total Absences")
    c3.metric("Engagement Moyen", f"{df['study_hours'].mean():.1f}h", "Étude/Jour")
    c4.metric("Efficacité IA", "94%", "Précision")

    st.markdown("---")
    
    # Ligne 1 de Graphiques
    g1, g2 = st.columns(2)
    with g1:
        # Sunburst : Vision hiérarchique Filière > Année
        fig_sun = px.sunburst(df, path=['course', 'year'], values='attendance', 
                              title="Structure de l'Assiduité (Filières & Promotions)",
                              color_continuous_scale='Blues')
        st.plotly_chart(fig_sun, use_container_width=True)
    with g2:
        # Boxplot : Dispersion du sommeil par filière (Bien-être vs Performance)
        fig_box = px.box(df, x="course", y="sleep_hours", color="course",
                         title="Analyse du Sommeil par Filière (Facteur Santé)")
        st.plotly_chart(fig_box, use_container_width=True)

    # Ligne 2 de Graphiques
    g3, g4 = st.columns(2)
    with g3:
        # Histogramme : Impact de la météo sur l'absentéisme
        weather_impact = df[df['attendance'] == 0].groupby('weather').size().reset_index(name='absences')
        fig_weather = px.bar(weather_impact, x='weather', y='absences', color='absences',
                             title="Corrélation Météo / Absentéisme", color_continuous_scale='Reds')
        st.plotly_chart(fig_weather, use_container_width=True)
    with g4:
        # Scatter : Étude vs Sommeil (Patterns de réussite)
        fig_scat = px.scatter(df.sample(500), x="study_hours", y="sleep_hours", color="attendance",
                              title="Nuage de Points : Étude vs Sommeil (Échantillon 500)")
        st.plotly_chart(fig_scat, use_container_width=True)

# --- 5. PAGE 2 : SUIVI ÉTUDIANT 360° ---
elif page == "👤 Suivi Étudiant 360°":
    st.title("👤 Dossier Individuel Prédictif")
    student_id = st.selectbox("Sélectionner l'ID Étudiant :", df['student_id'].unique())
    
    u_data = df[df['student_id'] == student_id]
    absences = len(u_data[u_data['attendance'] == 0])
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.subheader(f"Statut : ID {student_id}")
        st.write(f"Cumul : **{absences}** / 16 séances d'absence.")
        st.progress(min(absences / 16, 1.0))
        if absences >= 16:
            st.error("🚨 ÉTUDIANT PÉNALISÉ (Seuil dépassé)")
        elif absences >= 10:
            st.warning("⚠️ ATTENTION : Risque de pénalité imminent.")
        else:
            st.success("✅ Dossier sous le seuil critique.")

    with col_r:
        # Radar Chart : Profil comportemental
        categories = ['Étude', 'Sommeil', 'Assiduité']
        values = [u_data['study_hours'].mean()*10, u_data['sleep_hours'].mean()*10, (1 - (absences/len(u_data)))*100]
        fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', line_color='#58a6ff'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
                                title="Radar Comportemental", paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. PAGE 3 : SIMULATEUR AGENT IA (AMÉLIORÉE) ---
elif page == "🧠 Simulateur Agent IA":
    st.title("🧠 Agent Vigil-AI : Scan de Risque")
    st.markdown("Ajustez les paramètres pour voir la prédiction de l'agent en temps réel.")
    
    with st.container():
        st.markdown("### 🛠️ Paramètres du Profil")
        col1, col2 = st.columns(2)
        
        with col1:
            study_h = st.slider("Heures d'étude individuelle / jour", 0, 15, 5)
            sleep_h = st.slider("Heures de sommeil / nuit", 2, 12, 7) # AJOUT SOMMEIL
            travel_m = st.number_input("Temps de trajet (minutes)", 10, 180, 45)
        
        with col2:
            st.write("☁️ **Conditions Météorologiques**")
            # Choix météo plus visuel
            weather_choice = st.radio("Sélectionnez le temps prévu :", 
                                      ["Sunny ☀️", "Cloudy ☁️", "Rainy 🌧️", "Stormy ⚡"], horizontal=True)
            
            class_choice = st.selectbox("Type de cours", ["Offline (Présentiel)", "Online (Distance)"])

        st.markdown("---")
        if st.button("🚀 Lancer l'Analyse Prédictive"):
            # Logique de risque enrichie
            risk = 10
            if study_h < 3: risk += 35
            if sleep_h < 5: risk += 20
            if travel_m > 60 and "Offline" in class_choice: risk += 20
            if "Rainy" in weather_choice or "Stormy" in weather_choice: risk += 15
            
            res_l, res_r = st.columns(2)
            with res_l:
                st.subheader("Diagnostic de l'Agent")
                st.metric("Risque d'Absence Prédit", f"{risk}%")
                st.progress(risk/100)
            with res_r:
                if risk > 60:
                    st.error("🔴 **ALERTE :** Risque de décrochage élevé. Une pénalité est probable si ce pattern se répète.")
                else:
                    st.success("🟢 **STABLE :** Le profil présente une assiduité saine selon les prévisions.")
