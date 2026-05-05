# Implementación del patrón Flyweight
# Permite compartir objetos iguales para ahorrar memoria.
# En este caso, se reutilizan letras en lugar de crear una por cada aparición.
# Letras compartidas. pd: si la letra ya existe, no la creo de nuevo, la reutilizo.

# # Esta clase se comparte entre múltiples usos del mismo carácter
class Letra:
    """Flyweight: estado compartido"""
    def __init__(self, caracter):
        self.caracter = caracter

    # posicion es estado externo (no se guarda en la clase)
    def mostrar(self, posicion):
        print(f"Letra '{self.caracter}' en posición {posicion}")

"""Factory que reutiliza instancias de letras en lugar de crear nuevas"""
class FabricaLetras:
    def __init__(self):
        self._letras = {}

    def obtener_letra(self, caracter):
        # Si no existe, se crea
        if caracter not in self._letras:
            print(f"Creando letra: {caracter}")
            self._letras[caracter] = Letra(caracter)
            # Si ya existe, se reutiliza
        else:
            print(f"Reutilizando letra: {caracter}")

        return self._letras[caracter]


def main():
    fabrica = FabricaLetras()

    # Texto con letras repetidas
    texto = "ABBA"

    # Se solicita cada letra a la fábrica
    # Algunas se crean, otras se reutilizan
    letras_usadas = []

    # creamos letras (algunas se repiten)
    for i, c in enumerate(texto):
        letra = fabrica.obtener_letra(c)
        letras_usadas.append((letra, i))

    print("\nMostrando texto:")
    for letra, pos in letras_usadas:
        letra.mostrar(pos)

    # Se muestra cuántos objetos se crearon realmente
    # (deberían ser menos que la cantidad de letras)

    print("\nCantidad de objetos creados:", len(fabrica._letras))


if __name__ == "__main__":
    main()