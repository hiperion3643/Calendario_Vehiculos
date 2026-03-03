
# Página de Estado de Vehículos

import streamlit as st
import pandas as pd
import sys
import os

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS, obtener_vehiculo_por_id
from data.gestion_datos import cargar_estado_vehiculos, obtener_ultimo_viaje, calcular_rendimiento_promedio
from data.vehiculos_detalle import obtener_detalle_vehiculo

def mostrar_pagina():

    st.title("🚗 Estado de Vehículos")
    st.markdown("Consulta el estado de los vehículos de la flota.")

    st.markdown("---")

    # Selector de vehículo
    opciones_vehiculos = [f"{v['tipo']} - {v['placa']} ({v['asignado']})" for v in VEHICULOS]
    vehiculo_seleccionado = st.selectbox("Selecciona un vehículo para ver su estado:", opciones_vehiculos)

    # Obtener el ID del vehículo seleccionado
    try:
        idx = opciones_vehiculos.index(vehiculo_seleccionado)
        id_vehiculo = VEHICULOS[idx]["id"]
    except (ValueError, AttributeError):
        st.error("Error al seleccionar el vehículo. Por favor, selecciona un vehículo de la lista.")
        return

    # Cargar datos del vehículo
    df_estado = cargar_estado_vehiculos()

    # Buscar el vehículo en el DataFrame
    vehiculo_estado = df_estado[df_estado["ID"] == id_vehiculo]

    if vehiculo_estado.empty:
        st.error(f"No se encontró información del vehículo con ID: {id_vehiculo}")
        return

    vehiculo_info = vehiculo_estado.iloc[0]

    # Obtener el último viaje del vehículo
    ultimo_viaje = obtener_ultimo_viaje(id_vehiculo)

    # Calcular el rendimiento promedio
    rendimiento_promedio = calcular_rendimiento_promedio(id_vehiculo)

    # Obtener información detallada del vehículo
    detalle_vehiculo = obtener_detalle_vehiculo(id_vehiculo)

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
        # Mostrar datos del último viaje si existe
        if ultimo_viaje is not None and pd.notna(ultimo_viaje['Km_Regreso']):
            st.write(f"**Kilometraje:** {int(ultimo_viaje['Km_Regreso'])} km")
            st.write(f"**Nivel de combustible:** {ultimo_viaje['gasolina regreso']}")
            st.write(f"**Última actualización:** {ultimo_viaje['Fecha']}")
        else:
            st.write(f"**Kilometraje:** {int(vehiculo_info['Kilometraje'])} km")
            st.write(f"**Nivel de combustible:** {vehiculo_info['Combustible']}")
            st.write(f"**Última actualización:** {vehiculo_info['Última Actualización']}")

    # Mostrar rendimiento promedio
    st.metric("Rendimiento Promedio", f"{rendimiento_promedio} km/l")

    # Mostrar información detallada del vehículo si está disponible
    if detalle_vehiculo:
        st.markdown("---")
        st.markdown("### 🚗 Información Detallada del Vehículo")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**📋 Información General:**")
            st.markdown(f"- Marca: {detalle_vehiculo['Marca']}")
            st.markdown(f"- Modelo: {detalle_vehiculo['Modelo']}")
            st.markdown(f"- Color: {detalle_vehiculo['Color']}")
            st.markdown(f"- Placas: {detalle_vehiculo['Placas']}")
            st.markdown(f"- Área Asignada: {detalle_vehiculo['Area_Asignada']}")

        with col2:
            st.markdown(f"**📄 Documentación:**")
            st.markdown(f"- Origen: {detalle_vehiculo['Origen']}")
            st.markdown(f"- Vigencia: {detalle_vehiculo['Vigencia']}")
            st.markdown(f"- Clase/Tipo: {detalle_vehiculo['Clase_Tipo']}")
            st.markdown(f"- Doc. Legalización: {detalle_vehiculo['Documento_de_Legalizacion']}")
            st.markdown(f"- Año Modelo: {detalle_vehiculo['Año_Modelo']}")

        with col3:
            st.markdown(f"**👤 Propietario:**")
            st.markdown(f"- Propietario: {detalle_vehiculo['Propietario']}")
            st.markdown(f"- RFC: {detalle_vehiculo['RFC']}")
            st.markdown(f"- Folio: {detalle_vehiculo['Folio']}")
            st.markdown(f"- Cilindros: {detalle_vehiculo['Cilindros']}")
            st.markdown(f"- Tipo de Servicio: {detalle_vehiculo['Tipo_de_Servicio']}")

    # Sección de imágenes del vehículo
    st.markdown("---")
    st.markdown("### 📸 Imágenes del Vehículo")

    # Crear directorio de imágenes si no existe
    dir_imagenes = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "imagenes", id_vehiculo)

    try:
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
    except Exception as e:
        st.warning(f"No se pudieron cargar las imágenes del vehículo: {e}")

if __name__ == "__main__":
    mostrar_pagina()
