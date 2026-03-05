
# Página de Control de Gasolina

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.gestion_gasolina import (
    obtener_estado_gasolina_semana,
    obtener_historico_gasolina,
    VEHICULOS_ASIGNADOS,
    MONTO_SEMANAL
)
from data.vehiculos import obtener_todos_vehiculos

def mostrar_pagina():
    st.title("⛽ Control de Gasolina Semanal")
    st.markdown("Sistema de control de recargas de gasolina para vehículos asignados")

    # --- SECCIÓN SUPERIOR: SELECCIÓN DE SEMANA ---
    st.markdown("### 📅 Seleccionar Semana")

    col_fecha, col_btn = st.columns([2, 1])

    with col_fecha:
        fecha_seleccionada = st.date_input(
            "Selecciona una fecha:",
            value=date.today(),
            max_value=date.today() + timedelta(days=7)
        )

    with col_btn:
        consultar = st.button("🔍 Consultar", use_container_width=True)

    # --- DASHBOARD DE ESTADO ---
    st.markdown("### 📊 Estado de Recargas de Gasolina")

    # Obtener estado de la semana seleccionada
    df_estado = obtener_estado_gasolina_semana(fecha_seleccionada)

    # Calcular estadísticas
    total_vehiculos = len(df_estado)
    recargados = len(df_estado[df_estado["Estado"] == "✅ Recargado"])
    pendientes = total_vehiculos - recargados

    # Mostrar métricas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Vehículos", total_vehiculos)

    with col2:
        st.metric("Recargados", recargados)

    with col3:
        st.metric("Pendientes", pendientes)

    # Mostrar tabla de estado
    st.dataframe(
        df_estado[["Tipo", "Placa", "Asignado", "Fecha_Recarga", "Estado"]],
        use_container_width=True,
        hide_index=True
    )

    # --- NOTA INFORMATIVA ---
    st.info("""
    ℹ️ **Información importante:**
    - Cada vehículo asignado tiene derecho a una recarga semanal de $500.00 MXN
    - El sistema registra automáticamente la semana de cada recarga
    - Para registrar una recarga, utiliza el módulo de administración
    """)

    # --- SECCIÓN DE HISTÓRICO ---
    st.markdown("### 📋 Histórico de Recargas")

    col_anio, col_vehiculo_hist = st.columns(2)

    with col_anio:
        anios_disponibles = [date.today().year, date.today().year - 1]
        anio_seleccionado = st.selectbox(
            "Año:",
            anios_disponibles,
            index=0
        )

    with col_vehiculo_hist:
        opciones_todos = ["Todos"] + [
            f"{v['tipo']} - {v['placa']} ({v['asignado']})"
            for v in VEHICULOS_ASIGNADOS
        ]
        vehiculo_hist_seleccionado = st.selectbox(
            "Vehículo:",
            opciones_todos
        )

    # Obtener histórico
    id_vehiculo_hist = None
    if vehiculo_hist_seleccionado != "Todos":
        for v in VEHICULOS_ASIGNADOS:
            if f"{v['tipo']} - {v['placa']} ({v['asignado']})" == vehiculo_hist_seleccionado:
                id_vehiculo_hist = v['id']
                break

    df_historico = obtener_historico_gasolina(id_vehiculo_hist, anio_seleccionado)

    if not df_historico.empty:
        st.dataframe(
            df_historico[["Placa", "Asignado", "Fecha", "Semana", "Monto", "Estado"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay registros de recargas para el período seleccionado")

if __name__ == "__main__":
    mostrar_pagina()
