from django.contrib import admin
from .models import Sucursal, Empleado, RegistroAsistencia

admin.site.register(Sucursal)
admin.site.register(Empleado)
admin.site.register(RegistroAsistencia)
