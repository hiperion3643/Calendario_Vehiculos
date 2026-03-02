
# Módulo de gestión de datos

import pandas as pd
import os
from datetime import datetime, date

# Rutas de archivos de datos
DIR_DATA = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(DIR_DATA)
FILE_RESERVAS = os.path.join(DIR_BASE, "reservas.csv")
FILE_ESTADO_VEHICULOS = os.path.join(DIR_BASE, "data", "estado_vehiculos.csv")
FILE_VERIFICACIONES = os.path.join(DIR_BASE, "data", "verificaciones.csv")
FILE_FOTOMULTAS = os.path.join(DIR_BASE, "data", "fotomultas.csv")

def inicializar_archivos():
    """Inicializa los archivos de datos si no existen"""
    # Archivo de reservas
    if not os.path.exists(FILE_RESERVAS):
        df = pd.DataFrame(columns=["Fecha", "Hora Inicio", "Hora Fin", "Vehículo", "Solicitante", "Área", "Km_Salida", "Km_Regreso", "gasolina salida", "gasolina regreso"])
        df.to_csv(FILE_RESERVAS, index=False)

    # Archivo de estado de vehículos
    if not os.path.exists(FILE_ESTADO_VEHICULOS):
        from .vehiculos import VEHICULOS
        df = pd.DataFrame([{
            "ID": v["id"],
            "Tipo": v["tipo"],
            "Placa": v["placa"],
            "Asignado": v["asignado"],
            "Estado": "Disponible",
            "Kilometraje": 0,
            "Combustible": "100%",
            "Última Actualización": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } for v in VEHICULOS])
        df.to_csv(FILE_ESTADO_VEHICULOS, index=False)

    # Archivo de verificaciones
    if not os.path.exists(FILE_VERIFICACIONES):
        from .vehiculos import VEHICULOS
        df = pd.DataFrame([{
            "ID": v["id"],
            "Placa": v["placa"],
            "Última Verificación": "",
            "Próxima Verificación": "",
            "Estado Verificación": "Pendiente",
            "Último Mantenimiento": "",
            "Próximo Mantenimiento": "",
            "Estado Mantenimiento": "Pendiente",
            "Último Control Vehicular": "",
            "Próximo Control Vehicular": "",
            "Estado Control Vehicular": "Pendiente"
        } for v in VEHICULOS])
        df.to_csv(FILE_VERIFICACIONES, index=False)

    # Archivo de fotomultas
    if not os.path.exists(FILE_FOTOMULTAS):
        df = pd.DataFrame(columns=[
            "ID", "Placa", "Fecha", "Hora", "Lugar", "Infracción", 
            "Monto", "Estado", "Referencia", "Observaciones"
        ])
        df.to_csv(FILE_FOTOMULTAS, index=False)

def cargar_reservas():
    """Carga los datos de reservas"""
    if not os.path.exists(FILE_RESERVAS):
        return pd.DataFrame(columns=["Fecha", "Hora Inicio", "Hora Fin", "Vehículo", "Solicitante", "Área", "Km_Salida", "Km_Regreso", "gasolina salida", "gasolina regreso"])
    return pd.read_csv(FILE_RESERVAS)

def guardar_reserva(reserva):
    """Guarda una nueva reserva"""
    df = cargar_reservas()
    df = pd.concat([df, pd.DataFrame([reserva])], ignore_index=True)
    df.to_csv(FILE_RESERVAS, index=False)

def cargar_estado_vehiculos():
    """Carga el estado de los vehículos"""
    if not os.path.exists(FILE_ESTADO_VEHICULOS):
        inicializar_archivos()
    return pd.read_csv(FILE_ESTADO_VEHICULOS)

def actualizar_estado_vehiculo(id_vehiculo, estado, kilometraje=None, combustible=None):
    """Actualiza el estado de un vehículo"""
    df = cargar_estado_vehiculos()
    idx = df.index[df["ID"] == id_vehiculo].tolist()[0]
    df.at[idx, "Estado"] = estado
    df.at[idx, "Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if kilometraje is not None:
        df.at[idx, "Kilometraje"] = kilometraje

    if combustible is not None:
        df.at[idx, "Combustible"] = combustible

    df.to_csv(FILE_ESTADO_VEHICULOS, index=False)

def cargar_verificaciones():
    """Carga los datos de verificaciones"""
    if not os.path.exists(FILE_VERIFICACIONES):
        inicializar_archivos()
    return pd.read_csv(FILE_VERIFICACIONES)

def actualizar_verificacion(id_vehiculo, tipo, fecha_actual, fecha_proxima, estado):
    """Actualiza una verificación de vehículo"""
    df = cargar_verificaciones()
    idx = df.index[df["ID"] == id_vehiculo].tolist()[0]

    if tipo == "verificacion":
        df.at[idx, "Última Verificación"] = fecha_actual
        df.at[idx, "Próxima Verificación"] = fecha_proxima
        df.at[idx, "Estado Verificación"] = estado
    elif tipo == "mantenimiento":
        df.at[idx, "Último Mantenimiento"] = fecha_actual
        df.at[idx, "Próximo Mantenimiento"] = fecha_proxima
        df.at[idx, "Estado Mantenimiento"] = estado
    elif tipo == "control_vehicular":
        df.at[idx, "Último Control Vehicular"] = fecha_actual
        df.at[idx, "Próximo Control Vehicular"] = fecha_proxima
        df.at[idx, "Estado Control Vehicular"] = estado

    df.to_csv(FILE_VERIFICACIONES, index=False)

def cargar_fotomultas():
    """Carga los datos de fotomultas"""
    if not os.path.exists(FILE_FOTOMULTAS):
        inicializar_archivos()
    return pd.read_csv(FILE_FOTOMULTAS)

def agregar_fotomulta(fotomulta):
    """Agrega una nueva fotomulta"""
    df = cargar_fotomultas()
    df = pd.concat([df, pd.DataFrame([fotomulta])], ignore_index=True)
    df.to_csv(FILE_FOTOMULTAS, index=False)

def actualizar_estado_fotomulta(id_fotomulta, estado):
    """Actualiza el estado de una fotomulta"""
    df = cargar_fotomultas()
    idx = df.index[df["Referencia"] == id_fotomulta].tolist()[0]
    df.at[idx, "Estado"] = estado
    df.to_csv(FILE_FOTOMULTAS, index=False)
