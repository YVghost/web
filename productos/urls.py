from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'productos'

urlpatterns = [
    # Públicas
    path('', views.explorar, name='explorar'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='por_categoria'),
    
    # Protegidas - Gestión de productos
    path('vender/', login_required(views.vender), name='vender'),
    path('mis-productos/', login_required(views.mis_productos), name='mis_productos'),
    path('estadisticas/', login_required(views.estadisticas_productos), name='estadisticas'),
    path('ventas/', login_required(views.productos_mas_vendidos), name='ventas'),
    path('marcar-todos-vendidos/', login_required(views.marcar_todos_vendidos), name='marcar_todos_vendidos'),
    
    # Detalles y acciones específicas de producto
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle'),
    path('producto/<int:producto_id>/editar/', login_required(views.editar_producto), name='editar'),
    path('producto/<int:producto_id>/eliminar/', login_required(views.eliminar_producto), name='eliminar'),
    
    # CORREGIDO: Cambiar estado con parámetro en la URL
    path('producto/<int:producto_id>/cambiar-estado/<str:nuevo_estado>/', 
         login_required(views.cambiar_estado_producto), name='cambiar_estado'),
    
    path('producto/<int:producto_id>/activar-desactivar/', 
         login_required(views.activar_desactivar_producto), name='activar_desactivar'),
    path('producto/<int:producto_id>/duplicar/', 
         login_required(views.duplicar_producto), name='duplicar'),
    
    # Favoritos
    path('favoritos/', login_required(views.mis_favoritos), name='mis_favoritos'),
    path('producto/<int:producto_id>/favorito/', 
         login_required(views.toggle_favorito), name='toggle_favorito'),
    
    # Checkout
    path('producto/<int:producto_id>/checkout/', 
         login_required(views.iniciar_checkout), name='iniciar_checkout'),
]