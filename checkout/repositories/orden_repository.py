from checkout.models import Orden

class OrdenRepository:

    def crear_orden(self, usuario, total):
        return Orden.objects.create(
            usuario=usuario,
            total=total,
            estado='pendiente'
        )

    def confirmar_pago(self, orden):
        orden.estado = 'pagado'
        orden.save()
