from django.urls import path
from . import views


urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_estudiante, name="login"),
    path("logout/", views.logout_estudiante, name="logout"),
    path("perfil/<int:banner_id>/", views.perfil, name="perfil"),
]
