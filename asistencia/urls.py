from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_checada, name='inicio'),
    path('checador/', views.registrar_checada, name='registrar_checada'),
    path('empleados/', views.registrar_empleado, name='registrar_empleado'),
]