
from checkout.repositories.orden_repository import OrdenRepository
from checkout.services.pago_strategy import PagoTarjeta, PagoTransferencia


class CheckoutService:

    def __init__(self):
        self.repository = OrdenRepository()
        self.strategies = {
            'tarjeta': PagoTarjeta(),
            'transferencia': PagoTransferencia(),
        }

    def procesar_checkout(self, usuario, total, metodo_pago):
        orden = self.repository.crear_orden(usuario, total)

        estrategia = self.strategies.get(metodo_pago)
        if not estrategia:
            raise ValueError("Método de pago no soportado")

        resultado_pago = estrategia.pagar(total)
        self.repository.confirmar_pago(orden)

        return {
            'orden': orden,
            'mensaje': resultado_pago
        }
