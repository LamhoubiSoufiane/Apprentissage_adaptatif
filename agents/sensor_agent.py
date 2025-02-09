import json
import random
import time
import threading
from pathlib import Path

class SensorAgent:
    def __init__(self):
        self.capteurs_file = Path(__file__).parent.parent / "data" / "capteurs.json"
        self.running = True
        self._lock = threading.Lock()

    def lire_capteurs(self):
        """Lit les données des capteurs depuis le fichier JSON"""
        with self._lock:
            with open(self.capteurs_file, "r", encoding='utf-8') as file:
                data = json.load(file)
            return data["capteurs"]

    def mettre_a_jour_capteurs(self):
        """Met à jour les valeurs des capteurs avec des données simulées"""
        with self._lock:
            with open(self.capteurs_file, "r", encoding='utf-8') as file:
                data = json.load(file)

            for capteur in data["capteurs"]:
                if capteur["type"] == "température":
                    capteur["valeur"] = round(random.uniform(18, 26), 1)
                elif capteur["type"] == "luminosité":
                    capteur["valeur"] = random.randint(100, 600)
                elif capteur["type"] == "consommation":
                    capteur["valeur"] = round(random.uniform(0.5, 2.5), 2)

            with open(self.capteurs_file, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return data["capteurs"]

    def mise_a_jour_en_continue(self, intervalle=2):
        """Met à jour continuellement les capteurs selon l'intervalle spécifié"""
        while self.running:
            self.mettre_a_jour_capteurs()
            time.sleep(intervalle)

    def start(self, intervalle=2):
        """Démarre la mise à jour continue des capteurs dans un thread séparé"""
        thread = threading.Thread(target=self.mise_a_jour_en_continue, args=(intervalle,))
        thread.daemon = True
        thread.start()

    def stop(self):
        """Arrête la mise à jour continue des capteurs"""
        self.running = False

    def get_sensor_by_id(self, sensor_id):
        """Récupère les données d'un capteur spécifique par son ID"""
        capteurs = self.lire_capteurs()
        for capteur in capteurs:
            if capteur["id"] == sensor_id:
                return capteur
        return None

    def get_sensors_by_type(self, sensor_type):
        """Récupère tous les capteurs d'un type spécifique"""
        capteurs = self.lire_capteurs()
        return [c for c in capteurs if c["type"] == sensor_type]

    def get_sensors_by_location(self, location):
        """Récupère tous les capteurs d'un emplacement spécifique"""
        capteurs = self.lire_capteurs()
        return [c for c in capteurs if c["emplacement"] == location]
