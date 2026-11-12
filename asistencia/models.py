from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empleado')
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13, unique=True, help_text="RFC del SAT")
    curp = models.CharField(max_length=18, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class RegistroAsistencia(models.Model):
    TIPO_REGISTRO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_REGISTRO)
    fecha_hora = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True, null=True, help_text="Ej. Retardo")

    def __str__(self):
        return f"{self.empleado.nombre} - {self.tipo}"