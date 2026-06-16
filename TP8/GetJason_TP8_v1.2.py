"""
getJason.py

Copyright UADERFCyT-IS2©2024
Todos los derechos reservados.

Sistema de lectura de archivos JSON desarrollado para la catedra de
Ingeniería de Software II.

Permite recuperar valores almacenados en un archivo JSON.
Implementa el patrón de diseño Singleton para garantizar una única
instancia del lector de datos durante toda la ejecución del programa.

Además, se aplica la estrategia "Branching by abstraction" para permitir
la coexistencia entre la implementación procedural original y la nueva
versión orientada a objetos.

Uso:
    python getJason.py <archivo_json> [clave]

Parámetros:
    archivo_json : ruta al archivo JSON de entrada (debe existir y ser legible).
    clave        : clave a buscar dentro del JSON (opcional).
                   Si no se especifica, se utiliza "token1" por defecto.

Códigos de salida:
    0  : ejecución exitosa.
    1  : error de uso / parámetros inválidos.
    2  : error de acceso o lectura del archivo.
    3  : error de formato JSON.
    4  : clave no encontrada en el JSON.
    99 : error inesperado capturado.
"""

import json
import os
import sys


# Constantes

DEFAULT_KEY = "token1"
VERSION = "1.2"

EXIT_OK             = 0
EXIT_USO            = 1
EXIT_ARCHIVO        = 2
EXIT_JSON           = 3
EXIT_CLAVE          = 4
EXIT_INESPERADO     = 99

 
# Abstracción común (Branching by abstraction)

class JsonProvider:#
    """
    Abstracción para acceso a datos JSON.

    Permite desacoplar el código cliente de la implementación concreta,
    facilitando la transición entre la versión procedural original y la
    nueva implementación basada en Singleton.
    """

    def obtener_valor(self, clave):
        """
        Método abstracto que debe ser implementado por las clases hijas.
        """
        raise NotImplementedError



# Implementación legacy (versión procedural original)

