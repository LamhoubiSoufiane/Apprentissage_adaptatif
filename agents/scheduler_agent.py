import json
from pathlib import Path
from datetime import datetime, timedelta

class SchedulerAgent:
    def __init__(self):
        self.capteurs_file = Path(__file__).parent.parent / "data" / "capteurs.json"
        self.schedule_file = Path(__file__).parent.parent / "data" / "schedules.json"
        self.peak_hours = [(7, 9), (18, 22)]  # Heures de pointe (format: (début, fin))
        self.max_concurrent_devices = 2  # Nombre maximum d'appareils en fonctionnement simultané

    def load_schedules(self):
        """Charge les plannings existants"""
        if not self.schedule_file.exists():
            return {"schedules": []}
        
        with open(self.schedule_file, "r", encoding='utf-8') as file:
            return json.load(file)

    def save_schedules(self, schedules):
        """Sauvegarde les plannings"""
        with open(self.schedule_file, "w", encoding='utf-8') as file:
            json.dump(schedules, file, indent=4, ensure_ascii=False)

    def is_peak_hour(self, hour):
        """Vérifie si l'heure donnée est une heure de pointe"""
        for start, end in self.peak_hours:
            if start <= hour < end:
                return True
        return False

    def get_current_consumption(self):
        """Obtient la consommation totale actuelle"""
        with open(self.capteurs_file, "r", encoding='utf-8') as file:
            data = json.load(file)
        
        total_consumption = 0
        for capteur in data["capteurs"]:
            if capteur["type"] == "consommation":
                total_consumption += capteur["valeur"]
        return total_consumption

    def ajuster_horaires(self):
        """Ajuste les horaires des appareils pour optimiser la consommation"""
        current_hour = datetime.now().hour
        current_consumption = self.get_current_consumption()
        schedules = self.load_schedules()
        
        # Vérifier la consommation actuelle
        if current_consumption > 4.0:  # Seuil de consommation élevée
            print(f"⚠️ Alerte : Consommation élevée détectée ({current_consumption:.2f} kWh)")
            
            # Récupérer les appareils en cours d'utilisation
            with open(self.capteurs_file, "r", encoding='utf-8') as file:
                data = json.load(file)
            
            high_consumption_devices = []
            for capteur in data["capteurs"]:
                if capteur["type"] == "consommation" and capteur["valeur"] > 1.0:
                    high_consumption_devices.append(capteur)
            
            # Planifier le report des appareils énergivores
            for device in high_consumption_devices:
                new_schedule = {
                    "device_id": device["id"],
                    "device_name": device["appareil"],
                    "original_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "rescheduled_time": self.find_optimal_time(current_hour)
                }
                schedules["schedules"].append(new_schedule)
                print(f"📅 Appareil {device['appareil']} reporté à {new_schedule['rescheduled_time']}")
        
        self.save_schedules(schedules)
        return schedules["schedules"]

    def find_optimal_time(self, current_hour):
        """Trouve l'heure optimale pour reporter un appareil"""
        test_hour = current_hour
        max_test_hours = 24  # Limite de recherche
        
        while max_test_hours > 0:
            test_hour = (test_hour + 1) % 24
            if not self.is_peak_hour(test_hour):
                # Convertir en datetime pour le format de sortie
                optimal_time = datetime.now() + timedelta(hours=(test_hour - current_hour))
                return optimal_time.strftime("%Y-%m-%d %H:%M:%S")
            max_test_hours -= 1
        
        # Si aucune heure optimale n'est trouvée, retourner le lendemain à la même heure
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    def get_device_schedule(self, device_id):
        """Récupère le planning d'un appareil spécifique"""
        schedules = self.load_schedules()
        return [s for s in schedules["schedules"] if s["device_id"] == device_id]

    def get_all_schedules(self):
        """Récupère tous les plannings"""
        return self.load_schedules()["schedules"]
