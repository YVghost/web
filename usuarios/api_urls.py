from django.urls import path
from .api_views import LoginAPIView, RegistroAPIView, PerfilAPIView

app_name = "usuarios"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("registro/", RegistroAPIView.as_view(), name="registro"),
    path("perfil/", PerfilAPIView.as_view(), name="perfil"),
]
