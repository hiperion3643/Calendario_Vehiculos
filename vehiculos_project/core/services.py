import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import pandas as pd
from datetime import datetime, date, time

# Configuración
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'client_secret.json' # Asegúrate de poner este archivo en la raíz del proyecto o en settings

class GoogleSheetsService:
    def __init__(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open("Gestión de Vehículos").sheet1
        except Exception as e:
            print(f"Error conectando a Google Sheets: {e}")
            self.sheet = None

    def get_all_reservations(self):
        if not self.sheet: return []
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        # Lógica de conversión de fechas similar a la de Streamlit...
        return df.to_dict('records')

    def add_reservation(self, reservation_data):
        if not self.sheet: return False
        # reservation_data es un diccionario con los datos
        row = [
            reservation_data.get('fecha'),
            reservation_data.get('vehiculo'),
            reservation_data.get('solicitante'),
            # ... resto de campos
        ]
        self.sheet.append_row(row)
        return True

    def update_return_time(self, fecha, vehiculo, hora_salida, hora_regreso):
        if not self.sheet: return False
        # Lógica para buscar y actualizar la celda específica
        filas = self.sheet.get_all_values()
        for i, fila in enumerate(filas[1:], start=2):
            if (fila[0] == fecha.strftime("%Y-%m-%d") and 
                fila[1] == vehiculo and 
                fila[5] == hora_salida.strftime("%H:%M")):
                self.sheet.update_cell(i, 7, hora_regreso.strftime("%H:%M"))
                return True
        return False
