"""RPN (Reverse Polish Notation) Calculator."""

# PYLINT C0410: 'multiple-imports' — se separaron en dos líneas
# (antes: import math, sys)
import math
import sys


# PYLINT C0115: 'missing-class-docstring' — se agregó docstring a la clase
# PYLINT C0321: 'multiple-statements' — se separó 'pass' en línea propia
class RPNError(Exception):
    """Excepción personalizada para errores de la calculadora RPN."""


CONSTANTS = {"p": math.pi, "e": math.e, "j": (1 + math.sqrt(5)) / 2}
memory = [0.0] * 10

# Mejora 3: texto de ayuda listando todos los comandos disponibles
HELP_TEXT = """
Operadores : + - * /
Constantes : p (pi)  e (Euler)  j (phi)
Funciones  : sqrt  log  ln  ex  10x  yx  1/x  chs
Trig (grad): sin  cos  tg  asin  acos  atg
Pila       : dup  swap  drop  clear
Memoria    : STO <n>  RCL <n>   (n = 0..9)
Especial   : help
Notacion   : enteros, decimales y cientifica (ej: 1e10, 2.5e-3)
"""


# PYLINT C0116: 'missing-function-docstring' — se agregó docstring a todas las funciones
# PYLINT C0321: 'multiple-statements' — cada sentencia en su propia línea
def to_num(token):
    """Intenta convertir un token a int, float o notacion cientifica.

    Mejora 4: soporte explicito de notacion cientifica (1e10, 2.5e-3).
    Retorna None si el token no es un numero valido.
    """
    try:
        return int(token)
    except ValueError:
        try:
            # float() ya maneja notacion cientifica nativamente en Python
            return float(token)
        except ValueError:
            return None


def pop1(stack):
    """Extrae y retorna el tope de la pila. Lanza RPNError si está vacía."""
    # PYLINT C0321: antes era 'if len(stack) < 1: raise RPNError(...)' en una línea
    if len(stack) < 1:
        raise RPNError("Stack underflow: need at least 1 value")
    return stack.pop()


def pop2(stack):
    """Extrae y retorna los dos valores del tope de la pila."""
    # PYLINT C0321: antes era 'if len(stack) < 2: raise RPNError(...)' en una línea
    if len(stack) < 2:
        raise RPNError("Stack underflow: need at least 2 values")
    b, a = stack.pop(), stack.pop()
    return a, b


# PYLINT C0321: antes era 'def deg(x): return math.radians(x)' en una línea
def deg(x):
    """Convierte grados a radianes."""
    return math.radians(x)


def adeg(x):
    """Convierte radianes a grados."""
    return math.degrees(x)


# PYLINT R0912/R0915: 'too-many-branches' y 'too-many-statements' en evaluate() —
# se extrajeron cuatro funciones auxiliares para distribuir la lógica
def _handle_stack_cmd(tl, stack):
    """Ejecuta comandos de manipulación de pila: dup, swap, drop, clear."""
    if tl == "dup":
        x = pop1(stack)
        stack.extend([x, x])
    elif tl == "swap":
        a, b = pop2(stack)
        stack.extend([b, a])
    elif tl == "drop":
        pop1(stack)
    elif tl == "clear":
        stack.clear()


def _handle_memory(tl, stack):
    """Ejecuta comandos de memoria: sto, rcl."""
    if tl == "sto":
        addr = pop1(stack)
        val = pop1(stack)
        # PYLINT C0325: 'superfluous-parens' — se quitaron paréntesis innecesarios
        # antes: not (0 <= addr <= 9)   ahora: not 0 <= addr <= 9
        if not isinstance(addr, int) or not 0 <= addr <= 9:
            raise RPNError(f"STO: address must be 0-9, got {addr}")
        memory[addr] = val
    elif tl == "rcl":
        addr = pop1(stack)
        # PYLINT C0325: ídem corrección anterior
        if not isinstance(addr, int) or not 0 <= addr <= 9:
            raise RPNError(f"RCL: address must be 0-9, got {addr}")
        stack.append(memory[addr])


def _handle_arithmetic(tl, stack):
    """Ejecuta operaciones aritméticas básicas: +, -, *, /."""
    if tl == "+":
        # PYLINT C0321: antes era 'a, b = pop2(stack); stack.append(a + b)' en una línea
        a, b = pop2(stack)
        stack.append(a + b)
    elif tl == "-":
        a, b = pop2(stack)
        stack.append(a - b)
    elif tl == "*":
        a, b = pop2(stack)
        stack.append(a * b)
    elif tl == "/":
        a, b = pop2(stack)
        # PYLINT C0321: antes era 'if b == 0: raise RPNError(...)' en una línea
        if b == 0:
            raise RPNError("Division by zero")
        stack.append(a / b)


