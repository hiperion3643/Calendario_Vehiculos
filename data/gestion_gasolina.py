
# Módulo de gestión de gasolina para vehículos asignados

import pandas as pd
import os
from datetime import datetime, date, timedelta
from .vehiculos import VEHICULOS

# Rutas de archivos
DIR_DATA = os.path.dirname(os.path.abspath(__file__))
DIR_BASE = os.path.dirname(DIR_DATA)
FILE_GASOLINA = os.path.join(DIR_BASE, "data", "gasolina.csv")

# Lista de vehículos asignados (con límite semanal)
VEHICULOS_ASIGNADOS = [
    v for v in VEHICULOS 
    if v["asignado"] not in ["Utilitario", "Utilitaria"]
]

# Lista de vehículos utilitarios (sin límite semanal)
VEHICULOS_UTILITARIOS = [
    v for v in VEHICULOS 
    if v["asignado"] in ["Utilitario", "Utilitaria"]
]

# Monto semanal de gasolina asignado
MONTO_SEMANAL = 500.0

def inicializar_archivo_gasolina():
    """Inicializa el archivo de gasolina si no existe"""
    if not os.path.exists(FILE_GASOLINA):
        df = pd.DataFrame(columns=[
            "ID_Vehiculo",
            "Placa",
            "Asignado",
            "Fecha",
            "Semana",
            "Monto",
            "Estado"
        ])
        df.to_csv(FILE_GASOLINA, index=False)

def cargar_registros_gasolina():
    """Carga todos los registros de gasolina"""
    if not os.path.exists(FILE_GASOLINA):
        inicializar_archivo_gasolina()
    return pd.read_csv(FILE_GASOLINA)

def obtener_semana(fecha):
    """Obtiene el número de semana y año de una fecha"""
    return fecha.isocalendar()[1], fecha.year

def registrar_gasolina(id_vehiculo, monto, fecha=None):
    """Registra una recarga de gasolina para un vehículo"""
    df = cargar_registros_gasolina()

    # Buscar información del vehículo
    vehiculo = next((v for v in VEHICULOS if v["id"] == id_vehiculo), None)
    if not vehiculo:
        raise ValueError(f"Vehículo con ID {id_vehiculo} no encontrado")

    # Usar fecha actual si no se proporciona
    if fecha is None:
        fecha = date.today()

    # Obtener semana y año
    semana, anio = obtener_semana(fecha)

    # Verificar si ya tiene recarga esta semana (solo para vehículos asignados)
    if vehiculo["asignado"] not in ["Utilitario", "Utilitaria"]:
        registros_semana = df[
            (df["ID_Vehiculo"] == id_vehiculo) &
            (df["Semana"] == semana) &
            (df["Fecha"].str[:4].astype(int) == anio)
        ]
        if not registros_semana.empty:
            raise ValueError(f"El vehículo ya tiene una recarga registrada para la semana {semana} del año {anio}")

    # Crear nuevo registro
    nuevo_registro = {
        "ID_Vehiculo": id_vehiculo,
        "Placa": vehiculo["placa"],
        "Asignado": vehiculo["asignado"],
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Semana": semana,
        "Monto": monto,
        "Estado": "Completado"
    }

    # Agregar registro
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    df.to_csv(FILE_GASOLINA, index=False)

def obtener_estado_gasolina_semana(fecha=None):
    """Obtiene el estado de gasolina de todos los vehículos para una semana específica"""
    df = cargar_registros_gasolina()

    # Usar fecha actual si no se proporciona
    if fecha is None:
        fecha = date.today()

    # Obtener semana y año
    semana, anio = obtener_semana(fecha)

    # Filtrar registros de la semana
    registros_semana = df[
        (df["Fecha"].str[:4].astype(int) == anio) &
        (df["Semana"] == semana)
    ]

    # Crear DataFrame con estado de todos los vehículos asignados
    estado = []
    for vehiculo in VEHICULOS_ASIGNADOS:
        registro = registros_semana[registros_semana["ID_Vehiculo"] == vehiculo["id"]]

        if not registro.empty:
            estado_vehiculo = {
                "ID_Vehiculo": vehiculo["id"],
                "Tipo": vehiculo["tipo"],
                "Placa": vehiculo["placa"],
                "Asignado": vehiculo["asignado"],
                "Fecha_Recarga": registro.iloc[0]["Fecha"],
                "Monto": registro.iloc[0]["Monto"],
                "Estado": "✅ Recargado",
                "Semana": semana,
                "Anio": anio
            }
        else:
            estado_vehiculo = {
                "ID_Vehiculo": vehiculo["id"],
                "Tipo": vehiculo["tipo"],
                "Placa": vehiculo["placa"],
                "Asignado": vehiculo["asignado"],
                "Fecha_Recarga": "Pendiente",
                "Monto": MONTO_SEMANAL,
                "Estado": "⏳ Pendiente",
                "Semana": semana,
                "Anio": anio
            }

        estado.append(estado_vehiculo)

    # Agregar vehículos utilitarios (sin límite semanal)
    for vehiculo in VEHICULOS_UTILITARIOS:
        registros_vehiculo = df[df["ID_Vehiculo"] == vehiculo["id"]]

        if not registros_vehiculo.empty:
            # Obtener la última recarga de la semana
            recargas_semana = registros_vehiculo[
                (registros_vehiculo["Fecha"].str[:4].astype(int) == anio) &
                (registros_vehiculo["Semana"] == semana)
            ]

            if not recargas_semana.empty:
                total_monto = recargas_semana["Monto"].sum()
                estado_vehiculo = {
                    "ID_Vehiculo": vehiculo["id"],
                    "Tipo": vehiculo["tipo"],
                    "Placa": vehiculo["placa"],
                    "Asignado": vehiculo["asignado"],
                    "Fecha_Recarga": f"{len(recargas_semana)} recarga(s)",
                    "Monto": total_monto,
                    "Estado": "✅ Recargado",
                    "Semana": semana,
                    "Anio": anio
                }
            else:
                estado_vehiculo = {
                    "ID_Vehiculo": vehiculo["id"],
                    "Tipo": vehiculo["tipo"],
                    "Placa": vehiculo["placa"],
                    "Asignado": vehiculo["asignado"],
                    "Fecha_Recarga": "Sin recargas",
                    "Monto": 0,
                    "Estado": "⏳ Sin recargas",
                    "Semana": semana,
                    "Anio": anio
                }
        else:
            estado_vehiculo = {
                "ID_Vehiculo": vehiculo["id"],
                "Tipo": vehiculo["tipo"],
                "Placa": vehiculo["placa"],
                "Asignado": vehiculo["asignado"],
                "Fecha_Recarga": "Sin recargas",
                "Monto": 0,
                "Estado": "⏳ Sin recargas",
                "Semana": semana,
                "Anio": anio
            }

        estado.append(estado_vehiculo)

    return pd.DataFrame(estado)

def obtener_historico_gasolina(id_vehiculo=None, anio=None):
    """Obtiene el histórico de recargas de gasolina"""
    df = cargar_registros_gasolina()

    if id_vehiculo:
        df = df[df["ID_Vehiculo"] == id_vehiculo]

    if anio:
        df = df[df["Fecha"].str[:4].astype(int) == anio]

    return df.sort_values("Fecha", ascending=False)
