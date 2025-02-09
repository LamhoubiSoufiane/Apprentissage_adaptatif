import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Smart Home Dashboard",
    page_icon="🏠",
    layout="wide"
)

# Titre
st.title("🏠 Smart Home Dashboard")

# Fonction pour générer des données simulées
def generate_mock_data(n_points=24):
    now = datetime.now()
    dates = [now - timedelta(hours=x) for x in range(n_points)]
    
    return pd.DataFrame({
        'timestamp': dates,
        'temperature': [random.uniform(18, 25) for _ in range(n_points)],
        'humidity': [random.uniform(30, 70) for _ in range(n_points)],
        'energy_consumption': [random.uniform(0.5, 2.5) for _ in range(n_points)],
        'light_intensity': [random.uniform(200, 800) for _ in range(n_points)],
        'air_quality': [random.uniform(0, 100) for _ in range(n_points)]
    })

# Générer des données simulées
data = generate_mock_data()

# Layout en colonnes
col1, col2 = st.columns(2)

# Graphique de température et humidité
with col1:
    st.subheader("Temperature & Humidity")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['temperature'],
        name='Temperature (°C)',
        line=dict(color='#FF9F1C')
    ))
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['humidity'],
        name='Humidity (%)',
        line=dict(color='#2EC4B6'),
        yaxis='y2'
    ))
    fig.update_layout(
        yaxis2=dict(
            title='Humidity (%)',
            overlaying='y',
            side='right'
        ),
        yaxis=dict(title='Temperature (°C)'),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Graphique de consommation d'énergie
with col2:
    st.subheader("Energy Consumption")
    fig = px.line(
        data,
        x='timestamp',
        y='energy_consumption',
        title='Energy Usage (kWh)',
        line_shape='spline'
    )
    fig.update_traces(line_color='#E71D36')
    st.plotly_chart(fig, use_container_width=True)

# Deuxième rangée
col3, col4 = st.columns(2)

# Graphique d'intensité lumineuse
with col3:
    st.subheader("Light Intensity")
    fig = px.area(
        data,
        x='timestamp',
        y='light_intensity',
        title='Light Levels (lux)',
        line_shape='spline'
    )
    fig.update_traces(line_color='#FFD700', fill='tonexty')
    st.plotly_chart(fig, use_container_width=True)

# Graphique de qualité de l'air
with col4:
    st.subheader("Air Quality")
    current_aqi = data['air_quality'].iloc[-1]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_aqi,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2EC4B6"},
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "red"}
            ],
        }
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Statistiques en temps réel
st.subheader("Real-time Statistics")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Current Temperature",
        f"{data['temperature'].iloc[-1]:.1f}°C",
        f"{(data['temperature'].iloc[-1] - data['temperature'].iloc[-2]):.1f}°C"
    )

with col6:
    st.metric(
        "Current Humidity",
        f"{data['humidity'].iloc[-1]:.1f}%",
        f"{(data['humidity'].iloc[-1] - data['humidity'].iloc[-2]):.1f}%"
    )

with col7:
    st.metric(
        "Energy Usage",
        f"{data['energy_consumption'].iloc[-1]:.2f} kWh",
        f"{(data['energy_consumption'].iloc[-1] - data['energy_consumption'].iloc[-2]):.2f} kWh"
    )

with col8:
    st.metric(
        "Air Quality Index",
        f"{data['air_quality'].iloc[-1]:.0f}",
        f"{(data['air_quality'].iloc[-1] - data['air_quality'].iloc[-2]):.0f}"
    )

# Recommandations
st.subheader("Smart Recommendations")
with st.expander("View Recommendations"):
    st.write("🌡️ Temperature is optimal for energy efficiency")
    st.write("💡 Consider reducing lighting in unused rooms")
    st.write("⚡ Peak energy usage expected in 2 hours")
    st.write("🌪️ Air quality is good, ventilation working properly")
