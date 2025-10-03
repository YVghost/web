from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto, Favorito

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'orden']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'activa', 'cantidad_productos']
    list_filter = ['activa']
    search_fields = ['nombre']
    list_editable = ['activa']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio_formateado', 'estado', 'vendedor', 'publicado_en']
    list_filter = ['estado', 'categoria', 'condicion', 'tipo_envio']
    search_fields = ['nombre', 'descripcion', 'tags']
    readonly_fields = ['publicado_en', 'actualizado_en', 'visitas']
    inlines = [ImagenProductoInline]
    
    def precio_formateado(self, obj):
        return obj.precio_formateado
    precio_formateado.short_description = 'Precio'

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'producto', 'agregado_en']
    list_filter = ['agregado_en']
    search_fields = ['estudiante__user__username', 'producto__nombre']
    readonly_fields = ['agregado_en']

admin.site.register(ImagenProducto) 