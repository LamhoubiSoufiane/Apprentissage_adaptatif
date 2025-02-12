import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
import time
import json
from datetime import datetime

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from agents.crew_agents import AdaptiveLearningCrewAgents

# Configuration de la page
st.set_page_config(
    page_title="Adaptive Learning Dashboard",
    page_icon="📚",
    layout="wide"
)

# Initialisation des agents
crew_agents = AdaptiveLearningCrewAgents()

# Titre
st.title("📚 Système d'Apprentissage Adaptatif")

# Sidebar - Partie 1 : ID Étudiant
with st.sidebar:
    st.header("Configuration")
    student_id = st.text_input("ID Étudiant", "STUDENT001")

# Gestion de l'état de la session
if "current_student_id" not in st.session_state or st.session_state.current_student_id != student_id:
    st.session_state.current_student_id = student_id
    # Réinitialiser l'état pour le nouvel étudiant
    st.session_state.show_questionnaire = True
    if "learning_style" in st.session_state:
        del st.session_state.learning_style

# Vérification du style d'apprentissage
if "learning_style" not in st.session_state:
    learning_style = crew_agents.student_manager.get_learning_style(student_id)
    if learning_style:
        st.session_state.learning_style = learning_style
        st.session_state.show_questionnaire = False

# Sidebar - Partie 2 : Autres configurations
with st.sidebar:
    # Sélection de la matière et du module
    st.subheader("Sélection du Cours")
    selected_subject = st.selectbox(
        "Matière",
        ["Mathématiques", "Physique", "Chimie", "Informatique", "Langues"]
    )
    
    # Modules spécifiques selon la matière
    modules = {
        "Mathématiques": ["Algèbre", "Analyse", "Géométrie", "Probabilités", "Statistiques"],
        "Physique": ["Mécanique", "Électricité", "Optique", "Thermodynamique", "Quantique"],
        "Chimie": ["Chimie organique", "Chimie inorganique", "Biochimie", "Chimie analytique"],
        "Informatique": ["Programmation", "Algorithmes", "Bases de données", "Réseaux", "IA"],
        "Langues": ["Grammaire", "Vocabulaire", "Expression orale", "Compréhension"]
    }
    
    selected_module = st.selectbox(
        "Module spécifique",
        modules.get(selected_subject, ["Général"])
    )
    
    # Préférences d'apprentissage supplémentaires
    st.subheader("Préférences d'Apprentissage")
    
    # Niveau de difficulté souhaité
    desired_difficulty = st.slider(
        "Niveau de difficulté souhaité",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Débutant, 5 = Expert"
    )
    
    # Durée de session préférée
    preferred_duration = st.select_slider(
        "Durée de session préférée (minutes)",
        options=[15, 30, 45, 60, 90, 120],
        value=30
    )
    
    # Type de contenu préféré
    preferred_content_types = st.multiselect(
        "Types de contenu préférés",
        ["Vidéos", "Documents PDF", "Exercices interactifs", "Audio", "Quiz"],
        default=["Vidéos", "Exercices interactifs"]
    )
    
    # Objectifs d'apprentissage
    st.subheader("Objectifs")
    learning_goal = st.text_area(
        "Décrivez vos objectifs d'apprentissage",
        placeholder="Ex: Je souhaite comprendre les concepts de base de l'algèbre linéaire..."
    )

# Affichage du questionnaire ou du contenu principal
if st.session_state.show_questionnaire:
    st.header("🎯 Détermination du Style d'Apprentissage")
    st.write("Pour personnaliser votre expérience d'apprentissage, veuillez répondre à ce court questionnaire.")
    
    questionnaire = crew_agents.student_manager.get_learning_style_questionnaire()
    answers = []
    
    for question in questionnaire["questions"]:
        choice = st.radio(
            question["text"],
            options=[choice["text"] for choice in question["choices"]],
            key=f"q_{question['id']}"
        )
        selected_choice = next(c for c in question["choices"] if c["text"] == choice)
        answers.append(selected_choice["id"])
    
    if st.button("Soumettre le Questionnaire"):
        learning_style = crew_agents.student_manager.get_learning_style(student_id, answers)
        crew_agents.student_manager.save_learning_style(student_id, learning_style)
        st.success("Style d'apprentissage déterminé avec succès !")
        st.info(f"Votre style d'apprentissage dominant est : {learning_style}")
        
        # Mettre à jour l'état de la session
        st.session_state.show_questionnaire = False
        st.session_state.learning_style = learning_style
        
        # Forcer le rechargement de la page
        st.rerun()

