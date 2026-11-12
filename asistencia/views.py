from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import ChecadorForm, EmpleadoForm, LoginForm, RegistroUsuarioForm
from .models import Empleado, RegistroAsistencia


def login_view(request):
    if request.user.is_authenticated:
        return redirect('registrar_checada')

    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('registrar_checada')
    else:
        login_form = LoginForm(request)

    return render(request, 'asistencia/auth.html', {
        'login_form': login_form,
        'registro_form': RegistroUsuarioForm(),
        'active_tab': 'login',
        'next': request.GET.get('next', ''),
    })


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('registrar_checada')

    if request.method == 'POST':
        registro_form = RegistroUsuarioForm(request.POST)
        if registro_form.is_valid():
            user = registro_form.save()
            login(request, user)
            messages.success(
                request,
                f'¡Cuenta creada con éxito! Bienvenido, {user.empleado.nombre}. Ya puedes registrar tu asistencia.',
            )
            return redirect('registrar_checada')
    else:
        registro_form = RegistroUsuarioForm()

    return render(request, 'asistencia/auth.html', {
        'login_form': LoginForm(request),
        'registro_form': registro_form,
        'active_tab': 'registro',
        'next': request.GET.get('next', ''),
    })


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required
def registrar_checada(request):
    empleado = Empleado.objects.select_related('sucursal').filter(user=request.user).first()

    if empleado is None:
        return render(request, 'asistencia/checador.html', {
            'empleado': None,
            'form': None,
            'ultimos_registros': [],
        })

    ultima_checada = RegistroAsistencia.objects.filter(empleado=empleado).order_by('-fecha_hora').first()
    tipo_sugerido = 'SALIDA' if ultima_checada and ultima_checada.tipo == 'ENTRADA' else 'ENTRADA'

    if request.method == 'POST':
        form = ChecadorForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.empleado = empleado
            registro.save()
            etiqueta = 'Entrada' if registro.tipo == 'ENTRADA' else 'Salida'
            messages.success(request, f'¡{etiqueta} registrada con éxito! Buen día de trabajo.')
            return redirect('registrar_checada')
    else:
        form = ChecadorForm(initial={'tipo': tipo_sugerido})

    ultimos_registros = RegistroAsistencia.objects.filter(empleado=empleado).order_by('-fecha_hora')[:5]

    return render(request, 'asistencia/checador.html', {
        'empleado': empleado,
        'form': form,
        'ultimos_registros': ultimos_registros,
    })


@login_required
def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Trabajador registrado con éxito en el sistema!')
            return redirect('registrar_empleado')
    else:
        form = EmpleadoForm()

    empleados = Empleado.objects.select_related('sucursal').all().order_by('-id')

    return render(request, 'asistencia/empleados.html', {
        'form': form,
        'empleados': empleados,
    })
