
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

def obtener_ultimo_viaje(id_vehiculo):
    """Obtiene el último viaje de un vehículo desde el archivo de reservas"""
    df_reservas = cargar_reservas()
    
    # Filtrar reservas por vehículo
    viajes_vehiculo = df_reservas[df_reservas["Vehículo"] == id_vehiculo]
    
    if viajes_vehiculo.empty:
        return None
    
    # Ordenar por fecha y hora para obtener el más reciente
    viajes_vehiculo["Fecha"] = pd.to_datetime(viajes_vehiculo["Fecha"])
    viajes_vehiculo = viajes_vehiculo.sort_values(by=["Fecha", "Hora Fin"], ascending=False)
    
    # Retornar el último viaje
    return viajes_vehiculo.iloc[0]

def calcular_rendimiento_promedio(id_vehiculo):
    """Calcula el rendimiento promedio (km/litro) de un vehículo basado en sus viajes"""
    df_reservas = cargar_reservas()
    
    # Filtrar reservas por vehículo
    viajes_vehiculo = df_reservas[df_reservas["Vehículo"] == id_vehiculo]
    
    if viajes_vehiculo.empty:
        return 0.0
    
    # Calcular rendimiento para cada viaje
    viajes_vehiculo["Km_Recorridos"] = viajes_vehiculo["Km_Regreso"] - viajes_vehiculo["Km_Salida"]
    viajes_vehiculo["Gasolina_Usada"] = viajes_vehiculo["gasolina salida"] - viajes_vehiculo["gasolina regreso"]
    
    # Filtrar viajes con datos válidos
    viajes_validos = viajes_vehiculo[
        (viajes_vehiculo["Km_Recorridos"] > 0) & 
        (viajes_vehiculo["Gasolina_Usada"] > 0)
    ]
    
    if viajes_validos.empty:
        return 0.0
    
    # Calcular rendimiento promedio
    viajes_validos["Rendimiento"] = viajes_validos["Km_Recorridos"] / viajes_validos["Gasolina_Usada"]
    rendimiento_promedio = viajes_validos["Rendimiento"].mean()
    
    return round(rendimiento_promedio, 2)

def obtener_ultimo_viaje(id_vehiculo):
    """Obtiene el último viaje registrado para un vehículo"""
    df = cargar_reservas()
    if df.empty:
        return None
    
    # Filtrar por vehículo y ordenar por fecha descendente
    viajes_vehiculo = df[df['Vehículo'] == id_vehiculo]
    if viajes_vehiculo.empty:
        return None
    
    # Obtener el viaje más reciente
    ultimo_viaje = viajes_vehiculo.sort_values(by=['Fecha', 'Hora Fin'], ascending=False).iloc[0]
    return ultimo_viaje

def calcular_rendimiento_promedio(id_vehiculo):
    """Calcula el rendimiento promedio (km/l) de un vehículo"""
    df = cargar_reservas()
    if df.empty:
        return 0
    
    # Filtrar por vehículo
    viajes_vehiculo = df[df['Vehículo'] == id_vehiculo]
    if viajes_vehiculo.empty or len(viajes_vehiculo) < 2:
        return 0
    
    # Calcular rendimiento promedio
    total_km = 0
    total_combustible = 0
    
    for i in range(1, len(viajes_vehiculo)):
        viaje_actual = viajes_vehiculo.iloc[i]
        viaje_anterior = viajes_vehiculo.iloc[i-1]
        
        # Calcular km recorridos
        km_recorridos = viaje_actual['Km_Regreso'] - viaje_anterior['Km_Salida']
        
        # Calcular combustible usado
        combustible_usado = viaje_anterior['gasolina salida'] - viaje_actual['gasolina regreso']
        
        if combustible_usado > 0:
            total_km += km_recorridos
            total_combustible += combustible_usado
    
    if total_combustible == 0:
        return 0
    
    return round(total_km / total_combustible, 2)


def obtener_nombres_vehiculos():
    """Obtiene una lista con los nombres de todos los vehículos"""
    from .vehiculos import VEHICULOS
    return [f"{v['tipo']} - {v['placa']} ({v['asignado']})" for v in VEHICULOS]



