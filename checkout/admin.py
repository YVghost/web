from django.contrib import admin
from .models import Orden

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'comprador',
        'producto',
        'total',
        'metodo_pago',
        'estado',
        'fecha_creacion',
    )
    list_filter = (
        'metodo_pago',
        'estado',
        'fecha_creacion',
    )
    search_fields = (
        'comprador__username',
        'producto__nombre',
        'paypal_payment_id',
    )
    readonly_fields = (
        'fecha_creacion',
        'paypal_payment_id',
    )
    ordering = ('-fecha_creacion',)

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('comprador',)
        }),
        ('Detalle del Pedido', {
            'fields': ('producto', 'total', 'metodo_pago', 'estado')
        }),
        ('Información de PayPal', {
            'fields': ('paypal_payment_id',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',)
        }),
    )
