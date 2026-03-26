import sys

class Factorial:
    def __init__(self):
        pass

    def calcular(self, num):
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, min, max):
        for num in range(min, max + 1):
            print("Factorial ", num, "! es ", self.calcular(num))


if len(sys.argv) < 2:
    rango = input("Ingrese un rango (ej. 4-8, -10, 4-): ")
else:
    rango = sys.argv[1]

partes = rango.split("-")

if partes[0] == "":
    desde = 1
    hasta = int(partes[1])
elif partes[1] == "":
    desde = int(partes[0])
    hasta = 60
else:
    desde = int(partes[0])
    hasta = int(partes[1])

f = Factorial()
f.run(desde, hasta)