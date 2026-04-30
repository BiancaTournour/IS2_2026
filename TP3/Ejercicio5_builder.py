#Extienda el ejemplo visto en el taller en clase de forma que se pueda utilizar
#para construir aviones en lugar de vehículos. Para simplificar suponga que un
#avión tiene un “body”, 2 turbinas, 2 alas y un tren de aterrizaje.

"""Implementación concreta de construcción de aviones usando el patrón de diseño Builder."""

from __future__ import annotations
from abc import ABC, abstractmethod

# Producto complejo que se construye paso a paso
class avion:
     def __init__(self) -> None:
          self.partes = []

     def agregar(self, parte: str) -> None:
          self.partes.append(parte)

     def mostrar(self) -> str:
          return "Avión con:\n  - " + "\n  - ".join(self.partes)

# Interfaz abstracta del Builder    
class BuilderAvion(ABC):
     
     def __init__(self):
          self.reset()
     
     def reset(self) -> None:
          self._producto = avion()

     def obtener_resultado(self) -> avion:
            producto = self._producto
            self.reset()
            return producto
     
     @abstractmethod
     def construir_body(self) -> None:
          pass
     
     @abstractmethod
     def construir_turbinas(self) -> None:
          pass
     
     @abstractmethod
     def construir_alas(self) -> None:
          pass
     
     @abstractmethod
     def construir_tren_aterrizaje(self) -> None:
          pass
     
# Builders concretos para diferentes tipos de aviones         
class BuilderAvionComercial(BuilderAvion):
        def construir_body(self) -> None:
            self._producto.agregar("Body de avión comercial")
    
        def construir_turbinas(self) -> None:
            self._producto.agregar("2 turbinas de avión comercial")
    
        def construir_alas(self) -> None:
            self._producto.agregar("2 alas de avión comercial")
    
        def construir_tren_aterrizaje(self) -> None:
            self._producto.agregar("Tren de aterrizaje de avión comercial")

class BuilderAvionPrivado(BuilderAvion):
        def construir_body(self) -> None:
            self._producto.agregar("Body de avión privado")
    
        def construir_turbinas(self) -> None:
            self._producto.agregar("2 turbinas de avión privado")
    
        def construir_alas(self) -> None:
            self._producto.agregar("2 alas de avión privado")
    
        def construir_tren_aterrizaje(self) -> None:
            self._producto.agregar("Tren de aterrizaje de avión privado")

# Director que define el orden de construcción de los aviones
class Director:
        def __init__(self, builder: BuilderAvion) -> None:
            self._builder = builder
    
        def construir_avion_comercial(self) -> None:
            self._builder.construir_body()
            self._builder.construir_turbinas()
            self._builder.construir_alas()
            self._builder.construir_tren_aterrizaje()

        def construir_avion_privado(self) -> None:
            self._builder.construir_body()
            self._builder.construir_turbinas()
            self._builder.construir_alas()
            self._builder.construir_tren_aterrizaje()

# Función principal para demostrar la construcción de aviones usando el patrón Builder
def main() -> None:
    # Construcción de un avión comercial
    builder_comercial = BuilderAvionComercial() # Crear un builder concreto para avión comercial
    director = Director(builder_comercial) # Crear un director con el builder comercial
    director.construir_avion_comercial() # Construir el avión comercial usando el director
    avion_comercial = builder_comercial.obtener_resultado() # Obtener el producto finalizado a través del builder
    print(avion_comercial.mostrar())

    # Construcción de un avión privado
    builder_privado = BuilderAvionPrivado()
    director = Director(builder_privado)
    director.construir_avion_privado()
    avion_privado = builder_privado.obtener_resultado()
    print(avion_privado.mostrar())

if __name__ == "__main__":
    main()