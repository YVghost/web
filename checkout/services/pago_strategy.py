from abc import ABC, abstractmethod


class MetodoPago(ABC):
    @abstractmethod
    def pagar(self, monto):
        pass


class PagoTarjeta(MetodoPago):
    def pagar(self, monto):
        return f"Pago con tarjeta aprobado por ${monto}"


class PagoTransferencia(MetodoPago):
    def pagar(self, monto):
        return f"Pago por transferencia aprobado por ${monto}"
