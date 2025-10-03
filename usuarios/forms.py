from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Estudiante, Calificacion

class RegistroEstudianteForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Crea una contraseña segura'
        }),
        min_length=8
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Repite tu contraseña'
        })
    )
    
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+593XXXXXXXXX',
            'pattern': '\+593\d{8,9}',
            'title': 'Formato: +593 seguido de 8-9 dígitos'
        }),
        help_text="Formato: +593XXXXXXXXX (opcional pero recomendado)"
    )
    
    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'apodo', 'correo', 'telefono', 'universidad']
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
        help_texts = {
            'telefono': 'Formato: +593XXXXXXXXX (opcional)',
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validar formato ecuatoriano
            if not telefono.startswith('+593'):
                raise forms.ValidationError('El número debe comenzar con +593 (código de Ecuador)')
            if len(telefono) not in [12, 13]:  # +593 + 8 o 9 dígitos
                raise forms.ValidationError('El número debe tener 12 o 13 dígitos incluyendo +593')
            if not telefono[4:].isdigit():
                raise forms.ValidationError('Solo se permiten números después del +593')
        return telefono
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        # Validaciones de seguridad
        if len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('La contraseña debe contener al menos un número')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula')
        
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
        # Crear usuario de Django
        user = User.objects.create_user(
            username=self.cleaned_data['correo'],
            email=self.cleaned_data['correo'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['nombres'],
            last_name=self.cleaned_data['apellidos']
        )
        
        # Crear estudiante
        estudiante = super().save(commit=False)
        estudiante.user = user
        
        if commit:
            estudiante.save()
        
        return estudiante

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.RadioSelect(choices=Calificacion.ESTRELLAS_OPCIONES),
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Comparte tu experiencia con este vendedor...',
                'class': 'form-control'
            }),
        }
        labels = {
            'estrellas': 'Calificación',
            'comentario': 'Comentario (opcional)'
        }