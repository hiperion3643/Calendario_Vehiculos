# Sistema de Gestión de Vehículos

Sistema web para la consulta del estado de vehículos de la universidad, incluyendo reserva de vehículos, control de estado, verificaciones, mantenimientos y fotomultas.

## Características

- 📅 **Calendario de Reservas**: Consulta de reservas de vehículos con control de horarios
- 🚗 **Estado de Vehículos**: Consulta del estado de cada vehículo con imágenes
- 🔧 **Verificaciones y Mantenimientos**: Consulta de fechas de verificación, mantenimiento y control vehicular
- 🚦 **Fotomultas**: Consulta de infracciones de tránsito

## Estructura del Proyecto

```
Calendario/
├── app.py                          # Aplicación principal (redirige al calendario)
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── reservas.csv                    # Archivo de datos de reservas
├── data/
│   ├── __init__.py
│   ├── vehiculos.py                # Información de los 10 vehículos
│   ├── gestion_datos.py            # Funciones para gestión de datos
│   ├── estado_vehiculos.csv        # Archivo de estado de vehículos
│   ├── verificaciones.csv          # Archivo de verificaciones
│   ├── fotomultas.csv             # Archivo de fotomultas
│   └── imagenes/                   # Directorio para imágenes de vehículos
└── pages/
    ├── __init__.py
    ├── 1_Calendario_Reservas.py    # Página de calendario de reservas
    ├── 2_Estado_Vehiculos.py       # Página de estado de vehículos
    ├── 3_Verificaciones_Mantenimientos.py  # Página de verificaciones
    └── 4_Fotomultas.py            # Página de fotomultas
```

## Instalación

1. Asegúrate de tener Python 3.8 o superior instalado
2. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la aplicación, ejecuta el siguiente comando en el directorio del proyecto:

```bash
streamlit run app.py
```

## Vehículos Registrados

El sistema cuenta con 10 vehículos registrados:

1. Virtus UEE785B - Utilitario
2. Virtus UEJ654B - Maestra Altagracia García Rosas
3. Virtus UEJ649B - Abogado Eduardo Hernández Flores
4. Virtus UEJ682B - Doctor Roberto Bautista Lozano
5. Pick-up SR29947 - Rector José Manuel Hernández Ramón
6. Pick-up SR29944 - Utilitaria
7. Urvan UEK998B - Utilitaria
8. Virtus UEJ681B - Licenciada Leticia Cid Aquino
9. Crafter SP85378 - Utilitaria
10. Versa UCC121B - Utilitario

## Uso

1. **Panel Principal**: La aplicación redirige automáticamente al calendario de reservas
2. **Calendario de Reservas**: Consulta la disponibilidad de vehículos y las reservas existentes
3. **Estado de Vehículos**: Consulta el estado de cada vehículo, incluyendo imágenes
4. **Verificaciones y Mantenimientos**: Consulta las fechas de verificación, mantenimiento y control vehicular
5. **Fotomultas**: Consulta las infracciones de tránsito registradas

## Contacto

Para más información o soporte, contacta a:
- Email: transporte@universidad.edu
- Teléfono: +52 555 555 5555
