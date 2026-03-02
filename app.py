import streamlit as st


st.set_page_config(
    page_title="Gestión de Vehículos Universidad",
    page_icon="🚗",
    layout="wide"
)

# Importar módulos de datos
from data.gestion_datos import inicializar_archivos

# Inicializar archivos de datos si no existen
inicializar_archivos()

# --- INTERFAZ DE USUARIO ---

# Redirigir automáticamente al calendario de reservas
st.switch_page("pages/1_Calendario_Reservas.py")
