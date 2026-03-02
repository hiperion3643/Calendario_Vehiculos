
# Página de Calendario de Reservas

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import sys
import os

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS, obtener_nombres_vehiculos
from data.gestion_datos import cargar_reservas, guardar_reserva

def mostrar_pagina():
   
    st.title("🚗 Calendario de Reserva de Vehículos")
    st.markdown("Bienvenido al sistema de gestión de transporte. Consulta la disponibilidad de vehículos.")

    # --- SECCIÓN SUPERIOR: DISPONIBILIDAD RÁPIDA ---
    st.markdown("### 🚗 Disponibilidad Inmediata")

    # Selector de fecha para consultar disponibilidad
    fecha_consulta = st.date_input("Selecciona una fecha para ver disponibilidad:", value=date.today())

    # Cargamos datos para verificar disponibilidad
    df_temp = cargar_reservas()

    # Lógica para encontrar vehículos disponibles
    vehiculos_ocupados = []
    vehiculos_asignados = []

    # Obtener vehículos que ya tienen asignación permanente (no son utilitarios)
    from data.vehiculos import VEHICULOS
    vehiculos_asignados = [f"{v['tipo']} {v['placa']}" for v in VEHICULOS 
                          if v['asignado'] not in ['Utilitario', 'Utilitaria']]

    if not df_temp.empty:
        # Convertir la columna Fecha a datetime y luego a date
        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha']).dt.date

        # Buscamos qué vehículos tienen reserva en la fecha seleccionada
        ocupados_hoy = df_temp[df_temp['Fecha'] == fecha_consulta]['Vehículo'].unique()
        vehiculos_ocupados = list(ocupados_hoy)

    # Filtramos la lista total de vehículos excluyendo los ocupados y los asignados permanentemente
    vehiculos_disponibles = [v for v in obtener_nombres_vehiculos() 
                           if v not in vehiculos_ocupados and v not in vehiculos_asignados]

    # Mostramos los primeros 5 disponibles (o menos si no hay 5)
    st.write(f"Vehículos libres para el {fecha_consulta}:")
    if vehiculos_disponibles:
        # Usamos columns para mostrarlos en una fila bonita
        cols = st.columns(min(5, len(vehiculos_disponibles)))
        for i, v in enumerate(vehiculos_disponibles[:5]):
            cols[i].success(f"✅ {v}")
    else:
        st.warning("⚠️ No hay vehículos disponibles para esta fecha.")

    # --- NOTA DE RESERVAS ---
    st.info("ℹ️ Para realizar una reserva de vehículo, por favor contacta a través del siguiente botón:")

    # Botón de WhatsApp
    numero_whatsapp = "522224884437"
    mensaje_whatsapp = "Hola, me gustaría solicitar un vehículo."
    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_whatsapp}"

    st.markdown(f"""
    <a href="{link_whatsapp}" target="_blank">
        <button style="
            background-color: #25D366;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        ">
            💬 Contactar por WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

    # --- VISUALIZACIÓN DE DATOS ---
    st.markdown("### 📅 Calendario General de Reservas")

    # Cargar datos
    df_reservas = cargar_reservas()

    if not df_reservas.empty:
        # Convertir la columna de fecha a formato datetime
        df_reservas['Fecha'] = pd.to_datetime(df_reservas['Fecha'])

        # Filtro de mes
        st.markdown("### 🔍 Filtrar por Mes")
        col1, col2 = st.columns(2)

        with col1:
            mes_seleccionado = st.selectbox(
                "Selecciona el mes:",
                options=["Todos"] + list(range(1, 13)),
                format_func=lambda x: "Todos" if x == "Todos" else datetime(2024, x, 1).strftime("%B")
            )

        with col2:
            anio_seleccionado = st.selectbox(
                "Selecciona el año:",
                options=["Todos"] + sorted(df_reservas['Fecha'].dt.year.unique().tolist())
            )

        # Aplicar filtros
        if mes_seleccionado != "Todos":
            df_reservas = df_reservas[df_reservas['Fecha'].dt.month == mes_seleccionado]

        if anio_seleccionado != "Todos":
            df_reservas = df_reservas[df_reservas['Fecha'].dt.year == anio_seleccionado]

        # Ordenar por fecha
        df_reservas = df_reservas.sort_values(by=['Fecha', 'Hora Inicio'])

        # 1. Mostramos la tabla interactiva principal
        # Crear una copia para mostrar sin la hora
        df_mostrar = df_reservas.copy()
        df_mostrar['Fecha'] = df_mostrar['Fecha'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_mostrar, use_container_width=True)

        # 2. Opcional: Un acordeón con la tabla ordenada por vehículo también
        with st.expander("📋 Ver lista detallada (ordenada por Vehículo)"):
            tabla_ordenada = df_reservas.copy()
            tabla_ordenada['Fecha'] = tabla_ordenada['Fecha'].dt.strftime('%Y-%m-%d')
            tabla_ordenada = tabla_ordenada.sort_values(by=['Fecha', 'Vehículo', 'Hora Inicio'])
            st.dataframe(tabla_ordenada, use_container_width=True)
    else:
        st.info("Aún no hay reservas registradas.")

if __name__ == "__main__":
    mostrar_pagina()