else:
    # Récupérer le style d'apprentissage de la session
    learning_style = st.session_state.learning_style

# Layout principal avec les nouvelles informations
col1, col2 = st.columns(2)

# Profil d'apprentissage
with col1:
    st.subheader("Profil d'Apprentissage")
    
    # Style d'apprentissage
    with st.expander("🎯 Style d'Apprentissage", expanded=True):
        st.info(f"Style d'apprentissage dominant : {learning_style}")
        
        # Récupérer les détails du style d'apprentissage
        with open(crew_agents.student_manager.students_file, "r", encoding='utf-8') as f:
            students_data = json.load(f)
            student = next((s for s in students_data["students"] if s["id"] == student_id), None)
            if student and "learning_style_details" in student:
                details = student["learning_style_details"]
                
                # Afficher les pourcentages pour chaque style
                st.write("**Répartition des styles d'apprentissage :**")
                for style, percentage in details["style_percentages"].items():
                    st.progress(percentage / 100)
                    st.write(f"{style.capitalize()}: {percentage:.1f}%")
                
                # Afficher les styles secondaires
                st.write("**Styles secondaires :**")
                for style, pct in details["secondary_styles"]:
                    st.write(f"- {style.capitalize()}: {pct:.1f}%")
                
                # Date de la dernière mise à jour
                st.write(f"*Dernière mise à jour : {datetime.fromisoformat(student['learning_style_updated']).strftime('%d/%m/%Y')}*")
                
                # Bouton pour refaire le questionnaire
                if st.button("Refaire le questionnaire"):
                    st.session_state.redo_questionnaire = True
                    st.rerun()
    
    # Afficher les préférences sélectionnées
    st.subheader("Préférences Actuelles")
    st.write(f"**Module:** {selected_module} ({selected_subject})")
    st.write(f"**Niveau souhaité:** {desired_difficulty}/5")
    st.write(f"**Durée de session:** {preferred_duration} minutes")
    st.write("**Types de contenu préférés:**")
    for content_type in preferred_content_types:
        st.write(f"- {content_type}")
    
    if learning_goal:
        st.write("**Objectifs:**")
        st.write(learning_goal)
    
    # Performance globale
    performance = crew_agents.student_manager.analyze_performance(student_id)
    if "status" not in performance:
        col_perf1, col_perf2, col_perf3 = st.columns(3)
        with col_perf1:
            st.metric("Score Moyen", f"{performance['average_score']:.2f}")
        with col_perf2:
            st.metric("Taux de Complétion", f"{performance['completion_rate']:.1f}%")
        with col_perf3:
            st.metric("Temps Total", f"{performance['time_spent']/60:.1f}h")

        # Points forts et faibles
        st.subheader("Points Forts")
        for subject in performance["strengths"]["strong_subjects"]:
            st.success(f"✓ {subject}")
        
        st.subheader("Points à Améliorer")
        for subject in performance["weaknesses"]["weak_subjects"]:
            st.warning(f"⚠ {subject}")