class LegacyJsonReader(JsonProvider):
    """
    Implementación basada en la versión original procedural.

    Cada consulta realiza nuevamente la apertura y lectura completa
    del archivo JSON.
    """

    def __init__(self, json_file: str) -> None:
        self.json_file = json_file

    def obtener_valor(self, clave: str = DEFAULT_KEY):
        """
        Recupera un valor desde el archivo JSON utilizando la lógica
        original del programa.
        """
        with open(self.json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data[clave]


# Singleton: JsonReader

class JsonReader(JsonProvider):
    """
    Lector de archivos JSON implementado como Singleton.

    Garantiza que solo exista una instancia del lector durante toda la
    ejecución. La instancia carga el archivo JSON una única vez; lecturas
    posteriores sobre el mismo archivo reutilizan los datos en memoria.

    Atributos de clase:
        _instancia  : referencia a la única instancia permitida.
        _json_file  : ruta del archivo JSON cargado.
        _data       : contenido del JSON como diccionario Python.
    """

    _instancia: "JsonReader | None" = None
    _json_file: "str | None"        = None
    _data:      "dict | None"       = None

    
    # Control de instancia única
    
    def __new__(cls, json_file: str) -> "JsonReader":
        """
        Devuelve siempre la misma instancia.
        Si se solicita un archivo distinto al ya cargado, recarga los datos.
        """
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, json_file: str) -> None:
        """
        Inicializa (o reinicializa) la instancia con el archivo indicado.
        La carga real del JSON queda diferida hasta la primera consulta.
        """
        if json_file != self._json_file:
            # Nuevo archivo: invalidar datos previos
            JsonReader._json_file = json_file
            JsonReader._data      = None

    
    # Validaciones
    
    @staticmethod
    def validar_archivo(json_file: str) -> tuple[bool, int, str]:
        """
        Verifica que el archivo exista, no sea un directorio y sea legible.

        Retorna:
            (True, EXIT_OK, "")               si todo está bien.
            (False, código_error, mensaje)    si hay algún problema.
        """
        if not json_file or not json_file.strip():
            return False, EXIT_USO, "Error: la ruta del archivo no puede estar vacía."

        if not os.path.exists(json_file):
            return False, EXIT_ARCHIVO, f"Error: el archivo '{json_file}' no existe."

        if os.path.isdir(json_file):
            return False, EXIT_ARCHIVO, f"Error: '{json_file}' es un directorio, no un archivo."

        if not os.access(json_file, os.R_OK):
            return False, EXIT_ARCHIVO, f"Error: sin permisos de lectura sobre '{json_file}'."

        return True, EXIT_OK, ""

    @staticmethod
    def validar_clave(clave: str) -> tuple[bool, int, str]:
        """
        Verifica que la clave sea una cadena no vacía.

        Retorna:
            (True, EXIT_OK, "")               si es válida.
            (False, código_error, mensaje)    si no lo es.
        """
        if not isinstance(clave, str) or not clave.strip():
            return False, EXIT_USO, "Error: la clave no puede estar vacía."
        return True, EXIT_OK, ""

    
    # Carga del archivo
    
    def _cargar(self) -> tuple[bool, int, str]:
        """
        Lee y parsea el archivo JSON, almacenando el resultado en _data.

        Retorna:
            (True, EXIT_OK, "")               si la carga fue exitosa.
            (False, código_error, mensaje)    ante cualquier problema.
        """
        if JsonReader._data is not None:
            # Ya cargado previamente para este archivo
            return True, EXIT_OK, ""

        try:
            with open(JsonReader._json_file, "r", encoding="utf-8") as fp:
                JsonReader._data = json.load(fp)

        except FileNotFoundError:
            return False, EXIT_ARCHIVO, f"Error: el archivo '{JsonReader._json_file}' no se encontró al intentar abrirlo."

        except PermissionError:
            return False, EXIT_ARCHIVO, f"Error: permiso denegado al leer '{JsonReader._json_file}'."

        except json.JSONDecodeError as exc:
            return False, EXIT_JSON, f"Error: el archivo no contiene JSON válido ({exc})."

        except OSError as exc:
            return False, EXIT_ARCHIVO, f"Error de sistema al leer el archivo: {exc}."

        return True, EXIT_OK, ""

    
    # Interfaz pública
    
    def obtener_valor(self, clave: str = DEFAULT_KEY) -> tuple[str | None, int, str]:
        """
        Devuelve el valor asociado a *clave* dentro del JSON.

        Retorna:
            (valor, EXIT_OK, "")              si la clave existe.
            (None,  código_error, mensaje)    ante cualquier problema.
        """
        # Validar clave antes de cualquier I/O
        ok, codigo, mensaje = self.validar_clave(clave)
        if not ok:
            return None, codigo, mensaje

        # Cargar el archivo si aún no se hizo
        ok, codigo, mensaje = self._cargar()
        if not ok:
            return None, codigo, mensaje

        if clave not in JsonReader._data:
            return None, EXIT_CLAVE, f"Error: la clave '{clave}' no existe en el JSON."

        return JsonReader._data[clave], EXIT_OK, ""

    
    # Representación
    
    def __repr__(self) -> str:
        cargado = "cargado" if JsonReader._data is not None else "no cargado"
        return f"JsonReader(archivo='{JsonReader._json_file}', estado={cargado})"


class GestorPagos:
    """
    Componente encargado de gestionar solicitudes de pago.

    Utiliza el Singleton JsonReader para obtener la clave asociada
    al token bancario seleccionado.
    """

    def __init__(self, archivo_json: str) -> None:
        self.lector = JsonReader(archivo_json)

    def obtener_clave_banco(self, token: str):
        """
        Obtiene la clave asociada al token indicado.
        """
        clave, codigo, mensaje = self.lector.obtener_valor(token)

        if codigo != EXIT_OK:
            raise ValueError(mensaje)

        return clave



# Registro de pagos: entidad y colección iterable (patrón Iterator)

class RegistroPago:
    """
    Representa un pago realizado: número de pedido, token utilizado y monto.
    """

    def __init__(self, numero_pedido: int, token: str, monto: float) -> None:
        self.numero_pedido = numero_pedido
        self.token         = token
        self.monto         = monto

    def __repr__(self) -> str:
        return (
            f"Pedido #{self.numero_pedido:04d} | "
            f"Token: {self.token} | "
            f"Monto: ${self.monto:.2f}"
        )


class IteradorPagos:
    """
    Iterador concreto sobre la lista de registros de pagos.

    Implementa el protocolo de iteración de Python (__iter__ / __next__)
    permitiendo recorrer la colección de pagos en orden cronológico
    sin exponer la estructura interna de almacenamiento.
    """

    def __init__(self, registros: list[RegistroPago]) -> None:
        self._registros = registros
        self._indice    = 0

    def __iter__(self) -> "IteradorPagos":
        return self

    def __next__(self) -> RegistroPago:
        if self._indice >= len(self._registros):
            raise StopIteration
        registro = self._registros[self._indice]
        self._indice += 1
        return registro


