from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Empleado, RegistroAsistencia, Sucursal


class AuthYChecadorTests(TestCase):
    def setUp(self):
        self.sucursal = Sucursal.objects.create(nombre='Matriz', direccion='Av. Central 100')

    def test_checador_requiere_login(self):
        resp = self.client.get(reverse('registrar_checada'))
        self.assertRedirects(resp, f"{reverse('login')}?next={reverse('registrar_checada')}")

    def test_registro_crea_usuario_empleado_y_permite_checar(self):
        resp = self.client.post(reverse('registro'), {
            'username': 'ana.gomez',
            'nombre': 'Ana Gómez',
            'rfc': 'goma900101abc',
            'curp': 'goma900101mdfrrn01',
            'sucursal': self.sucursal.id,
            'password1': 'ClaveSegura123!',
            'password2': 'ClaveSegura123!',
        })
        self.assertRedirects(resp, reverse('registrar_checada'))

        user = User.objects.get(username='ana.gomez')
        empleado = Empleado.objects.get(user=user)
        self.assertEqual(empleado.rfc, 'GOMA900101ABC')
        self.assertEqual(empleado.curp, 'GOMA900101MDFRRN01')

        # Registrar entrada
        resp_entrada = self.client.post(reverse('registrar_checada'), {
            'tipo': 'ENTRADA',
            'nota': 'Llegada puntual',
        })
        self.assertRedirects(resp_entrada, reverse('registrar_checada'))

        # Registrar salida
        resp_salida = self.client.post(reverse('registrar_checada'), {
            'tipo': 'SALIDA',
            'nota': 'Fin de jornada',
        })
        self.assertRedirects(resp_salida, reverse('registrar_checada'))

        registros = RegistroAsistencia.objects.filter(empleado=empleado)
        self.assertEqual(registros.count(), 2)
        self.assertEqual(list(registros.order_by('id').values_list('tipo', flat=True)), ['ENTRADA', 'SALIDA'])

    def test_logout_y_login(self):
        user = User.objects.create_user(username='carlos', password='PasswordFuerte99!')
        Empleado.objects.create(
            user=user,
            nombre='Carlos Ruiz',
            rfc='RUIC910202XYZ',
            curp='RUIC910202HDFRRN02',
        )

        self.client.post(reverse('login'), {'username': 'carlos', 'password': 'PasswordFuerte99!'})
        resp_checador = self.client.get(reverse('registrar_checada'))
        self.assertEqual(resp_checador.status_code, 200)
        self.assertContains(resp_checador, 'Carlos Ruiz')

        resp_logout = self.client.post(reverse('logout'))
        self.assertRedirects(resp_logout, reverse('login'))

        resp_protegida = self.client.get(reverse('registrar_checada'))
        self.assertEqual(resp_protegida.status_code, 302)
