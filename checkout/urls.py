# checkout/urls.py
from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("<int:producto_id>/iniciar/", views.iniciar_checkout, name="iniciar"),
    path("exito/", views.checkout_exito, name="checkout_exito"),
    path("cancelado/", views.checkout_cancelado, name="checkout_cancelado"),
]
