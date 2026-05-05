# Implementación del patrón Decorator mediante composición de objetos
# que permite agregar funcionalidades (operaciones) dinámicamente.

# Clase que permete a un numero cualquiera imprimir su valor.
# Sumarle 2, multiplicarle por 2, dividirlo por 3.
# Muestra los resultados de la clase sin agregardos y con la invocacion anidada a las clases con las dif operaciones.

from abc import ABC, abstractmethod


# Componente base
class Numero(ABC):
    @abstractmethod
    def operar(self):
        pass


# Implementación concreta
class NumeroBase(Numero):
    def __init__(self, valor):
        self.valor = valor

    def operar(self):
        return self.valor


# Decorator base
class OperacionDecorator(Numero):
    def __init__(self, numero: Numero):
        self._numero = numero

    def operar(self):
        return self._numero.operar()


# Decorators concretos

class SumarDos(OperacionDecorator):
    def operar(self):
        return self._numero.operar() + 2


class MultiplicarDos(OperacionDecorator):
    def operar(self):
        return self._numero.operar() * 2


class DividirTres(OperacionDecorator):
    def operar(self):
        return self._numero.operar() / 3


# prueba
def main():
    numero = NumeroBase(6)

    print("Sin decoradores:", numero.operar())

    # 🔥 decoradores anidados (como en el ejemplo del profe)
    numero_modificado = DividirTres(
        MultiplicarDos(
            SumarDos(numero)
        )
    )

    print("Con decoradores:", numero_modificado.operar())


if __name__ == "__main__":
    main()