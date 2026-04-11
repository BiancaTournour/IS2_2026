"""Unit tests for rpn.py — cobertura >= 90% — errores via try/except."""

import math
import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import rpn
from rpn import RPNError, evaluate, fmt, main, memory


def ev(expr):
    """Shortcut: evalúa una expresión RPN y retorna el resultado."""
    return evaluate(expr)


def assert_rpn_error(expr, substring=None):
    """
    Ejecuta una expresión RPN y verifica que lanza RPNError.
    Usa try/except explícito tal como lo requiere la cátedra.
    Retorna el mensaje de error para validaciones adicionales.
    """
    try:
        evaluate(expr)
        raise AssertionError(
            f"Se esperaba RPNError para '{expr}', pero no se lanzó ninguna excepción."
        )
    except RPNError as err:
        msg = str(err)
        if substring is not None:
            assert substring.lower() in msg.lower(), (
                f"Se esperaba '{substring}' en el mensaje, pero se obtuvo: '{msg}'"
            )
        return msg


# ---------------------------------------------------------------------------
# Aritmética básica
# ---------------------------------------------------------------------------
class TestBasicArithmetic(unittest.TestCase):
    """Tests de operaciones aritméticas básicas."""

    def test_addition(self):
        """Suma de dos enteros."""
        self.assertEqual(ev('3 4 +'), 7)

    def test_subtraction(self):
        """Resta de dos enteros."""
        self.assertEqual(ev('10 3 -'), 7)

    def test_multiplication(self):
        """Multiplicación de dos enteros."""
        self.assertEqual(ev('3 4 *'), 12)

    def test_division(self):
        """División exacta."""
        self.assertAlmostEqual(ev('10 2 /'), 5.0)

    def test_float_operands(self):
        """Suma con flotantes."""
        self.assertAlmostEqual(ev('2.5 1.5 +'), 4.0)

    def test_negative_operands(self):
        """Multiplicación con negativo."""
        self.assertAlmostEqual(ev('-3 2 *'), -6)

    def test_negative_result(self):
        """Resta con resultado negativo."""
        self.assertAlmostEqual(ev('1 5 -'), -4)

    def test_float_division(self):
        """División con resultado flotante."""
        self.assertAlmostEqual(ev('7 2 /'), 3.5)

    def test_chain_ops(self):
        """Expresión encadenada del enunciado."""
        self.assertEqual(ev('5 1 2 + 4 * + 3 -'), 14)

    def test_chain_ops2(self):
        """Segunda expresión encadenada del enunciado."""
        self.assertEqual(ev('2 3 4 * +'), 14)


# ---------------------------------------------------------------------------
# División por cero
# ---------------------------------------------------------------------------
class TestDivisionByZero(unittest.TestCase):
    """Tests de errores de división por cero."""

    def test_div_zero_int(self):
        """División entera por cero lanza RPNError."""
        assert_rpn_error('3 0 /', substring='zero')

    def test_div_zero_float(self):
        """División flotante por cero lanza RPNError."""
        assert_rpn_error('5.0 0.0 /', substring='zero')

    def test_inv_zero(self):
        """Inverso de cero lanza RPNError."""
        assert_rpn_error('0 1/x', substring='zero')


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
class TestConstants(unittest.TestCase):
    """Tests de constantes matemáticas predefinidas."""

    def test_pi(self):
        """Constante p = pi."""
        self.assertAlmostEqual(ev('p'), math.pi)

    def test_e(self):
        """Constante e = número de Euler."""
        self.assertAlmostEqual(ev('e'), math.e)

    def test_phi(self):
        """Constante j = número áureo."""
        self.assertAlmostEqual(ev('j'), (1 + math.sqrt(5)) / 2)


# ---------------------------------------------------------------------------
# Comandos de pila
# ---------------------------------------------------------------------------
class TestStackCommands(unittest.TestCase):
    """Tests de comandos de manipulación de pila."""

    def test_dup(self):
        """dup duplica el tope de la pila."""
        self.assertEqual(ev('7 dup +'), 14)

    def test_swap(self):
        """swap intercambia los dos valores del tope."""
        self.assertEqual(ev('3 5 swap -'), 2)

    def test_drop(self):
        """drop descarta el tope de la pila."""
        self.assertEqual(ev('1 2 drop'), 1)

    def test_clear_then_push(self):
        """clear vacía la pila completamente."""
        self.assertEqual(ev('9 8 7 clear 42'), 42)

    def test_dup_underflow(self):
        """dup sobre pila vacía lanza RPNError."""
        assert_rpn_error('dup', substring='underflow')

    def test_swap_underflow(self):
        """swap con menos de 2 elementos lanza RPNError."""
        assert_rpn_error('5 swap', substring='underflow')

    def test_drop_underflow(self):
        """drop sobre pila vacía lanza RPNError."""
        assert_rpn_error('drop', substring='underflow')


