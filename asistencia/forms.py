from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Empleado, RegistroAsistencia, Sucursal


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos. Verifica tus datos e intenta de nuevo.',
        'inactive': 'Esta cuenta está inactiva.',
    }

    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ej. juan.perez',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        }),
    )


class RegistroUsuarioForm(UserCreationForm):
    nombre = forms.CharField(
        label='Nombre Completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ej. Juan Pérez López',
        }),
    )
    rfc = forms.CharField(
        label='RFC',
        max_length=13,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. PELJ800101ABC',
            'maxlength': '13',
        }),
    )
    curp = forms.CharField(
        label='CURP',
        max_length=18,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. PELJ800101HDFRRN01',
            'maxlength': '18',
        }),
    )
    sucursal = forms.ModelChoiceField(
        label='Sucursal',
        queryset=Sucursal.objects.all(),
        required=False,
        empty_label='Selecciona una sucursal (opcional)',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = User
        fields = ('username', 'nombre', 'rfc', 'curp', 'sucursal', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej. juan.perez',
            'autocomplete': 'username',
        })
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'autocomplete': 'new-password',
        })

    def clean_rfc(self):
        rfc = self.cleaned_data['rfc'].strip().upper()
        if Empleado.objects.filter(rfc=rfc).exists():
            raise forms.ValidationError('Ya existe un empleado registrado con ese RFC.')
        return rfc

    def clean_curp(self):
        curp = self.cleaned_data['curp'].strip().upper()
        if Empleado.objects.filter(curp=curp).exists():
            raise forms.ValidationError('Ya existe un empleado registrado con esa CURP.')
        return curp

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        nombre = self.cleaned_data['nombre'].strip()
        user.first_name = nombre[:150]
        if commit:
            user.save()
            Empleado.objects.create(
                user=user,
                nombre=nombre,
                rfc=self.cleaned_data['rfc'],
                curp=self.cleaned_data['curp'],
                sucursal=self.cleaned_data.get('sucursal'),
                activo=True,
            )
        return user


class ChecadorForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ['tipo', 'nota']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nota': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej. Llegué tarde por el tráfico en el Periférico...',
            }),
        }


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'rfc', 'curp', 'sucursal', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ej. Juan Pérez López'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. PELJ800101ABC', 'maxlength': '13'}),
            'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. PELJ800101HDFRRN01', 'maxlength': '18'}),
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
