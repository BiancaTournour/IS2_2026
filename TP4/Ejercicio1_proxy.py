from abc import ABC, abstractmethod
import time

class IPING(ABC): 
    """Interfaz común para el ping real y el proxy."""

    @abstractmethod
    def execute(self, ip: str) -> None:
        pass

class Ping(IPING): # Objeto real que realiza la operación de ping.

    def __init__(self) -> None:
        pass

    def execute(self, ip: str) -> None:
        if not ip.startswith("192."):
            print(f"[PING] Dirección inválida ejecutar: {ip}") #Error
            return

        self._run_ping(ip)

    def executefree(self, ip: str) -> None:
        self._run_ping(ip)

    def _run_ping(self, ip: str) -> None: #SIMULA EL PING 
        print(f"[PING] Iniciando 10 intentos de ping a {ip}...")
        for intento in range(1, 11):
            print(f"[PING] Intento {intento}/10 -> {ip}")
            time.sleep(0.1)
            print(f"[PING] Respuesta recibida de {ip}.")
        print(f"[PING] Finalizaron los 10 intentos de ping a {ip}.\n")

class PingProxy(IPING): # Proxy que controla el acceso al objeto Ping real.

    def __init__(self) -> None:
        self._ping = Ping()

    def execute(self, ip: str) -> None:
        if ip == "192.168.0.254":
            print("[PROXY] Dirección especial detectada: 192.168.0.254")
            print("[PROXY] Redirigiendo ping a www.google.com.\n") #Usando el metodo executefree
            self._ping.executefree("www.google.com")
        else:
            print(f"[PROXY] Reenviando ejecución al objeto Ping para {ip}.\n")
            self._ping.execute(ip)

if __name__ == "__main__":
    ping = Ping()
    ping.execute("192.168.0.10") #dirección válida
    ping.execute("10.0.0.1") #DIRECCION INVALIDA
    ping.executefree("10.0.0.1") #EJECUTA EL PING A UNA DIRECCION INVALIDA

    proxy = PingProxy()
    proxy.execute("192.168.0.254")
    proxy.execute("192.168.0.100")