# Recommandations de contenu
with col2:
    st.subheader("Contenu Recommandé")
    
    # Préparer les préférences utilisateur
    user_preferences = {
        "module": selected_module,
        "difficulty": desired_difficulty,
        "duration": preferred_duration,
        "content_types": preferred_content_types,
        "learning_goal": learning_goal
    }
    
    recommendations = crew_agents.content_manager.recommend_content(
        student_id, 
        subject=selected_subject,
        preferences=user_preferences
    )
    
    for content in recommendations:
        with st.expander(f"📖 {content['title']} ({content['module']})"):
            col_content1, col_content2 = st.columns([2, 1])
            
            with col_content1:
                st.write(f"**Type:** {content['type']}")
                st.write(f"**Niveau:** {content['difficulty']}/5")
                st.write(f"**Description:** {content['description']}")
                
                # Afficher les objectifs
                st.write("**Objectifs:**")
                for obj in content['objectives']:
                    st.write(f"- {obj}")
                
                # Afficher les prérequis
                if 'prerequisites' in content and content['prerequisites']:
                    st.write("**Prérequis:**")
                    for prereq in content['prerequisites']:
                        st.write(f"- {prereq}")
            
            with col_content2:
                st.write(f"**Durée:** {content['duration']} minutes")
                
                # Afficher la ressource principale selon le type
                st.write("**Ressource Principale:**")
                if content['resource_type'] == 'video':
                    st.video(content['resource_url'])
                else:
                    st.write(f"[Accéder à la ressource]({content['resource_url']})")
                
                # Afficher les ressources complémentaires
                if 'additional_resources' in content and content['additional_resources']:
                    st.write("**Ressources Complémentaires:**")
                    for resource in content['additional_resources']:
                        st.write(f"- [{resource['type'].title()}]({resource['url']})")
            
            # Afficher les prochaines étapes
            if 'next_steps' in content and content['next_steps']:
                st.write("**Prochaines étapes suggérées:**")
                for step in content['next_steps']:
                    st.write(f"- {step}")
            
            # Bouton pour commencer
            if st.button("Commencer", key=content['id']):
                st.session_state.selected_content = content['id']

# Suivi des progrès
st.subheader("Suivi des Progrès")
progress_data = crew_agents.student_manager.track_progress(student_id)
if progress_data:
    df_progress = pd.DataFrame(progress_data)
    
    # Graphique des scores
    fig_scores = px.line(
        df_progress,
        x="timestamp",
        y="score",
        title="Évolution des Scores"
    )
    st.plotly_chart(fig_scores, use_container_width=True)
    
    # Graphique du taux de complétion
    fig_completion = px.line(
        df_progress,
        x="timestamp",
        y="completion_rate",
        title="Taux de Complétion"
    )
    st.plotly_chart(fig_completion, use_container_width=True)

# Support du tuteur virtuel
st.subheader("Support du Tuteur Virtuel")
col_tutor1, col_tutor2 = st.columns(2)

with col_tutor1:
    st.subheader("Difficultés Identifiées")
    struggles = crew_agents.tutor_manager.identify_struggles(student_id)
    if struggles:
        for subject, score in struggles["difficult_subjects"].items():
            st.error(f"{subject}: Score moyen de {score:.2f}")

with col_tutor2:
    st.subheader("Exercices Recommandés")
    exercises = crew_agents.tutor_manager.suggest_exercises(student_id, selected_subject)
    for exercise in exercises:
        with st.expander(f"📝 {exercise['subject']} - {exercise['difficulty']}"):
            st.write(f"**Durée recommandée:** {exercise['recommended_duration']} minutes")
            st.write("**Points à travailler:**")
            for area in exercise['focus_areas']:
                st.write(f"- {area}")

# Feedback en temps réel
if "selected_content" in st.session_state:
    st.subheader("Feedback sur la Session")
    feedback = crew_agents.tutor_manager.provide_feedback(
        student_id,
        st.session_state.selected_content
    )
    
    if "status" not in feedback:
        st.write("**Performance:**")
        col_feed1, col_feed2, col_feed3 = st.columns(3)
        with col_feed1:
            st.metric("Score", f"{feedback['performance_summary']['current_performance']['score']:.2f}")
        with col_feed2:
            st.metric("Complétion", f"{feedback['performance_summary']['current_performance']['completion_rate']:.1f}%")
        with col_feed3:
            st.metric("Temps", f"{feedback['performance_summary']['current_performance']['time_spent']} min")
        
        st.write("**Recommandations:**")
        for rec in feedback["recommendations"]:
            st.info(rec)
