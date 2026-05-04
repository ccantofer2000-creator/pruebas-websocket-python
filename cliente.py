import asyncio
import json
import websockets
import os
import http
import logging  # <-- Nueva librería
from datetime import datetime

# --- SILENCIAR RUIDO DE INTERNET ---
# Esto evita que websockets imprima errores gigantes cuando Render o bots escanean el puerto
logging.getLogger("websockets.server").setLevel(logging.CRITICAL)
logging.getLogger("websockets.protocol").setLevel(logging.CRITICAL)

# --- CONFIGURACIÓN ---
WS_PORT = int(os.environ.get("PORT", 7788))

# --- MANEJADOR DE HEALTH CHECKS (Para Render) ---
async def process_request(connection, request):
    if request.path == "/":
        return connection.respond(http.HTTPStatus.OK, "Servidor WebSocket OK\n")
    return None

async def handle_terminal(websocket):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Equipo conectado.")
    try:
        async for message in websocket:
            print(f"\n--- Mensaje Recibido ({datetime.now().strftime('%H:%M:%S')}) ---")
            print(message)
            
            try:
                data = json.loads(message)
                if data.get("cmd") == "reg":
                    res = {
                        "ret": "reg",
                        "result": True,
                        "cloudtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "nosenduser": True
                    }
                    await websocket.send(json.dumps(res))
                    print(">>> Respuesta de registro enviada.")
            except json.JSONDecodeError:
                print("Error: El mensaje recibido no es un JSON válido.")

    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Equipo desconectado.")

async def main():
    print(f"Servidor iniciado en el puerto {WS_PORT}. Esperando datos...")
    async with websockets.serve(handle_terminal, "0.0.0.0", WS_PORT, process_request=process_request):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")