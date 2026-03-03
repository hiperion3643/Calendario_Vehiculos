# Página de Calendario de Reservas

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import sys
import os

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS, obtener_nombres_vehiculos
from data.gestion_datos import cargar_reservas

def mostrar_pagina():
    st.title("🚗 Calendario de Reserva de Vehículos")
    st.markdown("Bienvenido al sistema de gestión de transporte. Consulta la disponibilidad de vehículos.")

    # --- SECCIÓN SUPERIOR: DISPONIBILIDAD RÁPIDA ---
    st.markdown("### 🚗 Disponibilidad Inmediata")

    # Selector de fecha y hora para consultar disponibilidad
    col_fecha, col_hora, col_btn = st.columns([2, 2, 1])

    with col_fecha:
        fecha_consulta = st.date_input("Selecciona una fecha:", value=date.today())

    with col_hora:
        # Usamos datetime.now() para obtener la hora actual
        hora_actual = datetime.now().time()
        hora_consulta = st.time_input("Selecciona una hora:", value=hora_actual)

    with col_btn:
        # Botón para realizar la consulta
        consultar = st.button("🔍 Consultar", use_container_width=True)

    # --- LÓGICA DE DISPONIBILIDAD ---

    # Variable para controlar si mostramos resultados
    mostrar_resultados = False
    vehiculos_disponibles = []  # Inicializamos la lista vacía para evitar errores

    # Solo realizamos la consulta si el usuario presiona el botón
    if consultar:
        mostrar_resultados = True

        # 1. FILTRADO POR ASIGNACIÓN (Solo Utilitarios)
        # Filtramos la lista de vehículos para obtener solo aquellos marcados como "Utilitario" o "Utilitaria"
        # Esto excluye a los vehículos asignados a personas específicas (Rector, Maestros, etc.)
        vehiculos_utilitarios = [v for v in VEHICULOS if v['asignado'].lower() in ['utilitario', 'utilitaria']]

        # Obtenemos los IDs de los vehículos utilitarios
        ids_utilitarios = [v['id'] for v in vehiculos_utilitarios]

        # Creamos un diccionario para mapear IDs a nombres completos
        # Usamos el formato "Tipo Placa" (sin guion) para mantener consistencia
        mapa_vehiculos = {v['id']: f"{v['tipo']} {v['placa']}" for v in vehiculos_utilitarios}

        # 2. CARGA Y FILTRADO DE RESERVAS
        df_reservas = cargar_reservas()

        if df_reservas.empty:
            st.info("No hay reservas registradas en el sistema.")
            # Si no hay reservas, todos los utilitarios están disponibles
            vehiculos_disponibles = list(mapa_vehiculos.values())
        else:
            # Convertir la columna de fecha a formato datetime
            df_reservas['Fecha'] = pd.to_datetime(df_reservas['Fecha']).dt.date

            # Filtramos reservas que coinciden con la fecha seleccionada
            reservas_fecha = df_reservas[df_reservas['Fecha'] == fecha_consulta]

            # Lista para almacenar IDs de vehículos ocupados (usamos set para evitar duplicados)
            ids_ocupados = set()

            if not reservas_fecha.empty:
                # Creamos un objeto datetime completo para la consulta
                hora_consulta_dt = datetime.combine(fecha_consulta, hora_consulta)

                # Iteramos sobre cada reserva del día
                for _, reserva in reservas_fecha.iterrows():
                    try:
                        # Convertimos las horas de inicio y fin a objetos time
                        hora_inicio = datetime.strptime(reserva['Hora Inicio'], "%H:%M").time()
                        hora_fin = datetime.strptime(reserva['Hora Fin'], "%H:%M").time()

                        # Creamos objetos datetime completos para comparación
                        inicio_dt = datetime.combine(fecha_consulta, hora_inicio)
                        fin_dt = datetime.combine(fecha_consulta, hora_fin)

                        # Verificamos si el vehículo está ocupado en el horario seleccionado
                        # Un vehículo está ocupado si la hora de consulta cae dentro del rango [inicio, fin]
                        if inicio_dt <= hora_consulta_dt <= fin_dt:
                            # Extraemos el ID del vehículo en la reserva
                            id_vehiculo = reserva['Vehículo']

                            # Verificamos si el ID del vehículo está en la lista de utilitarios
                            if id_vehiculo in ids_utilitarios:
                                ids_ocupados.add(id_vehiculo)
                    except Exception as e:
                        # Si hay error al procesar una reserva, la saltamos
                        print(f"Error al procesar reserva: {e}")
                        continue

            # 3. OBTENCIÓN DE VEHÍCULOS DISPONIBLES
            # Obtenemos la lista final de disponibles: utilitarios que no están ocupados
            vehiculos_disponibles = [mapa_vehiculos[id] for id in ids_utilitarios if id not in ids_ocupados]

            # --- MOSTRAR INFORMACIÓN DE DEPURACIÓN (Opcional) ---
            with st.expander("🔧 Ver detalles de la consulta (Depuración)"):
                st.write(f"Fecha de consulta: {fecha_consulta}")
                st.write(f"Hora de consulta: {hora_consulta}")
                st.write(f"Total de vehículos utilitarios en el sistema: {len(ids_utilitarios)}")
                st.write(f"Reservas para esta fecha: {len(reservas_fecha) if not reservas_fecha.empty else 0}")
                st.write(f"IDs de utilitarios: {ids_utilitarios}")
                st.write(f"Mapa de vehículos: {mapa_vehiculos}")

                if not reservas_fecha.empty:
                    st.write("Reservas encontradas para esta fecha:")
                    # Mostramos columnas relevantes para depuración
                    st.dataframe(reservas_fecha[['Vehículo', 'Hora Inicio', 'Hora Fin']])

                    # Mostrar información de cada reserva
                    for _, reserva in reservas_fecha.iterrows():
                        id_vehiculo = reserva['Vehículo']
                        st.write(f"ID del vehículo en reserva: {id_vehiculo}")
                        st.write(f"¿Está en ids_utilitarios? {id_vehiculo in ids_utilitarios}")
                        st.write(f"¿Está en mapa_vehículos? {id_vehiculo in mapa_vehiculos}")

                st.write(f"IDs de vehículos ocupados: {list(ids_ocupados)}")
                st.write(f"Vehículos disponibles: {vehiculos_disponibles}")

    # --- MOSTRAR RESULTADOS ---
    if mostrar_resultados:
        st.write(f"Vehículos disponibles para el {fecha_consulta} a las {hora_consulta}:")
        if vehiculos_disponibles:
            # Usamos columns para mostrarlos en una fila bonita
            cols = st.columns(min(5, len(vehiculos_disponibles)))
            for i, v in enumerate(vehiculos_disponibles[:5]):
                cols[i].success(f"✅ {v}")
        else:
            st.warning("⚠️ No hay vehículos disponibles para esta fecha y hora.")
    else:
        # Mensaje inicial cuando no se ha realizado consulta
        st.info("👆 Selecciona fecha y hora, luego presiona 'Consultar' para ver disponibilidad.")

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
