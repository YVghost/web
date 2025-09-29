from django.db import models
from django.utils import timezone

class Estudiante(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    prestigio = models.IntegerField(default=0)
    contrasena = models.CharField(max_length=128) 
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

