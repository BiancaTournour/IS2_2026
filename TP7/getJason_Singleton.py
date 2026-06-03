"""
getJason.py

Permite recuperar valores almacenados en un archivo JSON.
Implementa el patrón de diseño Singleton para garantizar una única
instancia del lector de datos durante toda la ejecución del programa.

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

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
DEFAULT_KEY = "token1"

EXIT_OK             = 0
EXIT_USO            = 1
EXIT_ARCHIVO        = 2
EXIT_JSON           = 3
EXIT_CLAVE          = 4
EXIT_INESPERADO     = 99


# ---------------------------------------------------------------------------
# Singleton: JsonReader
# ---------------------------------------------------------------------------
class JsonReader:
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

    # ------------------------------------------------------------------
    # Control de instancia única
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Carga del archivo
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Interfaz pública
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        cargado = "cargado" if JsonReader._data is not None else "no cargado"
        return f"JsonReader(archivo='{JsonReader._json_file}', estado={cargado})"


# ---------------------------------------------------------------------------
# Interfaz de línea de comandos
# ---------------------------------------------------------------------------
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
    """
    try:
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
        return EXIT_OK

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.", file=sys.stderr)
        return EXIT_USO

    except Exception as exc:  # pylint: disable=broad-except
        # Captura cualquier error inesperado para cumplir el requisito de
        # "nunca terminar con un error de sistema".
        print(f"Error inesperado: {exc}", file=sys.stderr)
        return EXIT_INESPERADO


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())