# ---------------------------------------------------------------------------
# Funciones matemáticas — camino feliz
# ---------------------------------------------------------------------------
class TestMathFunctions(unittest.TestCase):
    """Tests de funciones matemáticas con valores válidos."""

    def test_sqrt(self):
        """Raíz cuadrada de 9."""
        self.assertAlmostEqual(ev('9 sqrt'), 3.0)

    def test_sqrt_144(self):
        """Raíz cuadrada de 144."""
        self.assertAlmostEqual(ev('144 sqrt'), 12.0)

    def test_log(self):
        """Logaritmo base 10 de 1000."""
        self.assertAlmostEqual(ev('1000 log'), 3.0)

    def test_ln(self):
        """Logaritmo natural de 1."""
        self.assertAlmostEqual(ev('1 ln'), 0.0)

    def test_ex(self):
        """Exponencial de 0."""
        self.assertAlmostEqual(ev('0 ex'), 1.0)

    def test_10x(self):
        """10 elevado a la 2."""
        self.assertAlmostEqual(ev('2 10x'), 100.0)

    def test_yx(self):
        """2 elevado a la 3."""
        self.assertAlmostEqual(ev('2 3 yx'), 8.0)

    def test_inv(self):
        """Inverso de 4."""
        self.assertAlmostEqual(ev('4 1/x'), 0.25)

    def test_chs(self):
        """Cambio de signo de positivo."""
        self.assertAlmostEqual(ev('5 chs'), -5.0)

    def test_chs_negative(self):
        """Cambio de signo de negativo."""
        self.assertAlmostEqual(ev('-3 chs'), 3.0)


# ---------------------------------------------------------------------------
# Funciones matemáticas — condiciones de error (try/except explícito)
# ---------------------------------------------------------------------------
class TestMathFunctionErrors(unittest.TestCase):
    """Tests de errores de dominio en funciones matemáticas."""

    def test_sqrt_negative(self):
        """sqrt de número negativo lanza RPNError."""
        assert_rpn_error('-1 sqrt', substring='negativ')

    def test_log_zero(self):
        """log de cero lanza RPNError."""
        assert_rpn_error('0 log', substring='non-positive')

    def test_log_negative(self):
        """log de negativo lanza RPNError."""
        assert_rpn_error('-5 log', substring='non-positive')

    def test_ln_zero(self):
        """ln de cero lanza RPNError."""
        assert_rpn_error('0 ln', substring='non-positive')


# ---------------------------------------------------------------------------
# Trigonometría (grados)
# ---------------------------------------------------------------------------
class TestTrigonometry(unittest.TestCase):
    """Tests de funciones trigonométricas en grados."""

    def test_sin_90(self):
        """sin(90°) = 1."""
        self.assertAlmostEqual(ev('90 sin'), 1.0)

    def test_sin_0(self):
        """sin(0°) = 0."""
        self.assertAlmostEqual(ev('0 sin'), 0.0)

    def test_cos_0(self):
        """cos(0°) = 1."""
        self.assertAlmostEqual(ev('0 cos'), 1.0)

    def test_cos_90(self):
        """cos(90°) ≈ 0."""
        self.assertAlmostEqual(ev('90 cos'), 0.0, places=10)

    def test_tan_45(self):
        """tg(45°) = 1."""
        self.assertAlmostEqual(ev('45 tg'), 1.0)

    def test_asin_1(self):
        """asin(1) = 90°."""
        self.assertAlmostEqual(ev('1 asin'), 90.0)

    def test_acos_1(self):
        """acos(1) = 0°."""
        self.assertAlmostEqual(ev('1 acos'), 0.0)

    def test_atan_1(self):
        """atg(1) = 45°."""
        self.assertAlmostEqual(ev('1 atg'), 45.0)

    def test_sin_30(self):
        """sin(30°) = 0.5."""
        self.assertAlmostEqual(ev('30 sin'), 0.5)

    def test_cos_60(self):
        """cos(60°) = 0.5."""
        self.assertAlmostEqual(ev('60 cos'), 0.5)


# ---------------------------------------------------------------------------
# Memoria STO/RCL — camino feliz
# ---------------------------------------------------------------------------
class TestMemory(unittest.TestCase):
    """Tests de almacenamiento y recuperación de memoria."""

    def setUp(self):
        """Resetea la memoria antes de cada test."""
        for i in range(10):
            memory[i] = 0.0

    def test_sto_rcl_basic(self):
        """Almacena y recupera un valor entero."""
        self.assertEqual(ev('42 0 sto 0 rcl'), 42)

    def test_sto_rcl_slot9(self):
        """Almacena y recupera en el slot 9."""
        self.assertAlmostEqual(ev('3.14 9 sto 9 rcl'), 3.14)

    def test_rcl_default_zero(self):
        """Memoria sin inicializar retorna 0."""
        self.assertEqual(ev('5 rcl'), 0.0)

    def test_sto_overwrite(self):
        """Sobreescritura de memoria funciona correctamente."""
        self.assertEqual(ev('10 0 sto 20 0 sto 0 rcl'), 20)


