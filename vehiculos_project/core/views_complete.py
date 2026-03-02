from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime, time
from .models import Vehiculo, Reserva, Documentacion, Fotomulta
from .services import GoogleSheetsService

# Instancia del servicio
gs_service = GoogleSheetsService()

def home(request):
    # Datos para el dashboard
    total_vehiculos = Vehiculo.objects.count()
    reservas_hoy = Reserva.objects.filter(fecha=date.today()).count()

    # Contar vehículos por estado
    vehiculos_disponibles = Vehiculo.objects.filter(estado='DIS').count()
    vehiculos_en_uso = Vehiculo.objects.filter(estado='OCU').count()
    vehiculos_mantenimiento = Vehiculo.objects.filter(estado='MAN').count()

    context = {
        'total_vehiculos': total_vehiculos,
        'reservas_hoy': reservas_hoy,
        'vehiculos_disponibles': vehiculos_disponibles,
        'vehiculos_en_uso': vehiculos_en_uso,
        'vehiculos_mantenimiento': vehiculos_mantenimiento,
    }
    return render(request, 'core/home.html', context)

def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'core/lista_vehiculos.html', {'vehiculos': vehiculos})

def lista_reservas(request):
    # Obtenemos datos de BD
    reservas = Reserva.objects.select_related('vehiculo').all().order_by('-fecha', '-hora_salida')
    return render(request, 'core/lista_reservas.html', {'reservas': reservas})

def crear_reserva(request):
    if request.method == 'POST':
        # Procesar formulario
        vehiculo_id = request.POST.get('vehiculo')
        fecha_str = request.POST.get('fecha')
        hora_salida_str = request.POST.get('hora_salida')
        solicitante = request.POST.get('solicitante')
        area = request.POST.get('area')
        contacto = request.POST.get('contacto')
        motivo = request.POST.get('motivo', '')

        # Validaciones
        try:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            hora_salida = datetime.strptime(hora_salida_str, "%H:%M").time()

            # Verificar disponibilidad del vehículo
            if vehiculo.estado != 'DIS':
                messages.error(request, "El vehículo seleccionado no está disponible.")
                return redirect('crear_reserva')

            # Verificar si ya existe una reserva para el mismo vehículo en la misma fecha
            reserva_existente = Reserva.objects.filter(
                vehiculo=vehiculo,
                fecha=fecha,
                estado='ACT'
            ).exists()

            if reserva_existente:
                messages.error(request, "El vehículo ya tiene una reserva activa para esta fecha.")
                return redirect('crear_reserva')

            # Guardar en BD local
            Reserva.objects.create(
                vehiculo=vehiculo,
                fecha=fecha,
                hora_salida=hora_salida,
                solicitante=solicitante,
                area=area,
                contacto=contacto,
                estado='ACT'
            )

            # Opcional: Guardar en Google Sheets
            try:
                datos_reserva = {
                    'fecha': fecha,
                    'vehiculo': vehiculo.nombre,
                    'solicitante': solicitante,
                    'area': area,
                    'contacto': contacto,
                    'motivo': motivo,
                    'hora_salida': hora_salida,
                }
                if gs_service.add_reservation(datos_reserva):
                    messages.success(request, "Reserva creada exitosamente y sincronizada con Google Sheets.")
                else:
                    messages.success(request, "Reserva creada exitosamente (sin sincronización con Google Sheets).")
            except Exception as e:
                messages.success(request, "Reserva creada exitosamente (sin sincronización con Google Sheets).")

            return redirect('lista_reservas')

        except Exception as e:
            messages.error(request, f"Error al crear la reserva: {e}")

    # GET: Mostrar formulario vacío
    vehiculos = Vehiculo.objects.filter(estado='DIS')
    vehiculo_seleccionado = request.GET.get('vehiculo')
    context = {
        'vehiculos': vehiculos,
        'vehiculo_seleccionado': int(vehiculo_seleccionado) if vehiculo_seleccionado else None
    }
    return render(request, 'core/crear_reserva.html', context)

def actualizar_regreso(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        vehiculo_id = request.POST.get('vehiculo')
        hora_salida_str = request.POST.get('hora_salida')
        hora_regreso_str = request.POST.get('hora_regreso')

        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            hora_salida = datetime.strptime(hora_salida_str, "%H:%M").time()
            hora_regreso = datetime.strptime(hora_regreso_str, "%H:%M").time()

            # Actualizar en BD
            reserva = Reserva.objects.get(
                vehiculo=vehiculo,
                fecha=fecha,
                hora_salida=hora_salida
            )
            reserva.hora_regreso = hora_regreso
            reserva.estado = 'COM'
            reserva.save()

            # Actualizar estado del vehículo a disponible
            vehiculo.estado = 'DIS'
            vehiculo.save()

            # Opcional: Actualizar en Google Sheets
            try:
                if gs_service.update_return_time(fecha, vehiculo.nombre, hora_salida, hora_regreso):
                    messages.success(request, "Hora de regreso actualizada exitosamente.")
                else:
                    messages.success(request, "Hora de regreso actualizada en la base de datos local.")
            except Exception as e:
                messages.success(request, "Hora de regreso actualizada en la base de datos local.")

            return redirect('lista_reservas')
        except Exception as e:
            messages.error(request, f"Error al actualizar: {e}")

    return redirect('lista_reservas')

def estado_vehiculos(request):
    disponibles = Vehiculo.objects.filter(estado='DIS')
    en_uso = Vehiculo.objects.filter(estado='OCU')
    mantenimiento = Vehiculo.objects.filter(estado='MAN')

    context = {
        'disponibles': disponibles,
        'en_uso': en_uso,
        'mantenimiento': mantenimiento,
    }
    return render(request, 'core/estado_vehiculos.html', context)

def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    fotos = vehiculo.fotos.all()
    context = {
        'vehiculo': vehiculo,
        'fotos': fotos,
        'hoy': date.today()
    }
    return render(request, 'core/detalle_vehiculo.html', context)

def documentacion(request):
    docs = Documentacion.objects.select_related('vehiculo').all()
    context = {
        'documentacion': docs,
        'hoy': date.today()
    }
    return render(request, 'core/documentacion.html', context)

def fotomultas(request):
    multas = Fotomulta.objects.select_related('vehiculo').all()
    return render(request, 'core/fotomultas.html', {'multas': multas})
