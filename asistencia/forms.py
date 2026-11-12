from django import forms
from .models import RegistroAsistencia, Empleado

class ChecadorForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ['empleado', 'tipo', 'nota']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'tipo': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'nota': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ej. Llegué tarde por el tráfico en el Periférico...'
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