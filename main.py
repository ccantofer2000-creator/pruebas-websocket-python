import asyncio
import json
import websockets
from datetime import datetime

# --- CONFIGURACIÓN ---
WS_PORT = 7788

async def handle_terminal(websocket):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Equipo conectado.")
    try:
        async for message in websocket:
            # 1. Mostrar lo que envía el equipo en consola
            print(f"\n--- Mensaje Recibido ({datetime.now().strftime('%H:%M:%S')}) ---")
            print(message)
            
            # 2. Responder al equipo (necesario para mantener el flujo del protocolo)
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
    async with websockets.serve(handle_terminal, "0.0.0.0", WS_PORT):
        await asyncio.Future()  # Mantiene el servidor corriendo para siempre

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")