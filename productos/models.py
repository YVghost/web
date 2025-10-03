from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from usuarios.models import Estudiante

class Categoria(models.Model):
    """Categorías para organizar productos"""
    CATEGORIAS_UNIVERSITARIAS = [
        ('libros_texto', '📚 Libros de Texto'),
        ('apuntes_guias', '📝 Apuntes y Guías'),
        ('electronica', '💻 Electrónica'),
        ('instrumentos_laboratorio', '🔬 Instrumentos Lab'),
        ('ropa', '👕 Ropa'),
        ('deportes', '⚽ Deportes'),
        ('comida', '🍕 Comida'),
        ('accesorios', '🎒 Accesorios'),
        ('muebles_hogar', '🛋️ Muebles Hogar'),
        ('arte_musica', '🎨 Arte y Música'),
        ('servicios', '🛠️ Servicios'),
        ('otros', '📦 Otros'),
    ]
    
    nombre = models.CharField(max_length=50, choices=CATEGORIAS_UNIVERSITARIAS, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, default='📦')
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.get_nombre_display()
    
    @property
    def cantidad_productos(self):
        return self.productos.filter(estado='disponible').count()

class Producto(models.Model):
    ESTADO_OPCIONES = [
        ('disponible', '🟢 Disponible'),
        ('vendido', '🔴 Vendido'),
        ('reservado', '🟡 Reservado'),
        ('inactivo', '⚫ Inactivo'),
    ]
    
    CONDICION_OPCIONES = [
        ('nuevo', '🆕 Nuevo'),
        ('como_nuevo', '🌟 Como nuevo'),
        ('bueno', '👍 Bueno'),
        ('regular', '✅ Regular'),
        ('necesita_reparacion', '🔧 Necesita reparación'),
    ]
    
    TIPO_ENVIO_OPCIONES = [
        ('recoger', '🏫 Recoger en universidad'),
        ('envio', '🚗 Envío a domicilio'),
        ('ambos', '📦 Ambos'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    
    # Precio y condiciones
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    condicion = models.CharField(max_length=20, choices=CONDICION_OPCIONES, default='bueno')
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='disponible')
    
    # Stock y disponibilidad
    stock = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    es_multiple = models.BooleanField(default=False)
    
    # Entrega y ubicación - ELIMINADO campo ubicación fijo
    tipo_envio = models.CharField(max_length=10, choices=TIPO_ENVIO_OPCIONES, default='recoger')
    
    # Metadatos
    vendedor = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='productos_vendidos')
    publicado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    visitas = models.PositiveIntegerField(default=0)
    
    # Búsqueda
    tags = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-publicado_en']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    @property
    def precio_formateado(self):
        return f"${self.precio:,.2f}"
    
    @property
    def tiene_stock(self):
        return self.stock > 0 and self.estado == 'disponible'
    
    @property
    def cantidad_favoritos(self):
        return self.en_favoritos.count()
    
    @property
    def ubicacion(self):
        """Obtener la ubicación automáticamente del vendedor"""
        if self.vendedor and self.vendedor.universidad:
            return self.vendedor.get_universidad_display()
        return "Ubicación no especificada"
    
    @property 
    def icono_universidad(self):
        """Icono según la universidad del vendedor"""
        iconos_universidades = {
            'EPN': '🏛️',
            'USFQ': '🎓', 
            'PUCE': '⛪',
            'UCE': '🏫',
            'UDLA': '🌎',
            'UTE': '🔧',
            'UISRAEL': '✡️',
            'UNIVERSIDAD_DEL_QUINDIO': '☕',
            'UNIVERSIDAD_INTERNACIONAL_SEK': '🌍',
            'OTRA': '🏢'
        }
        if self.vendedor and self.vendedor.universidad:
            return iconos_universidades.get(self.vendedor.universidad, '🏢')
        return '🏢'
    
    @property
    def ubicacion_completa(self):
        """Ubicación con icono para mostrar en templates"""
        return f"{self.icono_universidad} {self.ubicacion}"
    
    @property
    def es_nuevo(self):
        """Verificar si el producto fue publicado en las últimas 24 horas"""
        from django.utils import timezone
        return (timezone.now() - self.publicado_en).days < 1
    
    @property
    def tiempo_publicacion(self):
        """Tiempo desde que fue publicado (formato humano)"""
        from django.utils import timezone
        from django.utils.timesince import timesince
        
        return f"Hace {timesince(self.publicado_en)}"
    
    def es_favorito_de(self, estudiante):
        """Verificar si un producto es favorito de un estudiante"""
        if not estudiante:
            return False
        return self.en_favoritos.filter(estudiante=estudiante).exists()
    
    def incrementar_visitas(self):
        self.visitas += 1
        self.save(update_fields=['visitas'])
    
    def puede_editar(self, estudiante):
        """Verificar si un estudiante puede editar este producto"""
        return self.vendedor == estudiante
    
    def puede_eliminar(self, estudiante):
        """Verificar si un estudiante puede eliminar este producto"""
        return self.vendedor == estudiante

class ImagenProducto(models.Model):
    """Múltiples imágenes por producto"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')
    orden = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['orden', 'creado_en']
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Favorito(models.Model):
    """Productos favoritos de los usuarios"""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='en_favoritos')
    agregado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['estudiante', 'producto']
        ordering = ['-agregado_en']
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
    def __str__(self):
        return f"{self.estudiante.apodo} ❤️ {self.producto.nombre}"