from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Vehiculo(models.Model):
    ESTADO_CHOICES = [
        ('DIS', 'Disponible'),
        ('OCU', 'En uso'),
        ('MAN', 'En mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='DIS')
    descripcion = models.TextField()
    placas = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.nombre

class FotoVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='vehiculos_fotos/')
    descripcion = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.vehiculo.nombre} - {self.descripcion}"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('ACT', 'Activa'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
    ]
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    contacto = models.CharField(max_length=20)
    fecha = models.DateField()
    hora_salida = models.TimeField()
    hora_regreso = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='ACT')
    
    def __str__(self):
        return f"{self.vehiculo.nombre} - {self.fecha} {self.hora_salida}"

class Documentacion(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    verificacion = models.DateField()
    tenencia = models.CharField(max_length=20) # Pagada, Pendiente, etc.
    control = models.DateField()
    seguro_vigencia = models.DateField()
    
    def __str__(self):
        return f"Doc {self.vehiculo.nombre}"

class Fotomulta(models.Model):
    ESTADO_CHOICES = [
        ('PEN', 'Pendiente'),
        ('PRO', 'En proceso'),
        ('PAG', 'Pagada'),
    ]
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField()
    motivo = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES)
    ubicacion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Multa {self.vehiculo.nombre} - {self.fecha}"

