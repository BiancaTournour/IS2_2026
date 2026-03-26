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
    num = int(input("Ingrese un número: "))
else:
    num = int(sys.argv[1])

print("Factorial ", num, "! es ", factorial(num))

