# checkout/models.py
from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto

class Orden(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('paypal', 'PayPal'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    paypal_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.comprador.username} ({self.metodo_pago})"
