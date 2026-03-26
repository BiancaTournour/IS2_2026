import sys

def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

if len(sys.argv) < 2:
    rango = input("Ingrese un rango (ej. 4-8): ")
else:
    rango = sys.argv[1]

partes = rango.split("-")
desde = int(partes[0])
hasta = int(partes[1])

for num in range(desde, hasta + 1):
    print("Factorial ", num, "! es ", factorial(num))