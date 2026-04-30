#Implemente una clase “factura” que tenga un importe correspondiente al total
# de la factura pero de acuerdo a la condición impositiva del cliente (IVA
# Responsable, IVA No Inscripto, IVA Exento) genere facturas que indiquen tal
# condición. 
#
# Usamos factory ya que hay distintos tipos de factura y su creacion depende de una condicion
#
"""Implementacion de factura con importes segun su condicion IVA, usando el patron de Factory."""
# 
# Importamos clase ABC y el decorador abstractmethod para crear clases abst
from abc import ABC, abstractmethod

# clase base para la factura.
class Factura(ABC):
    def __init__(self, importe: float):
        self.importe = importe

    @abstractmethod
    def mostrar(self) -> str:
        pass

# clases concretas
class FacturaResponsable(Factura):
    def mostrar(self) -> str:
        return f"Factura IVA Responsable - Total: ${self.importe}"
    
class FacturaNoInscripto(Factura):
    def mostrar(self) -> str:
        return f"Factura IVA No inscripto - Total: ${self.importe}"
    
class FacturaExento(Factura):
    def mostrar(self) -> str:
        return f"Factura Exento - Total: ${self.importe}"
    
# Creamos la clase Factura Factory.
class FacturaFactory:
    @staticmethod
    def crear_factura(tipo: str, importe: float) -> Factura:
        tipo = tipo.strip().lower()

        if tipo == "responsable":
            return FacturaResponsable(importe)
        if tipo == "no_inscripto":
            return FacturaNoInscripto(importe)
        if tipo == "exento":
            return FacturaExento(importe)

        raise ValueError("Tipo de factura no válido")
    
# ejemplo y prueba de uso.
def main():
    tipos = ["responsable", "no_inscripto", "exento"]

    for tipo in tipos:
        factura = FacturaFactory.crear_factura(tipo, 1000)
        print(factura.mostrar())


if __name__ == "__main__":
    main()