# ---------------------------------------------------------------------------
# Memoria STO/RCL — condiciones de error (try/except explícito)
# ---------------------------------------------------------------------------
class TestMemoryErrors(unittest.TestCase):
    """Tests de errores en comandos de memoria."""

    def test_sto_address_out_of_range(self):
        """STO con dirección fuera de rango lanza RPNError."""
        assert_rpn_error('99 10 sto', substring='address')

    def test_rcl_address_out_of_range(self):
        """RCL con dirección fuera de rango lanza RPNError."""
        assert_rpn_error('10 rcl', substring='address')

    def test_sto_float_address(self):
        """STO con dirección flotante lanza RPNError."""
        assert_rpn_error('5 1.5 sto', substring='address')


# ---------------------------------------------------------------------------
# Manejo general de errores (try/except explícito)
# ---------------------------------------------------------------------------
class TestErrorHandling(unittest.TestCase):
    """Tests de manejo general de errores de la calculadora."""

    def test_unknown_token(self):
        """Token desconocido lanza RPNError con el nombre del token."""
        msg = assert_rpn_error('3 foo +')
        self.assertIn('foo', msg)

    def test_too_many_values_on_stack(self):
        """Pila con más de un valor al final lanza RPNError."""
        msg = assert_rpn_error('3 4')
        self.assertIn('1', msg)

    def test_empty_stack_at_end(self):
        """Pila vacía al final lanza RPNError."""
        assert_rpn_error('1 drop', substring='1')

    def test_add_underflow(self):
        """Suma con un solo operando lanza RPNError."""
        assert_rpn_error('3 +', substring='underflow')

    def test_sub_underflow(self):
        """Resta con un solo operando lanza RPNError."""
        assert_rpn_error('3 -', substring='underflow')

    def test_mul_underflow(self):
        """Multiplicación con un solo operando lanza RPNError."""
        assert_rpn_error('3 *', substring='underflow')

    def test_div_underflow(self):
        """División con un solo operando lanza RPNError."""
        assert_rpn_error('3 /', substring='underflow')


# ---------------------------------------------------------------------------
# Función fmt
# ---------------------------------------------------------------------------
class TestFmt(unittest.TestCase):
    """Tests de formateo del resultado final."""

    def test_integer_float(self):
        """Float sin decimales se convierte a int."""
        self.assertEqual(fmt(3.0), 3)

    def test_real_float(self):
        """Float con decimales se mantiene como float."""
        self.assertEqual(fmt(3.5), 3.5)

    def test_native_int(self):
        """Entero nativo se mantiene como int."""
        self.assertEqual(fmt(7), 7)

    def test_negative_int_float(self):
        """Float negativo sin decimales se convierte a int."""
        self.assertEqual(fmt(-4.0), -4)


# ---------------------------------------------------------------------------
# main() — argumento CLI y stdin
# ---------------------------------------------------------------------------
class TestMain(unittest.TestCase):
    """Tests de la función main() como punto de entrada del programa."""

    def _run(self, args, stdin=None):
        """Ejecuta main() con argumentos y stdin simulados."""
        with patch('sys.argv', ['rpn.py'] + args), \
             patch('sys.stdout', new_callable=StringIO) as out, \
             patch('sys.stderr', new_callable=StringIO) as err:
            if stdin is not None:
                with patch('builtins.input', return_value=stdin):
                    try:
                        main()
                    except SystemExit:
                        pass
            else:
                try:
                    main()
                except SystemExit:
                    pass
        return out.getvalue().strip(), err.getvalue().strip()

    def test_main_args(self):
        """Expresión pasada como argumento CLI."""
        out, _ = self._run(['3', '4', '+'])
        self.assertEqual(out, '7')

    def test_main_stdin(self):
        """Expresión ingresada por stdin."""
        out, _ = self._run([], stdin='5 1 2 + 4 * + 3 -')
        self.assertEqual(out.splitlines()[-1], '14')

    def test_main_error_division_by_zero(self):
        """Error de división por cero se reporta en stderr."""
        try:
            _, err = self._run(['3', '0', '/'])
            self.assertIn('zero', err.lower())
        except SystemExit:
            pass

    def test_main_error_invalid_token(self):
        """Token inválido se reporta en stderr."""
        try:
            _, err = self._run(['abc'])
            self.assertTrue(len(err) > 0)
        except SystemExit:
            pass

    def test_main_eof(self):
        """EOFError en input() debe salir sin excepción."""
        with patch('sys.argv', ['rpn.py']), \
             patch('builtins.input', side_effect=EOFError):
            try:
                main()
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main(verbosity=2)