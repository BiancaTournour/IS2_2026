#Para un producto láminas de acero de 0.5” de espesor y 1,5 metros de ancho dispone de dos trenes laminadores, uno que genera planchas de 5 mts y otro de 10 mts. 
#Genere una clase que represente a las láminas en forma genérica al cual se le pueda indicar que a que tren laminador se enviará a producir. 
#(Use el patrón bridge en la solución).

from abc import ABC, abstractmethod

# Implementación: trenes laminadores

class TrenLaminador(ABC):
    """Interfaz de implementación para trenes laminadores."""

    @abstractmethod
    def producir(self, largo: float) -> None:
        pass


class TrenLaminador5(TrenLaminador):
    """Tren laminador que produce planchas de 5 metros."""

    def producir(self, largo: float) -> None:
        print(f"Produciendo lámina de {largo} metros en tren laminador de 5 metros.")

class TrenLaminador10(TrenLaminador):
    """Tren laminador que produce planchas de 10 metros."""

    def producir(self, largo: float) -> None:
        print(f"Produciendo lámina de {largo} metros en tren laminador de 10 metros.")

# Abstracción: láminas

class Lamina(ABC):
    """
    Abstracción principal.

    Mantiene una referencia al tren laminador, que es la implementación.
    """

    def __init__(self, tren: TrenLaminador) -> None:
        self.tren = tren

    @abstractmethod
    def producir(self, largo: float) -> None:
        pass

class LaminaAcero(Lamina):
    """Lámina de acero."""

    def producir(self, largo: float) -> None:
        print(f"Preparando para producir lámina de acero de {largo} metros. Espesor: 0.5”, Ancho: 1.5 metros.")
        self.tren.producir(largo)

def main() -> None:
    # Crear trenes laminadores
    tren5 = TrenLaminador5()
    tren10 = TrenLaminador10()

    # Crear láminas de acero con diferentes trenes
    lamina1 = LaminaAcero(tren5)
    lamina2 = LaminaAcero(tren10)

    # Producir láminas
    lamina1.producir(5)  # Producirá una lámina de 5 metros en el tren de 5 metros
    lamina2.producir(10) # Producirá una lámina de 10 metros en el tren de 10 metros

if __name__ == "__main__":
    main()