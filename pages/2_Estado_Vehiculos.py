
# Página de Estado de Vehículos

import streamlit as st
import pandas as pd
import sys
import os

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS, obtener_vehiculo_por_id
from data.gestion_datos import cargar_estado_vehiculos

def mostrar_pagina():
    
    st.title("🚗 Estado de Vehículos")
    st.markdown("Consulta el estado de los vehículos de la flota.")

    st.markdown("---")

    # Selector de vehículo
    opciones_vehiculos = [f"{v['tipo']} - {v['placa']} ({v['asignado']})" for v in VEHICULOS]
    vehiculo_seleccionado = st.selectbox("Selecciona un vehículo para ver su estado:", opciones_vehiculos)

    # Obtener el ID del vehículo seleccionado
    idx = opciones_vehiculos.index(vehiculo_seleccionado)
    id_vehiculo = VEHICULOS[idx]["id"]

    # Cargar datos del vehículo
    df_estado = cargar_estado_vehiculos()
    vehiculo_info = df_estado[df_estado["ID"] == id_vehiculo].iloc[0] if not df_estado.empty else None

    if vehiculo_info is not None:
        # Mostrar información del vehículo
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 Información General")
            st.write(f"**Tipo:** {vehiculo_info['Tipo']}")
            st.write(f"**Placa:** {vehiculo_info['Placa']}")
            st.write(f"**Asignado a:** {vehiculo_info['Asignado']}")
            st.write(f"**Estado actual:** {vehiculo_info['Estado']}")

        with col2:
            st.markdown("### 📊 Estado Actual")
            st.write(f"**Kilometraje:** {vehiculo_info['Kilometraje']} km")
            st.write(f"**Nivel de combustible:** {vehiculo_info['Combustible']}")
            st.write(f"**Última actualización:** {vehiculo_info['Última Actualización']}")

        # Sección de imágenes del vehículo
        st.markdown("### 📸 Imágenes del Vehículo")

        # Crear directorio de imágenes si no existe
        dir_imagenes = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "imagenes", id_vehiculo)
        os.makedirs(dir_imagenes, exist_ok=True)

        # Mostrar imágenes existentes
        imagenes = [f for f in os.listdir(dir_imagenes) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if imagenes:
            cols = st.columns(min(3, len(imagenes)))
            for i, img in enumerate(imagenes):
                with cols[i % 3]:
                    st.image(os.path.join(dir_imagenes, img), caption=img, use_column_width=True)
        else:
            st.info("No hay imágenes registradas para este vehículo.")
    else:
        st.error("No se encontró información del vehículo seleccionado.")

if __name__ == "__main__":
    mostrar_pagina()
