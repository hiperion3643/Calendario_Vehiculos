
# Módulo de gestión de vehículos

# Lista completa de vehículos con sus placas y asignaciones
VEHICULOS = [
    {
        "id": "virtus_uee785b",
        "tipo": "Virtus",
        "placa": "UEE785B",
        "asignado": "Utilitario",
        "descripcion": "Vehículo utilitario general"
    },
    {
        "id": "virtus_uej654b",
        "tipo": "Virtus",
        "placa": "UEJ654B",
        "asignado": "Maestra Altagracia García Rosas",
        "descripcion": "Vehículo asignado a maestra Altagracia García Rosas"
    },
    {
        "id": "virtus_uej649b",
        "tipo": "Virtus",
        "placa": "UEJ649B",
        "asignado": "Abogado Eduardo Hernández Flores",
        "descripcion": "Vehículo asignado al abogado Eduardo Hernández Flores"
    },
    {
        "id": "virtus_uej682b",
        "tipo": "Virtus",
        "placa": "UEJ682B",
        "asignado": "Doctor Roberto Bautista Lozano",
        "descripcion": "Vehículo asignado al doctor Roberto Bautista Lozano"
    },
    {
        "id": "pickup_sr29947",
        "tipo": "Pick-up",
        "placa": "SR29947",
        "asignado": "Rector José Manuel Hernández Ramón",
        "descripcion": "Vehículo asignado al rector José Manuel Hernández Ramón"
    },
    {
        "id": "pickup_sr29944",
        "tipo": "Pick-up",
        "placa": "SR29944",
        "asignado": "Utilitaria",
        "descripcion": "Vehículo utilitario general"
    },
    {
        "id": "urvan_uek998b",
        "tipo": "Urvan",
        "placa": "UEK998B",
        "asignado": "Utilitaria",
        "descripcion": "Vehículo utilitario general"
    },
    {
        "id": "virtus_uej681b",
        "tipo": "Virtus",
        "placa": "UEJ681B",
        "asignado": "Licenciada Leticia Cid Aquino",
        "descripcion": "Vehículo asignado a la licenciada Leticia Cid Aquino"
    },
    {
        "id": "crafter_sp85378",
        "tipo": "Crafter",
        "placa": "SP85378",
        "asignado": "Utilitaria",
        "descripcion": "Vehículo utilitario general"
    },
    {
        "id": "versa_ucc121b",
        "tipo": "Versa",
        "placa": "UCC121B",
        "asignado": "Utilitario",
        "descripcion": "Vehículo utilitario general"
    }
]

def obtener_vehiculo_por_id(id_vehiculo):
    """Obtiene un vehículo por su ID"""
    for vehiculo in VEHICULOS:
        if vehiculo["id"] == id_vehiculo:
            return vehiculo
    return None

def obtener_vehiculo_por_placa(placa):
    """Obtiene un vehículo por su placa"""
    for vehiculo in VEHICULOS:
        if vehiculo["placa"] == placa:
            return vehiculo
    return None

def obtener_vehiculos_por_tipo(tipo):
    """Obtiene todos los vehículos de un tipo específico"""
    return [v for v in VEHICULOS if v["tipo"] == tipo]

def obtener_todos_vehiculos():
    """Retorna todos los vehículos"""
    return VEHICULOS

def obtener_nombres_vehiculos():
    """Retorna una lista con los nombres de los vehículos (tipo + placa)"""
    return [f"{v['tipo']} {v['placa']}" for v in VEHICULOS]
