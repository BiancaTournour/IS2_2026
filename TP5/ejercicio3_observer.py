# Implemente una clase bajo el patrón observer donde una serie de clases están subscriptas, cada clase espera que su propio ID (una secuencia arbitraria de 4 caracteres) 
# sea expuesta y emitirá un mensaje cuando el ID emitido y el propio coinciden. Implemente 4 clases de tal manera que cada una tenga un ID especifico. 
# Emita 8 ID asegurándose que al menos cuatro de ellos coincidan con ID para el que tenga una clase implementada.

"""
Observer permite que múltiples objetos estén suscriptos
a un emisor de eventos

En este ejercicio:
- varias clases observadoras esperan un ID específico,
- el sistema emite IDs,
- cada observador reacciona únicamente cuando el ID coincide
  con el suyo.
"""

from abc import ABC, abstractmethod


class Observador(ABC):
    """Interfaz común para los observadores."""

    @abstractmethod
    def actualizar(self, codigo: str) -> None:
        pass


class EmisorIDs:
    """
    Sujeto observado.

    Mantiene una lista de observadores y les informa
    cada vez que se emite un ID.
    """

    def __init__(self) -> None:
        self._observadores: list[Observador] = []

    def agregar_observador(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def remover_observador(self, observador: Observador) -> None:
        self._observadores.remove(observador)

    def emitir_id(self, codigo: str) -> None:
        print(f"\n[EMISOR] ID emitido: {codigo}")
        self._notificar(codigo)

    def _notificar(self, codigo: str) -> None:
        for observador in self._observadores:
            observador.actualizar(codigo)


class ObservadorID(Observador):
    """
    Observador concreto.

    Cada instancia espera un ID específico.
    """

    def __init__(self, nombre: str, id_esperado: str) -> None:
        self.nombre = nombre
        self.id_esperado = id_esperado

    def actualizar(self, codigo: str) -> None:
        if codigo == self.id_esperado:
            print(
                f"[{self.nombre}] Coincidencia detectada "
                f"con ID: {codigo}"
            )


def main() -> None:

    # Sujeto observado
    emisor = EmisorIDs()

    # Observadores con IDs específicos
    obs1 = ObservadorID("ClaseA", "A123")
    obs2 = ObservadorID("ClaseB", "B456")
    obs3 = ObservadorID("ClaseC", "C789")
    obs4 = ObservadorID("ClaseD", "D000")

    # Suscripción de observadores
    emisor.agregar_observador(obs1)
    emisor.agregar_observador(obs2)
    emisor.agregar_observador(obs3)
    emisor.agregar_observador(obs4)

    # Emisión de 8 IDs
    ids = [
        "A123",
        "XXXX",
        "B456",
        "ZZZZ",
        "C789",
        "YYYY",
        "D000",
        "TTTT"
    ]

    for codigo in ids:
        emisor.emitir_id(codigo)


if __name__ == "__main__":
    main()