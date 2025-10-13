from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Orden

@receiver(valid_ipn_received)
def procesar_pago_paypal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            orden = Orden.objects.get(id=int(ipn.invoice))
            orden.estado = 'pagado'
            orden.id_transaccion = ipn.txn_id
            orden.save()

            # Marcar producto como vendido
            producto = orden.producto
            producto.estado = 'vendido'
            producto.save(update_fields=['estado'])
        except Orden.DoesNotExist:
            pass
