import pandas as pd
from datetime import datetime

class DataHandler:
    def __init__(self):
        self.data = pd.DataFrame(columns=[
            'timestamp',
            'temperature',
            'luminosity',
            'energy_consumption',
            'comfort_score'
        ])

    def add_record(self, sensor_data, comfort_score):
        """Ajoute un nouvel enregistrement aux données"""
        new_record = {
            'timestamp': datetime.now(),
            'temperature': sensor_data['temperature'],
            'luminosity': sensor_data['luminosity'],
            'energy_consumption': sensor_data['energy_consumption'],
            'comfort_score': comfort_score
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_record])], ignore_index=True)

    def get_statistics(self, period='day'):
        """Calcule les statistiques pour une période donnée"""
        if self.data.empty:
            return None

        if period == 'day':
            grouped = self.data.groupby(self.data['timestamp'].dt.date)
        elif period == 'hour':
            grouped = self.data.groupby(self.data['timestamp'].dt.hour)
        else:
            return None

        return grouped.agg({
            'temperature': ['mean', 'min', 'max'],
            'luminosity': ['mean', 'min', 'max'],
            'energy_consumption': 'sum',
            'comfort_score': 'mean'
        })
