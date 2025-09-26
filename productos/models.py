from django.db import models
from usuarios.models import Estudiante  # Relación con el vendedor

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    publicado_en = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=False, blank=False)

    class Meta:
        ordering = ['-publicado_en']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
