#Cree una clase bajo el patrón cadena de responsabilidad donde los números del 1 al 100 sean pasados a las clases subscriptas en secuencia, 
#aquella que identifique la necesidad de consumir el número lo hará y caso contrario lo pasará al siguiente en la cadena. 
#Implemente una clase que consuma números primos y otra números pares. 
#Puede ocurrir que un número no sea consumido por ninguna clase en cuyo caso se marcará como no consumido.

from abc import ABC, abstractmethod

#clase handler abstracta, permite establecer el siguiente handler y define el método handle que debe ser implementado por las clases concretas
class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, number):
        pass

#clase concreta para manejar números primos, verifica si el número es primo y lo consume, de lo contrario pasa al siguiente handler
class PrimeHandler(Handler):
    def handle(self, number):
        if self.is_prime(number):
            print(f"{number} es un número primo.")
        elif self._next_handler:
            self._next_handler.handle(number)
        else:
            print(f"{number} no fue consumido por ninguna clase.")

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

#clase concreta para manejar números pares, verifica si el número es par y lo consume, de lo contrario pasa al siguiente handler   
class EvenHandler(Handler):
    def handle(self, number):
        if number % 2 == 0:
            print(f"{number} es un número par.")
        elif self._next_handler:
            self._next_handler.handle(number)
        else:
            print(f"{number} no fue consumido por ninguna clase.")

#clase concreta para manejar números que no son consumidos por ninguna clase, simplemente imprime un mensaje indicando que el número no fue consumido
class NotConsumedHandler(Handler):
    def handle(self, number):
        print(f"{number} no fue consumido por ninguna clase.")

# Configuración de la cadena de responsabilidad
prime_handler = PrimeHandler()
even_handler = EvenHandler()
not_consumed_handler = NotConsumedHandler()

# Establecer la cadena: prime_handler -> even_handler -> not_consumed_handler
prime_handler.set_next(even_handler)
even_handler.set_next(not_consumed_handler)

# Prueba con números del 1 al 100
for num in range(1, 101):
    prime_handler.handle(num)
