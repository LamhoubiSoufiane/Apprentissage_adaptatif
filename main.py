from crewai import Crew, Task
from agents.crew_agents import SmartHomeCrewAgents
import streamlit as st
import time
import threading

def run_smart_home_crew():
    # Créer une instance de SmartHomeCrewAgents
    crew_agents = SmartHomeCrewAgents()
    
    # Obtenir les agents
    sensor_agent = crew_agents.create_sensor_agent()
    scheduler_agent = crew_agents.create_scheduler_agent()
    user_agent = crew_agents.create_user_agent()
    
    # Définir les tâches
    tasks = [
        Task(
            description="Collect and analyze environmental data",
            agent=sensor_agent,
            expected_output="Structured environmental data analysis report"
        ),
        Task(
            description="Create optimal device schedule based on collected data",
            agent=scheduler_agent,
            expected_output="Optimized device operation schedule"
        ),
        Task(
            description="Adjust settings based on user preferences",
            agent=user_agent,
            expected_output="User-customized device settings report"
        )
    ]
    
    # Créer l'équipage
    crew = Crew(
        agents=[sensor_agent, scheduler_agent, user_agent],
        tasks=tasks,
        verbose=True
    )

    # Démarrer la surveillance continue des capteurs
    crew_agents.start_monitoring()
    
    try:
        # Lancer l'exécution
        result = crew.kickoff()
        return result
    except KeyboardInterrupt:
        print("\nArrêt de la simulation...")
    finally:
        # Arrêter la surveillance des capteurs
        crew_agents.stop_monitoring()

def main():
    st.set_page_config(
        page_title="Smart Home System",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 Smart Home Management System")

    # Créer les agents
    crew_agents = SmartHomeCrewAgents()
    
    # Sidebar pour les contrôles
    with st.sidebar:
        st.header("Controls")
        if st.button("Start Monitoring", type="primary"):
            crew_agents.start_monitoring()
            st.success("Monitoring started!")
        
        if st.button("Stop Monitoring", type="secondary"):
            crew_agents.stop_monitoring()
            st.warning("Monitoring stopped!")

        st.header("User Preferences")
        room = st.selectbox("Select Room", ["Salon", "Chambre", "Cuisine"])
        temperature = st.slider("Temperature (°C)", 18, 28, 21)
        if st.button("Set Temperature"):
            crew_agents.user_manager.set_room_temperature(room, temperature)
            st.success(f"Temperature set to {temperature}°C for {room}")

        eco_mode = st.toggle("Eco Mode")
        if eco_mode:
            crew_agents.user_manager.toggle_eco_mode(True)
            st.info("Eco mode enabled")
        else:
            crew_agents.user_manager.toggle_eco_mode(False)

    # Layout principal
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Current Sensor Readings")
        sensor_data = crew_agents.sensor_manager.lire_capteurs()
        for sensor in sensor_data:
            st.metric(
                f"{sensor['appareil']} ({sensor['emplacement']})",
                f"{sensor['valeur']} {sensor['unite']}"
            )

    with col2:
        st.subheader("Energy Consumption Alerts")
        alerts = crew_agents.user_manager.get_consumption_alerts()
        if alerts:
            for alert in alerts:
                st.warning(alert['message'])
        else:
            st.success("No high consumption alerts")

    # Afficher les plannings
    st.subheader("Device Schedules")
    schedules = crew_agents.scheduler_manager.get_all_schedules()
    if schedules:
        for schedule in schedules:
            st.info(
                f"📅 {schedule['device_name']} rescheduled from "
                f"{schedule['original_time']} to {schedule['rescheduled_time']}"
            )
    else:
        st.info("No scheduled device operations")

    # Rafraîchissement automatique
    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
