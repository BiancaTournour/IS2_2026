#Elabore una clase para el cálculo del valor de impuestos a ser utilizado por
#todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado
#deberá recibir un valor de importe base imponible y deberá retornar la suma
#del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre
#esa base imponible.

#En este caso, se implementa el patrón Singleton para garantizar que solo exista una instancia de la clase Calculadora
class Calculadora:
    _instancia = None
   
   # Definición de las tasas de impuestos como constantes de clase
    IVA = 0.21
    IIBB = 0.05
    CONTRIBUCIONES = 0.012

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Calculadora, cls).__new__(cls)
        return cls._instancia
    
    def calcular_total(self, base_inponible):#método para calcular el total de impuestos a pagar dado una base imponible
        iva = base_inponible * self.IVA
        iibb = base_inponible * self.IIBB
        constribuciones = base_inponible * self.CONTRIBUCIONES

        return iva + iibb + constribuciones

calc1 = Calculadora()


base = float(input("Ingrese la base imponible: "))  # True, ambas variables apuntan a la misma instancia

resultado = calc1.calcular_total(base)
print(f"El total a pagar es: {resultado}")
