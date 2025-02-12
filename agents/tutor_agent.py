import json
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

class TutorAgent:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.learning_data_file = self.data_dir / "learning_data.json"
        self.feedback_file = self.data_dir / "feedback.json"
        self.init_data_files()

    def init_data_files(self):
        """Initialise les fichiers de données s'ils n'existent pas"""
        self.data_dir.mkdir(exist_ok=True)
        
        if not self.feedback_file.exists():
            default_feedback = {
                "feedback_records": []
            }
            with open(self.feedback_file, "w", encoding='utf-8') as f:
                json.dump(default_feedback, f, indent=4, ensure_ascii=False)

        # Initialiser les données d'apprentissage avec des données de test
        if not self.learning_data_file.exists():
            test_data = {
                "learning_records": [
                    {
                        "student_id": "STUDENT001",
                        "timestamp": datetime.now().isoformat(),
                        "subject": "Mathématiques",
                        "content_type": "visual",
                        "content_id": "MATH001",
                        "score": 0.85,
                        "completion_rate": 95,
                        "time_spent": 45,
                        "difficulty_level": 3,
                        "success_rate": 0.82,
                        "sub_topic": "Algèbre",
                        "exercise_type": "Problèmes"
                    },
                    {
                        "student_id": "STUDENT001",
                        "timestamp": datetime.now().isoformat(),
                        "subject": "Physique",
                        "content_type": "practical",
                        "content_id": "PHY001",
                        "score": 0.65,
                        "completion_rate": 80,
                        "time_spent": 60,
                        "difficulty_level": 4,
                        "success_rate": 0.60,
                        "sub_topic": "Mécanique",
                        "exercise_type": "Expériences"
                    },
                    {
                        "student_id": "STUDENT001",
                        "timestamp": datetime.now().isoformat(),
                        "subject": "Informatique",
                        "content_type": "practical",
                        "content_id": "INFO001",
                        "score": 0.92,
                        "completion_rate": 100,
                        "time_spent": 30,
                        "difficulty_level": 2,
                        "success_rate": 0.95,
                        "sub_topic": "Programmation",
                        "exercise_type": "Coding"
                    }
                ]
            }
            with open(self.learning_data_file, "w", encoding='utf-8') as f:
                json.dump(test_data, f, indent=4, ensure_ascii=False)

    def provide_feedback(self, student_id, content_id):
        """Fournit un feedback personnalisé et adaptatif"""
        # Charger les données d'apprentissage
        with open(self.learning_data_file, "r", encoding='utf-8') as f:
            learning_data = json.load(f)

        # Obtenir l'historique complet et les enregistrements spécifiques
        all_records = pd.DataFrame(learning_data["learning_records"])
        all_records['timestamp'] = pd.to_datetime(all_records['timestamp'])
        
        student_records = all_records[all_records["student_id"] == student_id]
        content_records = student_records[student_records["content_id"] == content_id]
        
        if content_records.empty:
            return {
                "status": "error",
                "message": "Aucune donnée disponible pour ce contenu"
            }

        # Analyse approfondie
        latest_record = content_records.iloc[-1]
        learning_context = self._analyze_learning_context(student_records, content_records)
        
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "student_id": student_id,
            "content_id": content_id,
            "performance_summary": self._generate_performance_summary(latest_record, learning_context),
            "progress_analysis": self._analyze_progress(content_records),
            "learning_insights": self._generate_learning_insights(student_records, content_records),
            "recommendations": self._generate_adaptive_recommendations(student_records, content_records),
            "next_steps": self._suggest_next_steps(student_records, content_records)
        }

        # Sauvegarder le feedback
        self._save_feedback(feedback)
        return feedback

    def _analyze_learning_context(self, student_records, content_records):
        """Analyse le contexte d'apprentissage complet"""
        return {
            "overall_progress": self._calculate_overall_progress(student_records),
            "content_mastery": self._evaluate_content_mastery(content_records),
            "learning_velocity": self._calculate_learning_velocity(student_records),
            "engagement_level": self._evaluate_engagement(student_records),
            "challenge_level": self._assess_challenge_level(content_records)
        }

    def _generate_performance_summary(self, latest_record, context):
        """Génère un résumé détaillé des performances"""
        return {
            "current_performance": {
                "score": latest_record["score"],
                "completion_rate": latest_record["completion_rate"],
                "time_spent": latest_record["time_spent"]
            },
            "relative_performance": self._calculate_relative_performance(latest_record, context),
            "mastery_level": self._calculate_mastery_level(latest_record, context),
            "improvement_areas": self._identify_improvement_areas(latest_record, context)
        }

    def _analyze_progress(self, content_records):
        """Analyse détaillée des progrès"""
        return {
            "learning_curve": self._analyze_learning_curve(content_records),
            "skill_development": self._analyze_skill_development(content_records),
            "knowledge_gaps": self._identify_knowledge_gaps(content_records),
            "mastery_trends": self._analyze_mastery_trends(content_records)
        }

    def _generate_learning_insights(self, student_records, content_records):
        """Génère des insights personnalisés sur l'apprentissage"""
        return {
            "strengths": self._identify_learning_strengths(student_records),
            "challenges": self._identify_learning_challenges(content_records),
            "learning_style_effectiveness": self._evaluate_learning_style(student_records),
            "engagement_patterns": self._analyze_engagement_patterns(student_records)
        }

    def _generate_adaptive_recommendations(self, student_records, content_records):
        """Génère des recommandations adaptatives"""
        recommendations = []
        
        # Analyser les besoins spécifiques
        needs = self._identify_specific_needs(student_records, content_records)
        
        # Recommandations basées sur le niveau de maîtrise
        mastery_level = self._calculate_mastery_level(content_records.iloc[-1], {})
        if mastery_level < 0.6:
            recommendations.append(self._generate_reinforcement_recommendation(content_records))
        elif mastery_level < 0.8:
            recommendations.append(self._generate_practice_recommendation(content_records))
        else:
            recommendations.append(self._generate_advancement_recommendation(content_records))

        # Recommandations basées sur le style d'apprentissage
        learning_style = self._evaluate_learning_style(student_records)
        recommendations.append(self._generate_style_based_recommendation(learning_style))

        # Recommandations pour l'engagement
        engagement_level = self._evaluate_engagement(student_records)
        if engagement_level < 0.7:
            recommendations.append(self._generate_engagement_recommendation(student_records))

        return recommendations

    def _suggest_next_steps(self, student_records, content_records):
        """Suggère les prochaines étapes d'apprentissage"""
        mastery_level = self._calculate_mastery_level(content_records.iloc[-1], {})
        learning_pace = self._calculate_learning_velocity(student_records)
        
        next_steps = []
        
        if mastery_level < 0.6:
            next_steps.append({
                "type": "revision",
                "focus": self._identify_revision_areas(content_records),
                "suggested_duration": self._calculate_optimal_duration(student_records),
                "resources": self._suggest_revision_resources(content_records)
            })
        elif mastery_level < 0.8:
            next_steps.append({
                "type": "practice",
                "exercises": self._suggest_practice_exercises(content_records),
                "difficulty_level": self._suggest_difficulty_level(student_records),
                "estimated_time": self._estimate_practice_time(student_records)
            })
        else:
            next_steps.append({
                "type": "advancement",
                "suggested_topics": self._suggest_advanced_topics(student_records),
                "challenge_level": self._suggest_challenge_level(student_records),
                "preparation_steps": self._suggest_preparation_steps(student_records)
            })
        
        return next_steps

    def _calculate_mastery_level(self, record, context):
        """Calcule le niveau de maîtrise"""
        return (record["score"] * 0.4 + 
                record["completion_rate"] * 0.3 + 
                record["success_rate"] * 0.3)

    def identify_struggles(self, student_id):
        """Identifie les domaines où l'étudiant a des difficultés"""
        with open(self.learning_data_file, "r", encoding='utf-8') as f:
            learning_data = json.load(f)

        records = [r for r in learning_data["learning_records"] if r["student_id"] == student_id]
        if not records:
            return []

        df = pd.DataFrame(records)
        
        # Analyser les difficultés par sujet
        subject_performance = df.groupby("subject")["score"].mean()
        difficult_subjects = subject_performance[subject_performance < 0.6]

        # Analyser les types de contenu problématiques
        content_performance = df.groupby("content_type")["success_rate"].mean()
        difficult_content_types = content_performance[content_performance < 0.6]

        # Analyser le temps passé
        time_analysis = df.groupby("subject")["time_spent"].mean()
        time_intensive_subjects = time_analysis[time_analysis > time_analysis.mean() + time_analysis.std()]

        struggles = {
            "difficult_subjects": difficult_subjects.to_dict(),
            "problematic_content_types": difficult_content_types.to_dict(),
            "time_intensive_subjects": time_intensive_subjects.to_dict()
        }

        return struggles

    def suggest_exercises(self, student_id, subject=None):
        """Suggère des exercices ciblés basés sur les besoins de l'étudiant"""
        struggles = self.identify_struggles(student_id)
        
        # Charger les données d'apprentissage
        with open(self.learning_data_file, "r", encoding='utf-8') as f:
            learning_data = json.load(f)

        df = pd.DataFrame(learning_data["learning_records"])
        student_df = df[df["student_id"] == student_id]

        if subject:
            student_df = student_df[student_df["subject"] == subject]

        # Identifier le niveau de difficulté approprié
        avg_performance = student_df["score"].mean()
        if avg_performance < 0.6:
            target_difficulty = "facile"
        elif avg_performance < 0.75:
            target_difficulty = "moyen"
        else:
            target_difficulty = "difficile"

        # Générer des suggestions d'exercices
        suggestions = []
        for subject, score in struggles["difficult_subjects"].items():
            suggestions.append({
                "subject": subject,
                "difficulty": target_difficulty,
                "focus_areas": self._identify_focus_areas(student_df, subject),
                "recommended_duration": 30,  # minutes
                "practice_type": "intensive"
            })

        return suggestions

    def _generate_recommendations(self, df):
        """Génère des recommandations personnalisées basées sur les performances"""
        recommendations = []
        
        # Analyser le temps passé
        avg_time = df["time_spent"].mean()
        if avg_time > df["time_spent"].median() * 1.5:
            recommendations.append("Considérer des sessions d'étude plus courtes mais plus fréquentes")

        # Analyser les erreurs communes
        if "error_types" in df.columns:
            common_errors = df["error_types"].value_counts()
            if not common_errors.empty:
                recommendations.append(f"Concentrez-vous sur la correction de: {common_errors.index[0]}")

        # Analyser le rythme d'apprentissage
        completion_trend = df["completion_rate"].diff().mean()
        if completion_trend < 0:
            recommendations.append("Votre rythme ralentit, prenez le temps de revoir les concepts de base")

        return recommendations

    def _identify_focus_areas(self, df, subject):
        """Identifie les domaines spécifiques nécessitant plus d'attention"""
        subject_df = df[df["subject"] == subject]
        
        focus_areas = []
        
        # Analyser les sous-thèmes
        if "sub_topic" in subject_df.columns:
            weak_topics = subject_df.groupby("sub_topic")["score"].mean()
            weak_topics = weak_topics[weak_topics < 0.6]
            focus_areas.extend(weak_topics.index.tolist())

        # Analyser les types d'exercices
        if "exercise_type" in subject_df.columns:
            weak_types = subject_df.groupby("exercise_type")["score"].mean()
            weak_types = weak_types[weak_types < 0.6]
            focus_areas.extend(weak_types.index.tolist())

        return focus_areas 