class ColeccionPagos:
    """
    Colección de registros de pago.

    Actúa como el Agregado (Aggregate) del patrón Iterator:
    almacena los pagos internamente y provee un iterador para recorrerlos.
    """

    def __init__(self) -> None:
        self._registros: list[RegistroPago] = []

    def agregar(self, registro: RegistroPago) -> None:
        """Agrega un nuevo registro de pago al final de la colección."""
        self._registros.append(registro)

    def crear_iterador(self) -> IteradorPagos:
        """Devuelve un iterador en orden cronológico (de inserción)."""
        return IteradorPagos(self._registros)

    def __iter__(self) -> IteradorPagos:
        """Permite usar la colección directamente en bucles for."""
        return self.crear_iterador()

    def __len__(self) -> int:
        return len(self._registros)



# Cadena de responsabilidad: ManejadorPago y cuentas concretas

class ManejadorPago:
    """
    Clase base para la cadena de responsabilidad.
    """

    def __init__(self):
        self.siguiente = None

    def establecer_siguiente(self, siguiente):
        self.siguiente = siguiente
        return siguiente

    def procesar_pago(self, numero_pedido: int, monto: float) -> "RegistroPago | None":
        raise NotImplementedError


class CuentaToken1(ManejadorPago):
    """
    Cuenta asociada al token1.
    """

    def __init__(self):
        super().__init__()
        self.token = "token1"
        self.saldo = 1000.0

    def procesar_pago(self, numero_pedido: int, monto: float) -> "RegistroPago | None":
        """
        Si el saldo es suficiente, debita el monto y retorna un RegistroPago.
        En caso contrario, delega al siguiente manejador de la cadena.

        Retorna:
            RegistroPago con (numero_pedido, token, monto) si el pago fue procesado.
            None si ningún manejador pudo procesar el pago.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            return RegistroPago(numero_pedido, self.token, monto)

        if self.siguiente:
            return self.siguiente.procesar_pago(numero_pedido, monto)

        return None


class CuentaToken2(ManejadorPago):
    """
    Cuenta asociada al token2.
    """

    def __init__(self):
        super().__init__()
        self.token = "token2"
        self.saldo = 2000.0

    def procesar_pago(self, numero_pedido: int, monto: float) -> "RegistroPago | None":
        """
        Si el saldo es suficiente, debita el monto y retorna un RegistroPago.
        En caso contrario, delega al siguiente manejador de la cadena.

        Retorna:
            RegistroPago con (numero_pedido, token, monto) si el pago fue procesado.
            None si ningún manejador pudo procesar el pago.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            return RegistroPago(numero_pedido, self.token, monto)

        if self.siguiente:
            return self.siguiente.procesar_pago(numero_pedido, monto)

        return None



# Procesador de pagos: orquesta la cadena + colección

class ProcesadorPagos:
    """
    Orquesta la cadena de responsabilidad y acumula el historial de pagos.

    Combina los patrones Chain of Responsibility (ruteo entre cuentas) e
    Iterator (recorrido cronológico del historial).
    """

    def __init__(self) -> None:
        # Construir la cadena: token1 → token2
        self._cuenta1 = CuentaToken1()
        self._cuenta2 = CuentaToken2()
        self._cuenta1.establecer_siguiente(self._cuenta2)

        # Colección de pagos realizados (Agregado del patrón Iterator)
        self._historial = ColeccionPagos()

        # Contador interno de pedidos
        self._proximo_pedido = 1

    def realizar_pago(self, monto: float) -> "RegistroPago | None":
        """
        Intenta procesar un pago por *monto* recorriendo la cadena.

        Asigna automáticamente el número de pedido, delega a la cadena de
        responsabilidad y, si el pago fue exitoso, lo registra en el
        historial.

        Parámetros:
            monto : importe del pago a procesar.

        Retorna:
            RegistroPago  si al menos una cuenta tenía saldo suficiente.
            None          si ninguna cuenta pudo cubrir el monto.
        """
        numero_pedido = self._proximo_pedido
        self._proximo_pedido += 1

        registro = self._cuenta1.procesar_pago(numero_pedido, monto)

        if registro is not None:
            self._historial.agregar(registro)

        return registro

    def listar_pagos(self) -> None:
        """
        Imprime en pantalla todos los pagos realizados en orden cronológico.

        Utiliza el iterador de ColeccionPagos (patrón Iterator) para
        recorrer el historial sin acceder directamente a la estructura
        interna de almacenamiento.
        """
        total = len(self._historial)
        if total == 0:
            print("No se han registrado pagos.")
            return

        print(f"\n{'─' * 50}")
        print(f"  Historial de pagos ({total} registro/s)")
        print(f"{'─' * 50}")

        for registro in self._historial:          # usa __iter__ → IteradorPagos
            print(f"  {registro}")

        print(f"{'─' * 50}\n")

    @property
    def saldo_token1(self) -> float:
        return self._cuenta1.saldo

    @property
    def saldo_token2(self) -> float:
        return self._cuenta2.saldo



