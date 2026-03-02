from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Vehiculo, FotoVehiculo, Reserva, Documentacion, Fotomulta

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'placas', 'estado', 'descripcion_corta')
    list_filter = ('estado',)
    search_fields = ('nombre', 'placas')

    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

@admin.register(FotoVehiculo)
class FotoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'descripcion', 'imagen_preview')
    list_filter = ('vehiculo',)
    search_fields = ('vehiculo__nombre', 'descripcion')

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Vista previa'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'solicitante', 'area', 'fecha', 'hora_salida', 'hora_regreso', 'estado')
    list_filter = ('estado', 'fecha', 'vehiculo')
    search_fields = ('solicitante', 'area', 'vehiculo__nombre')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora_salida')

@admin.register(Documentacion)
class DocumentacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'verificacion', 'tenencia', 'control', 'seguro_vigencia', 'documentos_vigentes')
    list_filter = ('verificacion', 'tenencia', 'control', 'seguro_vigencia')
    search_fields = ('vehiculo__nombre',)

    def documentos_vigentes(self, obj):
        from datetime import date
        hoy = date.today()
        vigentes = []

        if obj.verificacion >= hoy:
            vigentes.append("Verificación")
        if obj.control >= hoy:
            vigentes.append("Control")
        if obj.seguro_vigencia >= hoy:
            vigentes.append("Seguro")

        if vigentes:
            return format_html('<span style="color: green;">{}</span>', ", ".join(vigentes))
        return format_html('<span style="color: red;">Ningún documento vigente</span>')
    documentos_vigentes.short_description = 'Documentos Vigentes'

@admin.register(Fotomulta)
class FotomultaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha', 'motivo_corto', 'monto', 'estado', 'ubicacion')
    list_filter = ('estado', 'fecha', 'vehiculo')
    search_fields = ('vehiculo__nombre', 'motivo', 'ubicacion')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

    def motivo_corto(self, obj):
        return obj.motivo[:50] + '...' if len(obj.motivo) > 50 else obj.motivo
    motivo_corto.short_description = 'Motivo' 
