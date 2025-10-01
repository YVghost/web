from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Estudiante

class RegistroEstudianteForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Crea una contraseña segura'
        }),
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Repite tu contraseña'
        })
    )
    
    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'apodo', 'correo', 'universidad']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tus nombres'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tus apellidos'
            }),
            'apodo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tu apodo (opcional)'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'correo@universidad.edu.ec'
            }),
            'universidad': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('Este correo ya está registrado')
        return correo
    
    def clean_apodo(self):
        apodo = self.cleaned_data.get('apodo')
        if apodo and Estudiante.objects.filter(apodo=apodo).exists():
            raise forms.ValidationError('Este apodo ya está en uso')
        return apodo
    
    def save(self, commit=True):
        # Crear usuario de Django (ENCRIPTA la contraseña automáticamente)
        user = User.objects.create_user(
            username=self.cleaned_data['correo'],
            email=self.cleaned_data['correo'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['nombres'],
            last_name=self.cleaned_data['apellidos']
        )
        
        # Crear estudiante
        estudiante = super().save(commit=False)
        estudiante.user = user  # Relacionar con el usuario de Django
        
        if commit:
            estudiante.save()
        
        return estudiante