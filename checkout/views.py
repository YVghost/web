from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import Orden
from .paypal_config import paypalrestsdk
from django.shortcuts import render, get_object_or_404
from productos.models import Producto
from checkout.services.checkout_service import CheckoutService


@login_required
def iniciar_checkout(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    metodo = request.GET.get("metodo", "tarjeta")  # tarjeta o transferencia

    checkout = CheckoutService()
    resultado = checkout.procesar_pago(producto.precio, metodo)

    return render(request, "checkout/resumen.html", {
        "producto": producto,
        "resultado": resultado
    })

@csrf_exempt
def checkout_exito(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if payment_id and payer_id:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            try:
                orden = Orden.objects.get(paypal_payment_id=payment_id)
                orden.estado = "pagado"
                orden.save()

                # 🔥 Marcar el producto como vendido
                producto = orden.producto
                producto.estado = "vendido"
                producto.save(update_fields=["estado"])

                messages.success(request, "✅ Pago completado correctamente. El producto fue marcado como vendido.")
            except Orden.DoesNotExist:
                messages.error(request, "No se encontró la orden del pago.")
        else:
            messages.error(request, "Error al procesar el pago en PayPal.")
    else:
        messages.success(request, "✅ Compra completada con éxito (pago en efectivo).")

    return render(request, "checkout/exito.html")


def checkout_cancelado(request):
    payment_id = request.GET.get("paymentId")
    if payment_id:
        try:
            orden = Orden.objects.get(paypal_payment_id=payment_id)
            orden.estado = "cancelado"
            orden.save()
        except Orden.DoesNotExist:
            pass

    messages.warning(request, "❌ Pago cancelado.")
    return render(request, "checkout/cancelado.html")
