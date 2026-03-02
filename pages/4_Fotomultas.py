
# Página de Fotomultas

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, date

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS
from data.gestion_datos import cargar_fotomultas

def mostrar_pagina():
   
    st.title("🚦 Gestión de Fotomultas")
    st.markdown("Consulta las fotomultas de los vehículos de la flota.")

    st.markdown("---")

    # Cargar datos de fotomultas
    df_fotomultas = cargar_fotomultas()

    # --- SECCIÓN DE VISUALIZACIÓN ---
    st.markdown("### 📋 Listado de Fotomultas")

    if not df_fotomultas.empty:
        # Convertir la columna de fecha a formato datetime
        df_fotomultas['Fecha'] = pd.to_datetime(df_fotomultas['Fecha'])

        # Ordenar por fecha
        df_fotomultas = df_fotomultas.sort_values(by='Fecha', ascending=False)

        # Mostrar la tabla interactiva
        st.dataframe(df_fotomultas, use_container_width=True)
    else:
        st.info("Aún no hay fotomultas registradas.")

    # --- SECCIÓN DE RESUMEN ---
    st.markdown("### 📊 Resumen de Fotomultas")

    if not df_fotomultas.empty:
        # Calcular totales por estado
        resumen_estado = df_fotomultas.groupby('Estado').size().reset_index(name='Cantidad')
        st.write("Fotomultas por estado:")
        st.dataframe(resumen_estado, use_container_width=True)

        # Calcular monto total por estado
        resumen_monto = df_fotomultas.groupby('Estado')['Monto'].sum().reset_index(name='Monto Total')
        st.write("Monto total por estado:")
        st.dataframe(resumen_monto, use_container_width=True)

        # Calcular monto total de todas las fotomultas
        monto_total = df_fotomultas['Monto'].sum()
        st.write(f"**Monto total de todas las fotomultas:** ${monto_total:.2f}")

        # Calcular monto pendiente de pago
        monto_pendiente = df_fotomultas[df_fotomultas['Estado'] == 'Pendiente']['Monto'].sum()
        st.write(f"**Monto pendiente de pago:** ${monto_pendiente:.2f}")

if __name__ == "__main__":
    mostrar_pagina()
