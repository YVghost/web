from django.urls import path
from . import views


urlpatterns = [
    path('explorar/', views.explorar, name='explorar'),
    path('vender/', views.vender, name='vender'),
    path('perfil/', views.perfil, name='perfil'),
    
]
