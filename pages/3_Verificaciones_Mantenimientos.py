
# Página de Fechas Importantes

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, date, timedelta

# Añadir el directorio base al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehiculos import VEHICULOS
from data.gestion_datos import cargar_verificaciones

def mostrar_pagina():
    
    st.title("📅 Fechas Importantes")
    st.markdown("Consulta las fechas de verificación, mantenimiento, pago vehicular, tenencia, seguro, etc.")

    st.markdown("---")

    # Cargar datos de verificaciones
    df_verificaciones = cargar_verificaciones()

    # --- SECCIÓN DE ALERTAS ---
    st.markdown("### ⚠️ Alertas de Vencimiento Próximo")

    hoy = date.today()
    prox_30_dias = hoy + timedelta(days=30)

    alertas = []

    for idx, row in df_verificaciones.iterrows():
        # Verificar verificación
        if row["Próxima Verificación"]:
            fecha_verif = pd.to_datetime(row["Próxima Verificación"]).date()
            if fecha_verif <= prox_30_dias:
                alertas.append({
                    "Vehículo": f"{row['Placa']}",
                    "Tipo": "Verificación",
                    "Fecha Vencimiento": fecha_verif,
                    "Estado": row["Estado Verificación"]
                })

        # Verificar mantenimiento
        if row["Próximo Mantenimiento"]:
            fecha_mant = pd.to_datetime(row["Próximo Mantenimiento"]).date()
            if fecha_mant <= prox_30_dias:
                alertas.append({
                    "Vehículo": f"{row['Placa']}",
                    "Tipo": "Mantenimiento",
                    "Fecha Vencimiento": fecha_mant,
                    "Estado": row["Estado Mantenimiento"]
                })

        # Verificar control vehicular
        if row["Próximo Control Vehicular"]:
            fecha_ctrl = pd.to_datetime(row["Próximo Control Vehicular"]).date()
            if fecha_ctrl <= prox_30_dias:
                alertas.append({
                    "Vehículo": f"{row['Placa']}",
                    "Tipo": "Control Vehicular",
                    "Fecha Vencimiento": fecha_ctrl,
                    "Estado": row["Estado Control Vehicular"]
                })

    if alertas:
        df_alertas = pd.DataFrame(alertas)
        df_alertas = df_alertas.sort_values(by="Fecha Vencimiento")
        st.dataframe(df_alertas, use_container_width=True)
    else:
        st.success("✅ No hay vencimientos próximos en los próximos 30 días.")

    # --- VISUALIZACIÓN GENERAL ---
    st.markdown("### 📊 Resumen General")

    # Crear un resumen de todos los vehículos
    resumen = []
    for idx, row in df_verificaciones.iterrows():
        resumen.append({
            "Vehículo": f"{row['Placa']}",
            "Verificación": row["Estado Verificación"],
            "Próxima Verificación": row["Próxima Verificación"],
            "Mantenimiento": row["Estado Mantenimiento"],
            "Próximo Mantenimiento": row["Próximo Mantenimiento"],
            "Control Vehicular": row["Estado Control Vehicular"],
            "Próximo Control Vehicular": row["Próximo Control Vehicular"]
        })

    df_resumen = pd.DataFrame(resumen)
    st.dataframe(df_resumen, use_container_width=True)

if __name__ == "__main__":
    mostrar_pagina()
