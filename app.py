import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Vehículos Universidad",
    page_icon="🚗",
    layout="wide"
)

# Nombre del archivo para guardar las reservas
FILE_RESERVAS = "reservas.csv"

# Función para cargar los datos
def cargar_datos():
    if not os.path.exists(FILE_RESERVAS):
        # Si no existe, creamos un DataFrame vacío con las columnas necesarias
        df = pd.DataFrame(columns=["Fecha", "Vehículo", "Solicitante", "Área"])
        df.to_csv(FILE_RESERVAS, index=False)
        return df
    else:
        return pd.read_csv(FILE_RESERVAS)

# Función para guardar una nueva reserva
def guardar_reserva(fecha, vehiculo, solicitante, area):
    df = cargar_datos()
    nueva_fila = pd.DataFrame([[fecha, vehiculo, solicitante, area]], 
                              columns=["Fecha", "Vehículo", "Solicitante", "Área"])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_csv(FILE_RESERVAS, index=False)

# Lista de vehículos (10 vehículos)
vehiculos = ["Virtus", "Crafter", "Pick-up", "Urvan", "Versa"]

# --- INTERFAZ DE USUARIO ---

st.title("🚗 Calendario de Reserva de Vehículos")
st.markdown("Bienvenido al sistema de gestión de transporte. Consulta la disponibilidad o aparta un vehículo.")

# --- SECCIÓN SUPERIOR: DISPONIBILIDAD RÁPIDA ---
st.markdown("### 🚗 Disponibilidad Inmediata")

# Selector de fecha para consultar disponibilidad
fecha_consulta = st.date_input("Selecciona una fecha para ver disponibilidad:", value=date.today())

# Cargamos datos para verificar disponibilidad
df_temp = cargar_datos()
if not df_temp.empty:
    df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha']).dt.date

# Lógica para encontrar vehículos disponibles
vehiculos_ocupados = []
if not df_temp.empty:
    # Buscamos qué vehículos tienen reserva en la fecha seleccionada
    ocupados_hoy = df_temp[df_temp['Fecha'] == fecha_consulta]['Vehículo'].unique()
    vehiculos_ocupados = list(ocupados_hoy)

# Filtramos la lista total de vehículos excluyendo los ocupados
vehiculos_disponibles = [v for v in vehiculos if v not in vehiculos_ocupados]

# Mostramos los primeros 5 disponibles (o menos si no hay 5)
st.write(f"Vehículos libres para el {fecha_consulta}:")
if vehiculos_disponibles:
    # Usamos columns para mostrarlos en una fila bonita
    cols = st.columns(min(5, len(vehiculos_disponibles)))
    for i, v in enumerate(vehiculos_disponibles[:5]):
        cols[i].success(f"✅ {v}")
else:
    st.warning("⚠️ No hay vehículos disponibles para esta fecha.")


# Barra lateral para el formulario de reserva
with st.sidebar:
    st.header("📝 Nueva Reserva")
    with st.form("form_reserva", clear_on_submit=True):
        nombre = st.text_input("Nombre del solicitante")
        area = st.text_input("Área / Departamento")
        fecha_reserva = st.date_input("Fecha de uso", min_value=date.today())
        vehiculo_sel = st.selectbox("Selecciona un vehículo", vehiculos)
        
        submit_btn = st.form_submit_button("Reservar Vehículo")
        
        if submit_btn:
            if nombre and area:
                # Verificar si ya está reservado
                df = cargar_datos()
                # Convertimos la fecha del CSV a datetime para comparar
                df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
                
                # Filtramos si ese vehículo ya está reservado en esa fecha
                conflicto = df[(df['Vehículo'] == vehiculo_sel) & (df['Fecha'] == fecha_reserva)]
                
                if not conflicto.empty:
                    st.error(f"⚠️ El {vehiculo_sel} ya está reservado para esa fecha.")
                else:
                    guardar_reserva(fecha_reserva, vehiculo_sel, nombre, area)
                    st.success(f"✅ Reserva exitosa para el {vehiculo_sel} el {fecha_reserva}.")
                    st.rerun() # Recargar la app para actualizar la tabla
            else:
                st.warning("Por favor completa todos los campos.")
# --- VISUALIZACIÓN DE DATOS ---

st.subheader("📅 Calendario General de Reservas")

# Cargar datos
df_reservas = cargar_datos()

if not df_reservas.empty:
    # Convertir la columna de fecha a formato datetime
    df_reservas['Fecha'] = pd.to_datetime(df_reservas['Fecha'])
    
    # Ordenar por fecha
    df_reservas = df_reservas.sort_values(by='Fecha')

    # 1. Mostramos la tabla interactiva principal
    st.dataframe(df_reservas, use_container_width=True)

    # 2. Opcional: Un acordeón con la tabla ordenada por vehículo también
    with st.expander("📋 Ver lista detallada (ordenada por Vehículo)"):
        tabla_ordenada = df_reservas.sort_values(by=['Fecha', 'Vehículo'])
        st.dataframe(tabla_ordenada, use_container_width=True)

else:
    st.info("Aún no hay reservas registradas. ¡Sé el primero en apartar un vehículo!")
