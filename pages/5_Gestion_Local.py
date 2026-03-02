# Página de Gestión Local

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import sys
import os
from PIL import Image
import io

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS, obtener_nombres_vehiculos
from data.gestion_datos import (
    cargar_reservas, guardar_reserva,
    cargar_estado_vehiculos, actualizar_estado_vehiculo,
    cargar_verificaciones, actualizar_verificacion,
    cargar_fotomultas, agregar_fotomulta, actualizar_estado_fotomulta
)

# Configuración de la página
st.set_page_config(
    page_title="Gestión Local",
    page_icon="🔧",
    layout="wide"
)

def mostrar_pagina():
    st.title("🔧 Gestión Local de Reservas")
    st.markdown("Panel de administración para gestionar reservas, evidencias y fechas importantes")

    # Crear tabs para diferentes secciones
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Reservas", "🚗 Estado Vehículos", "📅 Verificaciones", "📸 Evidencias"])

    # --- TAB 1: GESTIÓN DE RESERVAS ---
    with tab1:
        st.markdown("### 📝 Gestión de Reservas")

        # Cargar reservas existentes
        df_reservas = cargar_reservas()

        if not df_reservas.empty:
            # Convertir la columna de fecha a formato datetime
            df_reservas['Fecha'] = pd.to_datetime(df_reservas['Fecha'])

            # Opciones: Ver, Editar o Eliminar
            opcion = st.radio("Selecciona una acción:", ["Ver Reservas", "Nueva Reserva", "Editar Reserva", "Eliminar Reserva"])

            if opcion == "Ver Reservas":
                # Mostrar todas las reservas
                df_mostrar = df_reservas.copy()
                df_mostrar['Fecha'] = df_mostrar['Fecha'].dt.strftime('%Y-%m-%d')
                st.dataframe(df_mostrar, use_container_width=True)

            elif opcion == "Nueva Reserva":
                st.markdown("#### 📝 Crear Nueva Reserva")

                with st.form("form_nueva_reserva"):
                    col1, col2 = st.columns(2)

                    with col1:
                        fecha_reserva = st.date_input("Fecha de la reserva:", value=date.today())
                        hora_inicio = st.time_input("Hora de inicio:", value=time(8, 0))
                        vehiculo = st.selectbox("Vehículo:", obtener_nombres_vehiculos())
                        solicitante = st.text_input("Solicitante:")

                    with col2:
                        hora_fin = st.time_input("Hora de fin:", value=time(17, 0))
                        area = st.text_input("Área:")
                        km_salida = st.number_input("Kilometraje de salida:", min_value=0, value=0)
                        km_regreso = st.number_input("Kilometraje de regreso:", min_value=0, value=0)

                    gasolina_salida = st.selectbox("Gasolina salida:", ["1/4", "1/2", "3/4", "Lleno"])
                    gasolina_regreso = st.selectbox("Gasolina regreso:", ["1/4", "1/2", "3/4", "Lleno"])

                    submit = st.form_submit_button("Guardar Reserva")

                    if submit:
                        if not solicitante or not area:
                            st.error("⚠️ Por favor completa todos los campos requeridos.")
                        else:
                            # Crear el diccionario de la reserva
                            nueva_reserva = {
                                "Fecha": fecha_reserva.strftime("%Y-%m-%d"),
                                "Hora Inicio": hora_inicio.strftime("%H:%M"),
                                "Hora Fin": hora_fin.strftime("%H:%M"),
                                "Vehículo": vehiculo,
                                "Solicitante": solicitante,
                                "Área": area,
                                "Km_Salida": km_salida,
                                "Km_Regreso": km_regreso,
                                "gasolina salida": gasolina_salida,
                                "gasolina regreso": gasolina_regreso
                            }

                            # Guardar la reserva
                            guardar_reserva(nueva_reserva)
                            st.success("✅ Reserva guardada exitosamente!")
                            st.rerun()

            elif opcion == "Editar Reserva":
                st.markdown("#### ✏️ Editar Reserva Existente")

                # Seleccionar reserva a editar
                df_mostrar = df_reservas.copy()
                df_mostrar['Fecha'] = df_mostrar['Fecha'].dt.strftime('%Y-%m-%d')

                # Crear un identificador único para cada reserva
                df_mostrar['ID'] = df_mostrar.index.astype(str)

                reserva_seleccionada = st.selectbox(
                    "Selecciona la reserva a editar:",
                    options=df_mostrar.index.tolist(),
                    format_func=lambda x: f"{df_mostrar.loc[x, 'Fecha']} - {df_mostrar.loc[x, 'Vehículo']} - {df_mostrar.loc[x, 'Solicitante']}"
                )

                if reserva_seleccionada is not None:
                    reserva_actual = df_reservas.iloc[reserva_seleccionada]

                    with st.form("form_editar_reserva"):
                        col1, col2 = st.columns(2)

                        with col1:
                            fecha_reserva = st.date_input(
                                "Fecha de la reserva:",
                                value=pd.to_datetime(reserva_actual['Fecha']).date()
                            )
                            hora_inicio = st.time_input(
                                "Hora de inicio:",
                                value=datetime.strptime(reserva_actual['Hora Inicio'], "%H:%M").time()
                            )
                            vehiculo = st.selectbox(
                                "Vehículo:",
                                obtener_nombres_vehiculos(),
                                index=obtener_nombres_vehiculos().index(reserva_actual['Vehículo'])
                            )
                            solicitante = st.text_input("Solicitante:", value=reserva_actual['Solicitante'])

                        with col2:
                            hora_fin = st.time_input(
                                "Hora de fin:",
                                value=datetime.strptime(reserva_actual['Hora Fin'], "%H:%M").time()
                            )
                            area = st.text_input("Área:", value=reserva_actual['Área'])
                            km_salida = st.number_input(
                                "Kilometraje de salida:",
                                min_value=0,
                                value=int(reserva_actual['Km_Salida']) if pd.notna(reserva_actual['Km_Salida']) else 0
                            )
                            km_regreso = st.number_input(
                                "Kilometraje de regreso:",
                                min_value=0,
                                value=int(reserva_actual['Km_Regreso']) if pd.notna(reserva_actual['Km_Regreso']) else 0
                            )

                        gasolina_salida = st.selectbox(
                            "Gasolina salida:",
                            ["1/4", "1/2", "3/4", "Lleno"],
                            index=["1/4", "1/2", "3/4", "Lleno"].index(reserva_actual['gasolina salida']) if pd.notna(reserva_actual['gasolina salida']) else 0
                        )
                        gasolina_regreso = st.selectbox(
                            "Gasolina regreso:",
                            ["1/4", "1/2", "3/4", "Lleno"],
                            index=["1/4", "1/2", "3/4", "Lleno"].index(reserva_actual['gasolina regreso']) if pd.notna(reserva_actual['gasolina regreso']) else 0
                        )

                        submit = st.form_submit_button("Actualizar Reserva")

                        if submit:
                            if not solicitante or not area:
                                st.error("⚠️ Por favor completa todos los campos requeridos.")
                            else:
                                # Actualizar la reserva
                                df_reservas.at[reserva_seleccionada, 'Fecha'] = fecha_reserva.strftime("%Y-%m-%d")
                                df_reservas.at[reserva_seleccionada, 'Hora Inicio'] = hora_inicio.strftime("%H:%M")
                                df_reservas.at[reserva_seleccionada, 'Hora Fin'] = hora_fin.strftime("%H:%M")
                                df_reservas.at[reserva_seleccionada, 'Vehículo'] = vehiculo
                                df_reservas.at[reserva_seleccionada, 'Solicitante'] = solicitante
                                df_reservas.at[reserva_seleccionada, 'Área'] = area
                                df_reservas.at[reserva_seleccionada, 'Km_Salida'] = km_salida
                                df_reservas.at[reserva_seleccionada, 'Km_Regreso'] = km_regreso
                                df_reservas.at[reserva_seleccionada, 'gasolina salida'] = gasolina_salida
                                df_reservas.at[reserva_seleccionada, 'gasolina regreso'] = gasolina_regreso

                                # Guardar cambios
                                df_reservas.to_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reservas.csv"), index=False)
                                st.success("✅ Reserva actualizada exitosamente!")
                                st.rerun()

            elif opcion == "Eliminar Reserva":
                st.markdown("#### 🗑️ Eliminar Reserva")

                # Seleccionar reserva a eliminar
                df_mostrar = df_reservas.copy()
                df_mostrar['Fecha'] = df_mostrar['Fecha'].dt.strftime('%Y-%m-%d')

                reserva_seleccionada = st.selectbox(
                    "Selecciona la reserva a eliminar:",
                    options=df_mostrar.index.tolist(),
                    format_func=lambda x: f"{df_mostrar.loc[x, 'Fecha']} - {df_mostrar.loc[x, 'Vehículo']} - {df_mostrar.loc[x, 'Solicitante']}"
                )

                if reserva_seleccionada is not None:
                    st.warning(f"¿Estás seguro de que deseas eliminar la reserva del {df_mostrar.loc[reserva_seleccionada, 'Fecha']} para el vehículo {df_mostrar.loc[reserva_seleccionada, 'Vehículo']}?")

                    if st.button("Confirmar Eliminación"):
                        df_reservas = df_reservas.drop(reserva_seleccionada)
                        df_reservas.to_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reservas.csv"), index=False)
                        st.success("✅ Reserva eliminada exitosamente!")
                        st.rerun()
        else:
            st.info("Aún no hay reservas registradas.")

    # --- TAB 2: ESTADO DE VEHÍCULOS ---
    with tab2:
        st.markdown("### 🚗 Estado de Vehículos")

        # Cargar estado de vehículos
        df_estado = cargar_estado_vehiculos()

        if not df_estado.empty:
            # Mostrar estado actual
            st.dataframe(df_estado, use_container_width=True)

            # Formulario para actualizar estado
            st.markdown("#### 🔄 Actualizar Estado de Vehículo")

            vehiculo_seleccionado = st.selectbox(
                "Selecciona el vehículo:",
                options=df_estado['ID'].tolist(),
                format_func=lambda x: f"{df_estado[df_estado['ID'] == x]['Tipo'].values[0]} {df_estado[df_estado['ID'] == x]['Placa'].values[0]}"
            )

            if vehiculo_seleccionado:
                col1, col2, col3 = st.columns(3)

                with col1:
                    nuevo_estado = st.selectbox(
                        "Nuevo Estado:",
                        ["Disponible", "En Uso", "En Mantenimiento", "Fuera de Servicio"]
                    )

                with col2:
                    kilometraje = st.number_input(
                        "Kilometraje:",
                        min_value=0,
                        value=int(df_estado[df_estado['ID'] == vehiculo_seleccionado]['Kilometraje'].values[0])
                    )

                with col3:
                    combustible = st.selectbox(
                        "Nivel de Combustible:",
                        ["1/4", "1/2", "3/4", "Lleno"],
                        index=["1/4", "1/2", "3/4", "Lleno"].index(df_estado[df_estado['ID'] == vehiculo_seleccionado]['Combustible'].values[0].replace('%', ''))
                    )

                if st.button("Actualizar Estado"):
                    actualizar_estado_vehiculo(vehiculo_seleccionado, nuevo_estado, kilometraje, combustible)
                    st.success("✅ Estado actualizado exitosamente!")
                    st.rerun()
        else:
            st.info("No hay datos de estado de vehículos.")

    # --- TAB 3: VERIFICACIONES ---
    with tab3:
        st.markdown("### 📅 Verificaciones y Mantenimientos")

        # Cargar verificaciones
        df_verificaciones = cargar_verificaciones()

        if not df_verificaciones.empty:
            # Mostrar verificaciones actuales
            st.dataframe(df_verificaciones, use_container_width=True)

            # Formulario para actualizar verificaciones
            st.markdown("#### 🔄 Actualizar Verificación")

            vehiculo_seleccionado = st.selectbox(
                "Selecciona el vehículo:",
                options=df_verificaciones['ID'].tolist(),
                format_func=lambda x: f"{df_verificaciones[df_verificaciones['ID'] == x]['Placa'].values[0]}"
            )

            tipo_verificacion = st.selectbox(
                "Tipo de Verificación:",
                ["verificacion", "mantenimiento", "control_vehicular"],
                format_func=lambda x: {
                    "verificacion": "Verificación",
                    "mantenimiento": "Mantenimiento",
                    "control_vehicular": "Control Vehicular"
                }[x]
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                fecha_actual = st.date_input("Fecha Actual:", value=date.today())

            with col2:
                fecha_proxima = st.date_input("Fecha Próxima:", value=date.today())

            with col3:
                estado = st.selectbox(
                    "Estado:",
                    ["Completado", "Pendiente", "En Proceso", "Vencido"]
                )

            if st.button("Actualizar Verificación"):
                actualizar_verificacion(
                    vehiculo_seleccionado,
                    tipo_verificacion,
                    fecha_actual.strftime("%Y-%m-%d"),
                    fecha_proxima.strftime("%Y-%m-%d"),
                    estado
                )
                st.success("✅ Verificación actualizada exitosamente!")
                st.rerun()
        else:
            st.info("No hay datos de verificaciones.")

    # --- TAB 4: EVIDENCIAS ---
    with tab4:
        st.markdown("### 📸 Gestión de Evidencias")

        # Seleccionar vehículo para agregar evidencias
        vehiculo_seleccionado = st.selectbox(
            "Selecciona el vehículo:",
            options=[v['id'] for v in VEHICULOS],
            format_func=lambda x: f"{next(v['tipo'] for v in VEHICULOS if v['id'] == x)} {next(v['placa'] for v in VEHICULOS if v['id'] == x)}"
        )

        if vehiculo_seleccionado:
            # Obtener información del vehículo
            vehiculo_info = next(v for v in VEHICULOS if v['id'] == vehiculo_seleccionado)
            placa = vehiculo_info['placa']

            # Crear directorio para evidencias si no existe
            dir_evidencias = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "imagenes",
                f"evidencias_{placa}"
            )

            os.makedirs(dir_evidencias, exist_ok=True)

            # Mostrar evidencias existentes
            st.markdown(f"#### 📸 Evidencias del Vehículo {vehiculo_info['tipo']} {placa}")

            # Listar archivos de evidencias
            archivos_evidencias = []
            if os.path.exists(dir_evidencias):
                archivos_evidencias = [f for f in os.listdir(dir_evidencias) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

            if archivos_evidencias:
                cols = st.columns(min(3, len(archivos_evidencias)))
                for i, archivo in enumerate(archivos_evidencias):
                    with cols[i % 3]:
                        ruta_imagen = os.path.join(dir_evidencias, archivo)
                        try:
                            st.image(ruta_imagen, caption=archivo, use_column_width=True)
                            if st.button(f"🗑️ Eliminar {archivo}", key=f"eliminar_{archivo}"):
                                os.remove(ruta_imagen)
                                st.success(f"✅ {archivo} eliminado exitosamente!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error al cargar {archivo}: {str(e)}")
            else:
                st.info("No hay evidencias registradas para este vehículo.")

            # Formulario para agregar nueva evidencia
            st.markdown("#### 📤 Agregar Nueva Evidencia")

            uploaded_file = st.file_uploader(
                "Sube una imagen de evidencia:",
                type=['png', 'jpg', 'jpeg', 'gif']
            )

            descripcion = st.text_input("Descripción de la evidencia:")

            if uploaded_file is not None:
                # Mostrar vista previa
                st.image(uploaded_file, caption="Vista previa", use_column_width=True)

                if st.button("Guardar Evidencia"):
                    # Generar nombre de archivo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    extension = uploaded_file.name.split('.')[-1]
                    nombre_archivo = f"{timestamp}_{descripcion.replace(' ', '_')}.{extension}" if descripcion else f"{timestamp}.{extension}"

                    # Guardar archivo
                    ruta_guardar = os.path.join(dir_evidencias, nombre_archivo)
                    with open(ruta_guardar, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.success(f"✅ Evidencia guardada exitosamente como {nombre_archivo}!")
                    st.rerun()

if __name__ == "__main__":
    mostrar_pagina()
