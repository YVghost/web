from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.explorar, name='explorar'),
    path('vender/', login_required(views.vender), name='vender'),
    path('mis-productos/', login_required(views.mis_productos), name='mis_productos'),
    path('favoritos/', login_required(views.mis_favoritos), name='mis_favoritos'),
    path('<int:producto_id>/', login_required(views.detalle_producto), name='detalle'), 
    path('<int:producto_id>/favorito/', login_required(views.toggle_favorito), name='toggle_favorito'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='por_categoria'),
    path('<int:producto_id>/editar/', login_required(views.editar_producto), name='editar'),
    path('<int:producto_id>/eliminar/', login_required(views.eliminar_producto), name='eliminar'),
    path('<int:producto_id>/cambiar-estado/', login_required(views.cambiar_estado_producto), name='cambiar_estado'),
]
