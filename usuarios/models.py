from django.db import models

class Estudiante(models.Model):
    banner_id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    carrera = models.CharField(max_length=100)
    prestigio = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.carrera})"
