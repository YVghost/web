from django.db import models

class Estudiante(models.Model):
    banner_id = models.CharField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    carrera = models.CharField(max_length=100)
    prestigio = models.IntegerField(default=0)
    contrasena = models.CharField(max_length=128) 

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.carrera})"

