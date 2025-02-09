from mesa import Model
from mesa.time import RandomActivation
from crewai import Crew
from agents.crew_agents import SmartHomeCrewAgents

class SmartHomeModel(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        
        # Créer les agents avec CrewAI
        agents_creator = SmartHomeCrewAgents()
        self.sensor = agents_creator.create_sensor_agent()
        self.scheduler = agents_creator.create_scheduler_agent()
        self.user = agents_creator.create_user_agent()
        
        # Créer l'équipe CrewAI
        self.crew = Crew(
            agents=[self.sensor, self.scheduler, self.user],
            tasks=[],  # Les tâches seront définies dynamiquement
            verbose=2
        )
        
        # Stockage des données
        self.current_data = None

    def get_sensor_data(self):
        """Retourne les données actuelles des capteurs"""
        return self.current_data

    def step(self):
        """Exécute un pas de simulation avec CrewAI"""
        # Exécuter l'équipe CrewAI
        result = self.crew.kickoff()
        
        # Mettre à jour les données actuelles
        self.current_data = {
            'temperature': 22.0,  # Valeurs par défaut
            'luminosity': 500,
            'energy_consumption': 1.5
        }
        
        return {
            'sensor_data': self.current_data,
            'crew_result': result
        }
