from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_checada, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('checador/', views.registrar_checada, name='registrar_checada'),
    path('empleados/', views.registrar_empleado, name='registrar_empleado'),
]
