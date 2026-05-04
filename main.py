import asyncio
import json
import websockets
import os
import http
from datetime import datetime

# --- CONFIGURACIÓN ---
WS_PORT = int(os.environ.get("PORT", 7788))

# --- MANEJADOR DE HEALTH CHECKS (Para Render) ---
async def process_request(connection, request):
    # Si Render envía un HTTP GET a la raíz ("/") para ver si estamos vivos
    if request.path == "/":
        # Le respondemos con un 200 OK para que Render se quede tranquilo
        return connection.respond(http.HTTPStatus.OK, "Servidor WebSocket OK\n")
    # Si no es la raíz, devolvemos None para continuar con la conexión WebSocket normal
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
    # ATENCIÓN: Aquí agregamos "process_request=process_request"
    async with websockets.serve(handle_terminal, "0.0.0.0", WS_PORT, process_request=process_request):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")