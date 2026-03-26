import sys

#funcion de factorial
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
    rango = input("Ingrese un rango (ej. 4-8, -10, 4-): ")
else:
    rango = sys.argv[1]

partes = rango.split("-")

if partes[0] == "":
    # Caso "-hasta": desde 1 hasta el número indicado
    desde = 1
    hasta = int(partes[1])
elif partes[1] == "":
    # Caso "desde-": desde el número indicado hasta 60
    desde = int(partes[0])
    hasta = 60
else:
    # Caso normal "desde-hasta"
    desde = int(partes[0])
    hasta = int(partes[1])

for num in range(desde, hasta + 1):
    print("Factorial ", num, "! es ", factorial(num))