# Interfaz de línea de comandos

def parsear_argumentos() -> tuple[str | None, str, int, str]:
    """
    Analiza y valida los argumentos de sys.argv.

    Retorna:
        (json_file, clave, EXIT_OK, "")              si los args son válidos.
        (None,      "",    código_error, mensaje)    si hay algún problema.
    """
    argc = len(sys.argv)

    # Sin argumentos
    if argc < 2:
        uso = (
            "Uso: python getJason.py <archivo_json> [clave]\n"
            f"     Si no se indica clave se usa '{DEFAULT_KEY}' por defecto."
        )
        return None, "", EXIT_USO, uso

    # Demasiados argumentos
    if argc > 3:
        return None, "", EXIT_USO, (
            f"Error: demasiados argumentos ({argc - 1}). "
            "Se esperan 1 o 2 argumentos."
        )

    json_file = sys.argv[1].strip()
    clave     = sys.argv[2].strip() if argc == 3 else DEFAULT_KEY

    # Validar ruta del archivo
    ok, codigo, mensaje = JsonReader.validar_archivo(json_file)
    if not ok:
        return None, "", codigo, mensaje

    # Validar clave
    ok, codigo, mensaje = JsonReader.validar_clave(clave)
    if not ok:
        return None, "", codigo, mensaje

    return json_file, clave, EXIT_OK, ""


def main() -> int:
    """
    Punto de entrada principal.

    Nunca lanza excepciones no capturadas; siempre retorna un código de
    salida entero y termina de forma controlada.

    Cuando se ejecuta sin argumentos adicionales realiza también una
    demostración del procesador de pagos (pedidos de $500.-) para
    ilustrar el funcionamiento del patrón Iterator sobre el historial.
    """
    try:
        # mostrar version del programa
        if len(sys.argv) == 2 and sys.argv[1] == "-v":
            print(f"Versión {VERSION}")
            return EXIT_OK

        # 1. Parsear y validar argumentos
        json_file, clave, codigo, mensaje = parsear_argumentos()
        if codigo != EXIT_OK:
            print(mensaje, file=sys.stderr)
            return codigo

        # 2. Obtener la instancia Singleton y consultar el valor
        lector = JsonReader(json_file)
        valor, codigo, mensaje = lector.obtener_valor(clave)

        if codigo != EXIT_OK:
            print(mensaje, file=sys.stderr)
            return codigo

        # 3. Resultado exitoso
        print(valor)

        # 4. Demostración del procesador de pagos
        print("\n--- Demostración ProcesadorPagos ---")
        procesador = ProcesadorPagos()
        monto_pago = 500.0
        cantidad_pedidos = 7       # 7 pedidos × $500 = $3500 > $1000 + $2000

        for _ in range(cantidad_pedidos):
            registro = procesador.realizar_pago(monto_pago)
            if registro:
                print(f"  Pago procesado  → {registro}")
            else:
                print(f"  Pago rechazado  → saldo insuficiente en todas las cuentas.")

        print(f"\n  Saldo restante token1: ${procesador.saldo_token1:.2f}")
        print(f"  Saldo restante token2: ${procesador.saldo_token2:.2f}")

        procesador.listar_pagos()

        return EXIT_OK

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.", file=sys.stderr)
        return EXIT_USO

    except Exception as exc:  # pylint: disable=broad-except
        # Captura cualquier error inesperado para cumplir el requisito de
        # "nunca terminar con un error de sistema".
        print(f"Error inesperado: {exc}", file=sys.stderr)
        return EXIT_INESPERADO



# Punto de entrada

if __name__ == "__main__":
    sys.exit(main())