def _apply_power(a, b, stack):
    """Mejora 3: calcula a**b validando base negativa con exponente fraccionario."""
    if a < 0 and not isinstance(b, int) and b != int(b):
        raise RPNError("yx: base negativa con exponente fraccionario")
    stack.append(a**b)


def _handle_math_fn(tl, stack):
    """Ejecuta funciones matematicas: sqrt, log, ln, ex, 10x, yx, 1/x, chs."""
    if tl == "sqrt":
        x = pop1(stack)
        # PYLINT C0321: antes era 'if x < 0: raise RPNError(...)' en una línea
        if x < 0:
            raise RPNError("sqrt of negative number")
        stack.append(math.sqrt(x))
    elif tl == "log":
        x = pop1(stack)
        if x <= 0:
            raise RPNError("log of non-positive number")
        stack.append(math.log10(x))
    elif tl == "ln":
        x = pop1(stack)
        if x <= 0:
            raise RPNError("ln of non-positive number")
        stack.append(math.log(x))
    elif tl == "ex":
        stack.append(math.exp(pop1(stack)))
    elif tl == "10x":
        stack.append(10 ** pop1(stack))
    elif tl == "yx":
        # PYLINT C0321: antes era 'a, b = pop2(stack); stack.append(a ** b)'
        # en una línea
        a, b = pop2(stack)
        _apply_power(a, b, stack)
    elif tl == "1/x":
        x = pop1(stack)
        if x == 0:
            raise RPNError("1/x: division by zero")
        stack.append(1 / x)
    elif tl == "chs":
        stack.append(-pop1(stack))


def _handle_trig(tl, stack):
    """Ejecuta funciones trigonometricas en grados: sin, cos, tg, asin, acos, atg."""
    # PYLINT C0321: antes cada rama era 'elif tl == X: stack.append(...)' en una línea
    if tl == "sin":
        stack.append(math.sin(deg(pop1(stack))))
    elif tl == "cos":
        stack.append(math.cos(deg(pop1(stack))))
    elif tl == "tg":
        stack.append(math.tan(deg(pop1(stack))))
    elif tl == "asin":
        stack.append(adeg(math.asin(pop1(stack))))
    elif tl == "acos":
        stack.append(adeg(math.acos(pop1(stack))))
    elif tl == "atg":
        stack.append(adeg(math.atan(pop1(stack))))


# PYLINT R0912/R0915: tabla de despacho por categoría — reduce branches en evaluate()
_STACK_CMDS = {"dup", "swap", "drop", "clear"}
_MEMORY_CMDS = {"sto", "rcl"}
_ARITH_OPS = {"+", "-", "*", "/"}
_MATH_FNS = {"sqrt", "log", "ln", "ex", "10x", "yx", "1/x", "chs"}
_TRIG_FNS = {"sin", "cos", "tg", "asin", "acos", "atg"}


def evaluate(expr: str) -> float:
    """Evalúa una expresión RPN y retorna el resultado numérico."""
    stack = []
    tokens = expr.split()

    for token in tokens:
        tl = token.lower()

        # Mejora 5: comando help imprime ayuda y no modifica la pila
        if tl == "help":
            print(HELP_TEXT)
            continue

        # Despacho por categoría — reemplaza la cadena de 36 elif originales
        # PYLINT R0912/R0915: complejidad reducida extrayendo funciones auxiliares
        if tl in CONSTANTS:
            stack.append(CONSTANTS[tl])
        elif tl in _STACK_CMDS:
            _handle_stack_cmd(tl, stack)
        elif tl in _MEMORY_CMDS:
            _handle_memory(tl, stack)
        elif tl in _ARITH_OPS:
            _handle_arithmetic(tl, stack)
        elif tl in _MATH_FNS:
            _handle_math_fn(tl, stack)
        elif tl in _TRIG_FNS:
            _handle_trig(tl, stack)
        else:
            n = to_num(token)
            if n is not None:
                stack.append(n)
            else:
                raise RPNError(f"Unknown token: '{token}'")

    if len(stack) != 1:
        raise RPNError(f"Expected 1 value on stack, got {len(stack)}: {stack}")
    return stack[0]


def fmt(x):
    """Formatea el resultado: entero si no tiene decimales, float si los tiene."""
    return int(x) if isinstance(x, float) and x.is_integer() else x


def main():
    """Punto de entrada: acepta expresión por argumento CLI o por stdin."""
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        print("RPN Calculator. Enter expression (or Ctrl+D to quit):")
        try:
            expr = input("> ")
        except EOFError:
            return
    try:
        result = evaluate(expr)
        print(fmt(result))
    except RPNError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


# PYLINT C0304: 'missing-final-newline' — archivo termina con newline
if __name__ == "__main__":
    main()