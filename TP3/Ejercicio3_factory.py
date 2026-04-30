#Genere una clase donde se instancie una comida rápida “hamburguesa” que pueda ser entregada en mostrador, 
#retirada por el cliente o enviada por delivery.
 
"""Implementación concreta de entrega de comida rápida usando el patrón de diseño Factory."""

#importamos la clase ABC y el decorador abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod 

#creamos la clase abstracta ComidaRapida que define el método entregar, que debe ser implementado por las clases concretas que hereden de ella 
class ComidaRapida(ABC):

    @abstractmethod
    def entregar(self) -> str:
        """Realiza la entrega y devuelve un mensaje descriptivo."""
        pass

class Mostrador(ComidaRapida):
    def entregar(self) -> str:#sobrescribimos el método entregar para mostrar el mensaje correspondiente a este tipo de entrega
        return "La hamburguesa se entrega en mostrador."

class Retirada(ComidaRapida):
    def entregar(self) -> str:
        return "La hamburguesa se retira por el cliente."

class Delivery(ComidaRapida):
    def entregar(self) -> str:
        return "La hamburguesa se envía por delivery."

#Creamos la clase ComidaRapidaFactory que actúa como una fábrica para crear instancias de las clases concretas de entrega de comida rápida
class ComidaRapidaFactory:
    @staticmethod 
    def crear_comida_rapida(tipo: str) -> ComidaRapida:
        tipo_normalizado = tipo.strip().lower()

        #dependiendo del tipo de entrega solicitado, se crea y devuelve una instancia de la clase correspondiente || Si el tipo no es válido, se lanza una excepción ValueError con un mensaje descriptivo
        if tipo_normalizado == "mostrador":
            return Mostrador()
        if tipo_normalizado == "retirada":
            return Retirada()
        if tipo_normalizado == "delivery":
            return Delivery()
        
        raise ValueError(f"Tipo de entrega '{tipo}' no válido. Opciones: mostrador, retirada, delivery.")
    
#Ejemplo de uso
def main() -> None:
    tipos_entrega = ["mostrador", "retirada", "delivery", "Ventanilla"]
    
    for tipo in tipos_entrega:
        try :
            comida = ComidaRapidaFactory.crear_comida_rapida(tipo)
            print(comida.entregar())
        except ValueError as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
