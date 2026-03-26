import matplotlib.pyplot as plt

def collatz_iteraciones(n):
    iteraciones = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        iteraciones += 1
    return iteraciones

numeros = list(range(1, 10001))
iteraciones = [collatz_iteraciones(n) for n in numeros]

plt.figure(figsize=(12, 6))
plt.plot(numeros, iteraciones, linewidth=0.5, color="steelblue")
plt.xlabel("Número de iteraciones hasta converger")
plt.ylabel("Número n de inicio")
plt.title("Conjetura de Collatz - números del 1 al 10000")
plt.tight_layout()
plt.savefig("src/collatz/collatz.png")
plt.show()