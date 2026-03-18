import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION ÉLÉGANTE ---
st.set_page_config(page_title="Vigil-AI | ESI Command Center", layout="wide", page_icon="🛡️")

# CSS Custom : Design "Aérospatial" (Sombre, néon, épuré)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.5);
        border-left: 5px solid #58a6ff;
        padding: 20px; border-radius: 10px;
    }
    .penalty-card {
        background: linear-gradient(145deg, #1f2428, #0d1117);
        border: 1px solid #30363d;
        padding: 25px; border-radius: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE DE DONNÉES ---
@st.cache_data
def load_data():
    return pd.read_csv('Attendance_Prediction.csv')

df = load_data()

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/shield.png", width=80)
    st.title("Vigil-AI ESI")
    page = st.radio("Pilotage :", ["📊 Direction & KPI", "👤 Suivi Étudiant 360°", "🧠 Agent IA Expert"])
    st.markdown("---")
    st.caption("Règle ESI : Sanction après $16$ séances d'absence.")

# --- 4. PAGE 1 : DIRECTION & KPI ---
if page == "📊 Direction & KPI":
    st.title("📊 Tableau de Bord de Gouvernance")
    
    # KPIs Globaux
    c1, c2, c3 = st.columns(3)
    c1.metric("Taux d'Assiduité Global", f"{df['attendance'].mean()*100:.1f}%")
    
    # Calcul des étudiants proches de la pénalité (ex: > 10 absences)
    absences_par_eleve = df[df['attendance'] == 0].groupby('student_id').size()
    critiques = len(absences_par_eleve[absences_par_eleve >= 10])
    
    c2.metric("Étudiants à Risque (>10 abs)", f"{critiques}", delta="Attention", delta_color="inverse")
    c3.metric("JH Économisés", f"{int(len(df)*5/480)} JH")

    st.markdown("### 📈 Analyse des Flux")
    fig = px.area(df.groupby('course')['attendance'].mean().reset_index(), 
                  x="course", y="attendance", title="Stabilité par Filière")
    st.plotly_chart(fig, use_container_width=True)

# --- 5. PAGE 2 : SUIVI ÉTUDIANT 360° (TA DEMANDE) ---
elif page == "👤 Suivi Étudiant 360°":
    st.title("👤 Dossier Individuel Prédictif")
    
    # Sélection de l'élève
    student_list = df['student_id'].unique()
    selected_id = st.selectbox("Rechercher un étudiant (ID) :", student_list)
    
    student_data = df[df['student_id'] == selected_id]
    total_absences = len(student_data[student_data['attendance'] == 0])
    total_sessions = len(student_data)
    absence_rate = (total_absences / total_sessions) * 100
    
    # Interface en colonnes
    col_info, col_gauge = st.columns([1.5, 1])
    
    with col_info:
        st.markdown(f"### État du Dossier : ID {selected_id}")
        
        # Jauge de Pénalité ESI (Seuil 16)
        remaining = 16 - total_absences
        if remaining > 0:
            st.write(f"📉 **Absences cumulées :** {total_absences} / $16$")
            st.progress(total_absences / 16)
            st.info(f"Il reste **{remaining} séances** avant la pénalité administrative.")
        else:
            st.error(f"🚨 **STATUT : PÉNALISÉ** ({total_absences} absences enregistrées)")
            st.progress(1.0)

        # Pattern Dynamique
        st.markdown("#### 🔍 Détection de Pattern par l'Agent")
        pattern_data = student_data[student_data['attendance'] == 0]
        if not pattern_data.empty:
            top_reason = pattern_data['absence_reason'].mode()[0]
            top_weather = pattern_data['weather'].mode()[0]
            st.warning(f"L'agent identifie un pattern lié à : **{top_reason}** par temps **{top_weather}**.")

    with col_gauge:
        # Risque d'absence à la PROCHAINE séance
        # Simulation basée sur l'historique de l'élève
        risk_next = (absence_rate * 1.2) if absence_rate < 80 else 99
        
        fig_risk = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_next,
            title = {'text': "Risque Prochaine Séance (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#f85149" if risk_next > 50 else "#238636"}}
        ))
        fig_risk.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_risk, use_container_width=True)

# --- 6. PAGE 3 : AGENT IA EXPERT ---
elif page == "🧠 Agent IA Expert":
    st.title("🧠 Simulateur de l'Agent Vigil-AI")
    st.write("Testez la réactivité de l'agent face à des conditions externes.")
    
    with st.container():
        c1, c2 = st.columns(2)
        study = c1.slider("Heures d'étude", 0, 12, 5)
        travel = c2.number_input("Temps de trajet (min)", 10, 180, 45)
        weather = st.select_slider("Météo", options=["Sunny", "Cloudy", "Rainy", "Stormy"])
        
        if st.button("Lancer le Diagnostic Global"):
            risk_score = 15
            if study < 3: risk_score += 40
            if travel > 60: risk_score += 20
            if weather in ["Rainy", "Stormy"]: risk_score += 25
            
            st.subheader(f"Score de vulnérabilité : {risk_score}%")
            if risk_score > 60:
                st.error("🚨 Alerte : Risque de décrochage élevé détecté.")
            else:
                st.success("✅ État : Comportement jugé stable.")
