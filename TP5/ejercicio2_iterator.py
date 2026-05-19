#Implemente una clase bajo el patrón iterator que almacena una cadena de caracteres y permite recorrerla en sentido directo y reverso.

from dataclasses import dataclass
from typing import Iterator

@dataclass
#cadena es una clase que representa una cadena de caracteres y tiene dos métodos para recorrerla en sentido directo y reverso
class Cadena:
    """Representa una cadena de caracteres."""
    texto: str

    def iterador_directo(self) -> Iterator[str]:
        """Iterator para recorrer la cadena en sentido directo."""
        for caracter in self.texto:
            yield caracter

    def iterador_reverso(self) -> Iterator[str]:
        """Iterator para recorrer la cadena en sentido reverso."""
        for caracter in reversed(self.texto):
            yield caracter

def main() -> None:
    cadena = Cadena("Hola Mundo")

    print("Recorrido directo:")
    for caracter in cadena.iterador_directo():
        print(caracter)

    print("\nRecorrido reverso:")
    for caracter in cadena.iterador_reverso():
        print(caracter)

if __name__ == "__main__":
    main()