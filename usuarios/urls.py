from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación básica
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_estudiante, name="login"),
    path("logout/", views.logout_estudiante, name="logout"),
    
    # Perfiles
    path("perfil/", views.perfil, name="perfil"), 
    path("perfil/<int:id>/", views.perfil, name="perfil_con_id"),
    
    # Calificaciones
    path('calificar/<int:vendedor_id>/', views.calificar_vendedor, name='calificar_vendedor'),
    path('calificaciones/<int:estudiante_id>/', views.ver_calificaciones, name='ver_calificaciones'),
    
]