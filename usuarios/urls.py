from django.urls import path
from . import views

# IMPORTANTE: importar las urls de la API
from .api_views import (
    RegistroAPIView,
    LoginAPIView,
    PerfilAPIView
)

app_name = 'usuarios'

urlpatterns = [

    # ============================
    # 🌐 VISTAS HTML (WEB NORMAL)
    # ============================

    # Autenticación básica
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_estudiante, name="login"),
    path("logout/", views.logout_estudiante, name="logout"),

    # Perfiles
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/<int:id>/", views.perfil, name="perfil_con_id"),

    # Calificaciones
    path("calificar/<int:vendedor_id>/", views.calificar_vendedor, name="calificar_vendedor"),
    path("calificaciones/<int:estudiante_id>/", views.ver_calificaciones, name="ver_calificaciones"),


    # ============================
    # 🔌 API REST (DJANGO REST)
    # ============================

    path("api/register/", RegistroAPIView.as_view(), name="api_register"),
    path("api/login/", LoginAPIView.as_view(), name="api_login"),
    path("api/profile/", PerfilAPIView.as_view(), name="api_profile"),
]
