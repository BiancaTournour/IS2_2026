# IS2_2026
 
## Descripcion del repositorio
 
Repositorio de trabajos prácticos para Ingenieria de Software II - 2026
 
---
 
## Contenido actual
 
### TP1 - Gestión de la configuración y programación Python
 
#### primes.py
Verifica si un número es primo. Se ejecuta desde la línea de comandos.
 
#### factorial.py
Calcula el factorial de un número o rango. Acepta:
- Rango completo: `4-8`
- Sin límite inferior: `-10` (calcula desde 1 hasta el número indicado)
- Sin límite superior: `4-` (calcula desde el número indicado hasta 60)
 
#### factorial_OOP.py
Misma funcionalidad que factorial.py pero implementada con programación orientada a objetos, usando la clase `Factorial` con el método `run(min, max)`.
 
#### collatz.py
Calcula la conjetura de Collatz para los números del 1 al 10000 y genera un gráfico con las iteraciones necesarias hasta converger.
 
#### Tecnologías utilizadas
 
- Python 3
- Git y GitHub para control de versiones
 
---
 
### TP2 - Calidad de software y herramientas de análisis
 
#### rpn.py
Calculadora en notación polaca inversa (RPN). Se ejecuta desde la línea de comandos pasando la expresión como argumento o en modo interactivo.
 
```bash
python rpn.py 3 4 +                  # → 7
python rpn.py 5 1 2 + 4 * + 3 -     # → 14
python rpn.py                         # modo interactivo
```
 
Soporta:
- Operadores: `+ - * /`
- Constantes: `p` (π), `e` (Euler), `j` (φ número áureo)
- Funciones matemáticas: `sqrt log ln ex 10x yx 1/x chs`
- Trigonometría en grados: `sin cos tg asin acos atg`
- Comandos de pila: `dup swap drop clear`
- Memoria (10 registros): `STO <n> RCL <n>` (n = 0..9)
- Notación científica: `1e10`, `2.5e-3`
- Ayuda: `help`
 
#### test_rpn.py
Suite de 70 tests unitarios para `rpn.py` usando `unittest`. Cubre el 98% del código con condiciones de error verificadas mediante `try/except` explícito.
 
```bash
python -m coverage run --source=rpn -m unittest test_rpn -v
python -m coverage report -m
python -m coverage html   # genera reporte visual en htmlcov/
```
 
#### pyproject.toml
Archivo de configuración para las herramientas de calidad de código:
- `black`: formateador automático (línea máxima 88 caracteres, target Python 3.11)
- `ruff`: linter con reglas E (PEP8), F (pyflakes), I (isort), B (bugbear) y UP (modernización de sintaxis)
 
#### Tecnologías utilizadas
 
- Python 3.11
- `unittest` y `coverage` para testing
- `pylint` para análisis estático (puntaje: 10.00/10)
- `black` para formateo de código
- `ruff` para linting
- `multimetric` para métricas de Halstead y McCabe
- Git y GitHub para control de versiones
 
---
 
## Cómo ejecutar el proyecto
 
1. Clonar el repositorio
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install coverage pylint black ruff multimetric
   ```
4. Navegar a la carpeta del TP a ejecutar y correr el archivo correspondiente
 
---
 
## Propiedad del repositorio
 
- Bianca Micaela Tournour
 
---
 
## Referencias
 
- [Documentación oficial de Python](https://docs.python.org/3/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Pylint](https://pylint.readthedocs.io/)
- [Black](https://black.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
 
---
![Logo de la institución](img/UADER-logo.png)