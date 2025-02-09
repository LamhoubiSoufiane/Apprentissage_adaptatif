import json
from pathlib import Path

class UserAgent:
    def __init__(self):
        self.capteurs_file = Path(__file__).parent.parent / "data" / "capteurs.json"
        self.preferences_file = Path(__file__).parent.parent / "data" / "preferences.json"
        self.init_preferences()

    def init_preferences(self):
        """Initialise le fichier des préférences utilisateur s'il n'existe pas"""
        if not self.preferences_file.exists():
            default_preferences = {
                "temperature": {
                    "Salon": 21.0,
                    "Chambre": 19.0
                },
                "luminosite": {
                    "Salon": 400,
                    "Cuisine": 500
                },
                "notifications": True,
                "mode_eco": True
            }
            with open(self.preferences_file, "w", encoding='utf-8') as file:
                json.dump(default_preferences, file, indent=4, ensure_ascii=False)

    def get_preferences(self):
        """Récupère les préférences utilisateur"""
        with open(self.preferences_file, "r", encoding='utf-8') as file:
            return json.load(file)

    def modifier_preference(self, capteur_id, nouvelle_valeur):
        """Modifie la valeur d'un capteur spécifique"""
        with open(self.capteurs_file, "r", encoding='utf-8') as file:
            data = json.load(file)

        updated = False
        for capteur in data["capteurs"]:
            if capteur["id"] == capteur_id:
                old_value = capteur["valeur"]
                capteur["valeur"] = nouvelle_valeur
                print(f"✅ La valeur du capteur {capteur_id} a été mise à jour de {old_value} à {nouvelle_valeur} {capteur['unite']}")
                updated = True
                break

        if updated:
            with open(self.capteurs_file, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        else:
            print(f"❌ Capteur {capteur_id} non trouvé")
            return False

    def set_room_temperature(self, room, temperature):
        """Définit la température souhaitée pour une pièce"""
        preferences = self.get_preferences()
        preferences["temperature"][room] = temperature
        with open(self.preferences_file, "w", encoding='utf-8') as file:
            json.dump(preferences, file, indent=4, ensure_ascii=False)
        
        # Mettre à jour le capteur correspondant
        capteur_id = f"temp_{room.lower()}"
        self.modifier_preference(capteur_id, temperature)

    def set_room_light(self, room, light_level):
        """Définit le niveau de luminosité souhaité pour une pièce"""
        preferences = self.get_preferences()
        preferences["luminosite"][room] = light_level
        with open(self.preferences_file, "w", encoding='utf-8') as file:
            json.dump(preferences, file, indent=4, ensure_ascii=False)
        
        # Mettre à jour le capteur correspondant
        capteur_id = f"lum_{room.lower()}"
        self.modifier_preference(capteur_id, light_level)

    def toggle_eco_mode(self, enabled):
        """Active ou désactive le mode éco"""
        preferences = self.get_preferences()
        preferences["mode_eco"] = enabled
        with open(self.preferences_file, "w", encoding='utf-8') as file:
            json.dump(preferences, file, indent=4, ensure_ascii=False)
        
        if enabled:
            # Réduire la consommation des appareils
            self.appliquer_mode_eco()

    def appliquer_mode_eco(self):
        """Applique les réglages du mode éco"""
        with open(self.capteurs_file, "r", encoding='utf-8') as file:
            data = json.load(file)

        for capteur in data["capteurs"]:
            if capteur["type"] == "température":
                # Réduire la température de 2 degrés
                capteur["valeur"] = max(18, capteur["valeur"] - 2)
            elif capteur["type"] == "luminosité":
                # Réduire la luminosité de 20%
                capteur["valeur"] = int(capteur["valeur"] * 0.8)

        with open(self.capteurs_file, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_consumption_alerts(self):
        """Récupère les alertes de consommation"""
        alerts = []
        with open(self.capteurs_file, "r", encoding='utf-8') as file:
            data = json.load(file)

        for capteur in data["capteurs"]:
            if capteur["type"] == "consommation":
                if capteur["valeur"] > 2.0:
                    alerts.append({
                        "device": capteur["appareil"],
                        "location": capteur["emplacement"],
                        "consumption": capteur["valeur"],
                        "message": f"⚠️ Consommation élevée : {capteur['appareil']} ({capteur['valeur']} kWh)"
                    })

        return alerts
