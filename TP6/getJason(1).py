"""
getJason.py

Permite recuperar valores almacenados en un archivo JSON.

Uso:
    python getJason.py <archivo_json> [clave]

Parámetros:
    archivo_json : archivo JSON de entrada.
    clave        : clave a buscar dentro del JSON (opcional).

Si no se especifica una clave, se utiliza "token1" por defecto.
"""

import json
import sys

DEFAULT_KEY = "token1"


def get_value_from_json(json_file, key=DEFAULT_KEY):
    """
    Recupera un valor desde un archivo JSON utilizando una clave.
    """

    with open(json_file, "r") as file:
        data = json.load(file)

    return data[key]


def main():
    """
    Función principal del programa.
    """

    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo_json> [clave]")
        sys.exit(1)

    json_file = sys.argv[1]

    if len(sys.argv) >= 3:
        json_key = sys.argv[2]
    else:
        json_key = DEFAULT_KEY

    try:
        value = get_value_from_json(json_file, json_key)
        print(value)

    except FileNotFoundError:
        print("Error: archivo JSON no encontrado.")

    except KeyError:
        print(f"Error: la clave '{json_key}' no existe en el JSON.")

    except json.JSONDecodeError:
        print("Error: el archivo no contiene un JSON válido.")


if __name__ == "__main__":
    main()