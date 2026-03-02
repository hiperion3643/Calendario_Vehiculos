from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/actualizar-regreso/', views.actualizar_regreso, name='actualizar_regreso'),
    path('estado/', views.estado_vehiculos, name='estado_vehiculos'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('fotomultas/', views.fotomultas, name='fotomultas'),
]
