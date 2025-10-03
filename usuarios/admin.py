from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Estudiante, Calificacion

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = [
        'apodo', 
        'nombre_completo', 
        'correo', 
        'universidad_display', 
        'prestigio_display', 
        'es_vendedor_verificado',
        'fecha_registro',
        'telefono_verificado'
    ]
    
    list_filter = [
        'universidad',
        'es_vendedor_verificado',
        'fecha_registro'
    ]
    
    search_fields = [
        'nombres',
        'apellidos', 
        'apodo',
        'correo',
        'telefono'
    ]
    
    readonly_fields = [
        'prestigio',
        'fecha_registro',
        'promedio_calificaciones_display',
        'total_calificaciones_display',
        'estrellas_display_admin'
    ]
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'nombres', 
                'apellidos', 
                'apodo',
                'correo',
                'telefono',
                'universidad'
            )
        }),
        ('Información de Perfil', {
            'fields': (
                'avatar',
                'bio',
                'es_vendedor_verificado'
            )
        }),
        ('Estadísticas', {
            'fields': (
                'prestigio',
                'promedio_calificaciones_display',
                'total_calificaciones_display',
                'estrellas_display_admin',
                'fecha_registro'
            )
        }),
        ('Usuario Django', {
            'fields': ('user',),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-fecha_registro']
    list_per_page = 20
    
    # Métodos personalizados para display en admin
    def universidad_display(self, obj):
        return obj.get_universidad_display()
    universidad_display.short_description = 'Universidad'
    
    def prestigio_display(self, obj):
        return f"{obj.prestigio}/100"
    prestigio_display.short_description = 'Prestigio'
    
    def telefono_verificado(self, obj):
        if obj.telefono:
            return format_html('<span style="color: green;">✓</span> Sí')
        return format_html('<span style="color: red;">✗</span> No')
    telefono_verificado.short_description = 'Teléfono Verificado'
    
    def promedio_calificaciones_display(self, obj):
        return f"{obj.promedio_calificaciones:.1f}/5.0"
    promedio_calificaciones_display.short_description = 'Promedio Calificaciones'
    
    def total_calificaciones_display(self, obj):
        return obj.total_calificaciones
    total_calificaciones_display.short_description = 'Total Calificaciones'
    
    def estrellas_display_admin(self, obj):
        return obj.estrellas_display
    estrellas_display_admin.short_description = 'Calificación Visual'
    
    # Acciones personalizadas
    actions = ['verificar_vendedores', 'desverificar_vendedores']
    
    def verificar_vendedores(self, request, queryset):
        updated = queryset.update(es_vendedor_verificado=True)
        self.message_user(request, f'{updated} vendedores verificados exitosamente.')
    verificar_vendedores.short_description = "Verificar vendedores seleccionados"
    
    def desverificar_vendedores(self, request, queryset):
        updated = queryset.update(es_vendedor_verificado=False)
        self.message_user(request, f'{updated} vendedores desverificados exitosamente.')
    desverificar_vendedores.short_description = "Desverificar vendedores seleccionados"

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'calificador_display',
        'calificado_display',
        'estrellas_display',
        'producto_display',
        'fecha_calificacion'
    ]
    
    list_filter = [
        'estrellas',
        'fecha_calificacion',
        'calificador__universidad'
    ]
    
    search_fields = [
        'calificador__nombres',
        'calificador__apellidos',
        'calificador__apodo',
        'calificado__nombres', 
        'calificado__apellidos',
        'calificado__apodo',
        'comentario'
    ]
    
    readonly_fields = ['fecha_calificacion']
    
    fieldsets = (
        ('Información de Calificación', {
            'fields': (
                'calificador',
                'calificado',
                'estrellas',
                'comentario',
                'producto'
            )
        }),
        ('Metadatos', {
            'fields': ('fecha_calificacion',),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-fecha_calificacion']
    list_per_page = 20
    
    # Métodos personalizados para display
    def calificador_display(self, obj):
        return f"{obj.calificador.nombre_completo} ({obj.calificador.apodo})"
    calificador_display.short_description = 'Calificador'
    
    def calificado_display(self, obj):
        return f"{obj.calificado.nombre_completo} ({obj.calificado.apodo})"
    calificado_display.short_description = 'Calificado'
    
    def estrellas_display(self, obj):
        stars = '⭐' * obj.estrellas
        return f"{stars} ({obj.estrellas}/5)"
    estrellas_display.short_description = 'Estrellas'
    
    def producto_display(self, obj):
        if obj.producto:
            return obj.producto.nombre
        return "Sin producto"
    producto_display.short_description = 'Producto'
    
    # Filtro personalizado para evitar auto-calificaciones
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "calificador":
            kwargs["queryset"] = Estudiante.objects.all().order_by('apodo')
        elif db_field.name == "calificado":
            kwargs["queryset"] = Estudiante.objects.all().order_by('apodo')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Si quieres también personalizar el User admin para mostrar información del estudiante
from django.contrib.auth.models import User

class EstudianteInline(admin.StackedInline):
    model = Estudiante
    can_delete = False
    verbose_name_plural = 'Información de Estudiante'
    fields = ['nombres', 'apellidos', 'apodo', 'correo', 'universidad', 'es_vendedor_verificado']
    readonly_fields = ['nombres', 'apellidos', 'apodo', 'correo', 'universidad']

class CustomUserAdmin(UserAdmin):
    inlines = (EstudianteInline,)
    list_display = UserAdmin.list_display + ('estudiante_info',)
    
    def estudiante_info(self, obj):
        try:
            estudiante = obj.estudiante
            return f"{estudiante.apodo} - {estudiante.get_universidad_display()}"
        except Estudiante.DoesNotExist:
            return "Sin perfil de estudiante"
    estudiante_info.short_description = 'Información Estudiante'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)