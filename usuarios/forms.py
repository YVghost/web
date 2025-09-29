from django import forms
from .models import Estudiante

class RegistroEstudianteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # campo adicional

    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'apodo', 'correo', 'password']
