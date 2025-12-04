from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import Orden
from .paypal_config import paypalrestsdk


@login_required
def iniciar_checkout(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedor = producto.vendedor  # 🔥 obtener el vendedor del producto

    if request.method == "POST":
        metodo_pago = request.POST.get("metodo_pago")

        # === Opción 1: Pago en efectivo ===
        if metodo_pago == "efectivo":
            orden = Orden.objects.create(
                comprador=request.user,
                producto=producto,
                total=producto.precio,
                metodo_pago="efectivo",
                estado="pagado",
            )

            producto.estado = "reservado"
            producto.save(update_fields=["estado"])

            messages.success(request, "✅ Compra registrada correctamente. Pague al recibir el producto.")
            return redirect("checkout:checkout_exito")

        # === Opción 2: Pago con PayPal ===
        elif metodo_pago == "paypal":
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse("checkout:checkout_exito")),
                    "cancel_url": request.build_absolute_uri(reverse("checkout:checkout_cancelado")),
                },
                "transactions": [{
                    "item_list": {"items": [{
                        "name": producto.nombre,
                        "sku": str(producto.id),
                        "price": str(producto.precio),
                        "currency": "USD",
                        "quantity": 1
                    }]},
                    "amount": {"total": str(producto.precio), "currency": "USD"},
                    "description": f"Compra del producto {producto.nombre}"
                }]
            })

            if payment.create():
                orden = Orden.objects.create(
                    comprador=request.user,
                    producto=producto,
                    total=producto.precio,
                    metodo_pago="paypal",
                    estado="pendiente",
                    paypal_payment_id=payment.id
                )

                for link in payment.links:
                    if link.method == "REDIRECT":
                        return redirect(link.href)
            else:
                print(payment.error)
                messages.error(request, "Error al crear el pago en PayPal.")
                return redirect("productos:detalle", producto_id=producto.id)


    return render(request, "checkout/iniciar.html", {"producto": producto, "vendedor": vendedor})



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
