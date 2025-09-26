from django import forms
from .models import Estudiante

class RegistroEstudianteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # campo adicional

    class Meta:
        model = Estudiante
        fields = ['banner_id','nombres', 'apellidos', 'apodo', 'correo', 'carrera', 'password']
