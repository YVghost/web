from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

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
    
    # Validator para teléfono ecuatoriano
    phone_regex = RegexValidator(
        regex=r'^\+593\d{8,9}$',
        message="El número debe estar en formato: +593XXXXXXXXX. (9-10 dígitos después del código país)"
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=13, 
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text="Formato: +593XXXXXXXXX"
    )
    universidad = models.CharField(
        max_length=50, 
        choices=UNIVERSIDADES, 
        default='OTRA'
    )
    prestigio = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False)
    
    # Campos adicionales
    es_vendedor_verificado = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Breve descripción sobre ti")
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def telefono_formateado(self):
        if self.telefono:
            return f"{self.telefono[:4]} {self.telefono[4:7]} {self.telefono[7:]}"
        return "No registrado"
    
    def tiene_telefono_verificado(self):
        return bool(self.telefono)
    
    # Métodos para calificaciones
    def actualizar_prestigio(self):
        """Actualizar el prestigio basado en las calificaciones"""
        calificaciones = self.calificaciones_recibidas.all()
        if calificaciones.exists():
            promedio = calificaciones.aggregate(models.Avg('estrellas'))['estrellas__avg']
            self.prestigio = round(promedio * 20)  # Convertir a escala 0-100
        else:
            self.prestigio = 0
        self.save(update_fields=['prestigio'])
    
    @property
    def promedio_calificaciones(self):
        """Obtener el promedio de calificaciones"""
        calificaciones = self.calificaciones_recibidas.all()
        if calificaciones.exists():
            return calificaciones.aggregate(models.Avg('estrellas'))['estrellas__avg']
        return 0
    
    @property
    def total_calificaciones(self):
        """Obtener el total de calificaciones recibidas"""
        return self.calificaciones_recibidas.count()
    
    @property
    def estrellas_display(self):
        """Mostrar estrellas formateadas"""
        promedio = self.promedio_calificaciones
        if promedio == 0:
            return "Sin calificaciones"
        
        estrellas_llenas = int(promedio)
        media_estrella = promedio - estrellas_llenas >= 0.5
        estrellas_vacias = 5 - estrellas_llenas - (1 if media_estrella else 0)
        
        display = "⭐" * estrellas_llenas
        if media_estrella:
            display += "✨"
        display += "☆" * estrellas_vacias
        
        return f"{display} ({promedio:.1f})"
    
    def puede_calificar(self, estudiante):
        """Verificar si puede calificar a otro estudiante"""
        if self == estudiante:
            return False  # No puede calificarse a sí mismo
        return True
    
    def ha_calificado_a(self, estudiante):
        """Verificar si ya ha calificado a este estudiante"""
        return self.calificaciones_hechas.filter(calificado=estudiante).exists()

class Calificacion(models.Model):
    """Sistema de calificaciones entre usuarios"""
    ESTRELLAS_OPCIONES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    calificador = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='calificaciones_hechas'
    )
    calificado = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='calificaciones_recibidas'
    )
    estrellas = models.IntegerField(choices=ESTRELLAS_OPCIONES)
    comentario = models.TextField(max_length=500, blank=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)
    
    # Relación con producto (opcional)
    producto = models.ForeignKey(
        'productos.Producto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    class Meta:
        unique_together = ['calificador', 'calificado', 'producto']
        ordering = ['-fecha_calificacion']
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
    
    def __str__(self):
        return f"{self.calificador} → {self.calificado}: {self.estrellas}⭐"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar el prestigio del estudiante calificado
        self.calificado.actualizar_prestigio()