#Represente la lista de piezas componentes de un ensamblado con sus relaciones jerárquicas. 
#Empiece con un producto principal formado por tres sub-conjuntos los que a su vez tendrán cuatro piezas cada uno. 
#Genere clases que representen esa configuración y la muestren. 
#Luego agregue un subconjunto opcional adicional también formado por cuatro piezas. (Use el patrón composite).

from abc import ABC, abstractmethod

# clases para representar la estructura jerárquica 
class Componente(ABC):
    """Componente abstracto común para piezas y conjuntos."""

    @abstractmethod
    def mostrar(self, indentacion: int = 0) -> None:
        pass

# Implementación de piezas y conjuntos
class Pieza(Componente):
    """Hoja del Composite."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def mostrar(self, indentacion: int = 0) -> None:
        espacio = " " * indentacion
        print(f"{espacio}- Pieza: {self.nombre}")

class Conjunto(Componente):
    """Composite que puede contener piezas u otros conjuntos."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.componentes: list[Componente] = []

    def agregar(self, componente: Componente) -> None:
        self.componentes.append(componente)

    def remover(self, componente: Componente) -> None:
        self.componentes.remove(componente)

    def mostrar(self, indentacion: int = 0) -> None:
        espacio = " " * indentacion
        print(f"{espacio}+ Conjunto: {self.nombre}")
        for componente in self.componentes:
            componente.mostrar(indentacion + 4)

def main() -> None:
    producto_principal = Conjunto("Producto Principal")

    # Crear sub-conjuntos
    subconjunto1 = Conjunto("Subconjunto 1")
    subconjunto2 = Conjunto("Subconjunto 2")
    subconjunto3 = Conjunto("Subconjunto 3")

    # Agregar piezas a cada subconjunto
    for i in range(1, 5):
        subconjunto1.agregar(Pieza(f"Pieza {i} del Subconjunto 1"))
        subconjunto2.agregar(Pieza(f"Pieza {i} del Subconjunto 2"))
        subconjunto3.agregar(Pieza(f"Pieza {i} del Subconjunto 3"))

    # Agregar subconjuntos al producto principal
    producto_principal.agregar(subconjunto1)
    producto_principal.agregar(subconjunto2)
    producto_principal.agregar(subconjunto3)

    # Mostrar la estructura del producto principal
    print("Estructura del Producto Principal:")
    producto_principal.mostrar()

    # Agregar un subconjunto opcional adicional
    subconjunto_opcional = Conjunto("Subconjunto Opcional")
    for i in range(1, 5):
        subconjunto_opcional.agregar(Pieza(f"Pieza {i} del Subconjunto Opcional"))

    producto_principal.agregar(subconjunto_opcional)

    # Mostrar la estructura actualizada del producto principal
    print("\nEstructura Actualizada del Producto Principal con Subconjunto Opcional:")
    producto_principal.mostrar()

if __name__ == "__main__":
    main()