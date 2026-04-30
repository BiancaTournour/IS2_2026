# Dado una clase que implemente el patrón “prototipo” verifique que una clase
# generada a partir de ella permite por su parte obtener también copias de si misma.
# permite original, copia y copia de la copia.

# Implementamos el patrón Prototype mediante el método clone() usando deepcopy. Se verifica que los objetos clonados pueden generar nuevas copias de sí mismos, manteniendo independencia entre instancias.

import copy
from abc import ABC, abstractmethod

# define que toda clase que quiera ser prototipo debe implementar el metodo clone()
class Prototype(ABC):
    """Interfaz que define el método de clonación."""

    @abstractmethod
    def clone(self):
        pass

# clase concreta que implementa prototype
class Documento(Prototype):
    def __init__(self, titulo: str, contenido: str, metadata: dict):
        # atributos del objeto
        self.titulo = titulo
        self.contenido = contenido
        # diccionario
        self.metadata = metadata

    def clone(self):
        # patron prototype
        # deepcopy crea una copia completamente independiente
        # del objeto (incluyendo objetos como metadata)
        return copy.deepcopy(self)

    def __str__(self) -> str:
        return (
            # metodo para mostrar el objeto de forma legible
            f"Documento:\n"
            f"  Título: {self.titulo}\n"
            f"  Contenido: {self.contenido}\n"
            f"  Metadata: {self.metadata}\n"
        )


def main() -> None:
    # Creamos objeto original (prototipo)
    doc_original = Documento(
        titulo="Informe Técnico",
        contenido="Resultados preliminares...",
        metadata={
            "autor": "Valen",
            "version": 1,
            "tags": ["testing"]
        }
    )

    print("=== ORIGINAL ===")
    print(doc_original)

    # Creamos un clon del original
    doc_clonado = doc_original.clone()

    # Creamos un clon del clon
    # Demuestro que un objeto clonado tambien puede clonarse.
    doc_clon2 = doc_clonado.clone()

    # Modificamos solo el segundo clon
    # Si deepcopy funciona bien, estos cambios NO afectan a los otros objetos
    doc_clon2.titulo = "Informe Técnico - Copia 2"
    doc_clon2.metadata["version"] = 3
    doc_clon2.metadata["tags"].append("extra")

    print("=== CLON DEL CLON MODIFICADO ===")
    print(doc_clon2)

    # verifica que el primer clon no cambio
    print("=== CLON ORIGINAL (no debe cambiar) ===")
    print(doc_clonado)

    # verificar que el original tampoco cambio
    print("=== ORIGINAL (no debe cambiar) ===")
    print(doc_original)

    # Verificación de que son objetos distintos en memoria.
    print("IDs:")
    print(id(doc_original))
    print(id(doc_clonado))
    print(id(doc_clon2))


if __name__ == "__main__":
    main()


