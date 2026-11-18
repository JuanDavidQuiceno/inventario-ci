"""Servidor HTTP mínimo (solo biblioteca estándar) para la prueba de humo."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from inventario import __version__
from inventario.core import Inventario

inventario = Inventario()
inventario.agregar("teclado", 10, 45000)
inventario.agregar("mouse", 25, 20000)


def estado():
    """Respuesta del endpoint /salud."""
    return {"estado": "ok", "version": __version__}


class Manejador(BaseHTTPRequestHandler):
    def _responder(self, codigo, cuerpo):
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        if self.path == "/salud":
            self._responder(200, estado())
        elif self.path == "/productos":
            self._responder(200, inventario.listar())
        else:
            self._responder(404, {"error": "no encontrado"})


def main(puerto=8000):
    servidor = ThreadingHTTPServer(("0.0.0.0", puerto), Manejador)
    print(f"Inventario {__version__} escuchando en el puerto {puerto}", flush=True)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
