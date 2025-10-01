from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Importar User

class Estudiante(models.Model):
    UNIVERSIDADES = [
        ('EPN', 'Escuela Politécnica Nacional (EPN)'),
        ('USFQ', 'Universidad San Francisco de Quito (USFQ)'),
        ('PUCE', 'Pontificia Universidad Católica del Ecuador (PUCE)'),
        ('UCE', 'Universidad Central del Ecuador (UCE)'),
        ('UDLA', 'Universidad de Las Américas (UDLA)'),
        ('UTE', 'Universidad Tecnológica Equinoccial (UTE)'),
        ('UISRAEL', 'Universidad Tecnológica Israel (UISRAEL)'),
        ('UNIVERSIDAD_DEL_QUINDIO', 'Universidad del Quindío'),
        ('UNIVERSIDAD_INTERNACIONAL_SEK', 'Universidad Internacional SEK'),
        ('OTRA', 'Otra universidad'),
    ]
    
    # Relación con User de Django (RECOMENDADO)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    prestigio = models.IntegerField(default=0)
    contrasena = models.CharField(max_length=128)
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)
    universidad = models.CharField(
        max_length=100, 
        choices=UNIVERSIDADES,
        default='OTRA'  # ← AGREGAR VALOR POR DEFECTO
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"