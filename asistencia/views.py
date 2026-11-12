from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ChecadorForm, EmpleadoForm
from .models import RegistroAsistencia, Empleado

# Create your views here.

def registrar_checada(request):
    if request.method == 'POST':
        form = ChecadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Checada registrada con éxito! Buen día de trabajo.")
            return redirect('registrar_checada')
    else:
        form = ChecadorForm()
    
    ultimos_registros = RegistroAsistencia.objects.order_by('-fecha_hora')[:5]
    
    return render(request, 'asistencia/checador.html', {
        'form': form,
        'ultimos_registros': ultimos_registros
    })

def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Trabajador registrado con éxito en el sistema!")
            return redirect('registrar_empleado')
    else:
        form = EmpleadoForm()
    
    empleados = Empleado.objects.all().order_by('-id')
    
    return render(request, 'asistencia/empleados.html', {
        'form': form,
        'empleados': empleados})