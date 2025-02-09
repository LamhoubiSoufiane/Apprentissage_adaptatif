from crewai import Agent
from langchain_openai import ChatOpenAI
from .sensor_agent import SensorAgent
from .scheduler_agent import SchedulerAgent
from .user_agent import UserAgent

class SmartHomeCrewAgents:
    def __init__(self):
        # Initialiser le modèle OpenAI
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7
        )
        
        # Initialiser les agents spécialisés
        self.sensor_manager = SensorAgent()
        self.scheduler_manager = SchedulerAgent()
        self.user_manager = UserAgent()

    def create_sensor_agent(self):
        """Crée l'agent responsable des capteurs"""
        return Agent(
            role='Sensor Specialist',
            goal='Monitor and analyze home environmental data with AI assistance',
            backstory='Expert in IoT sensors and data analysis using AI',
            tools=[
                {
                    'name': 'read_sensors',
                    'description': 'Read current sensor values',
                    'func': self.sensor_manager.lire_capteurs
                },
                {
                    'name': 'update_sensors',
                    'description': 'Update sensor values',
                    'func': self.sensor_manager.mettre_a_jour_capteurs
                },
                {
                    'name': 'get_sensor_by_id',
                    'description': 'Get specific sensor data by ID',
                    'func': self.sensor_manager.get_sensor_by_id
                }
            ],
            verbose=True,
            llm=self.llm
        )

    def create_scheduler_agent(self):
        """Crée l'agent responsable de la planification"""
        return Agent(
            role='Energy Optimizer',
            goal='Optimize energy usage using AI-powered scheduling',
            backstory='Expert in AI-driven energy management and optimization',
            tools=[
                {
                    'name': 'adjust_schedules',
                    'description': 'Adjust device schedules to optimize energy usage',
                    'func': self.scheduler_manager.ajuster_horaires
                },
                {
                    'name': 'get_device_schedule',
                    'description': 'Get schedule for a specific device',
                    'func': self.scheduler_manager.get_device_schedule
                },
                {
                    'name': 'get_all_schedules',
                    'description': 'Get all device schedules',
                    'func': self.scheduler_manager.get_all_schedules
                }
            ],
            verbose=True,
            llm=self.llm
        )

    def create_user_agent(self):
        """Crée l'agent responsable de l'interface utilisateur"""
        return Agent(
            role='User Experience Specialist',
            goal='Understand and implement user preferences with AI assistance',
            backstory='Expert in AI-powered comfort optimization and user experience',
            tools=[
                {
                    'name': 'get_preferences',
                    'description': 'Get user preferences',
                    'func': self.user_manager.get_preferences
                },
                {
                    'name': 'modify_preference',
                    'description': 'Modify user preference for a sensor',
                    'func': self.user_manager.modifier_preference
                },
                {
                    'name': 'get_consumption_alerts',
                    'description': 'Get alerts about high energy consumption',
                    'func': self.user_manager.get_consumption_alerts
                }
            ],
            verbose=True,
            llm=self.llm
        )

    def start_monitoring(self):
        """Démarre la surveillance continue des capteurs"""
        self.sensor_manager.start(intervalle=2)

    def stop_monitoring(self):
        """Arrête la surveillance des capteurs"""
        self.sensor_manager.stop()
