import asyncio
import json
import websockets

# --- CONFIGURACIÓN ---
# Usando una IP del rango 74.220.48.0/24
SERVER_IP = "74.220.48.0"
SERVER_PORT = "7788"
URI = f"ws://{SERVER_IP}:{SERVER_PORT}"

async def run_client():
    print(f"Intentando conectar al servidor en {URI}...")
    try:
        # Intentar establecer conexión con el servidor
        async with websockets.connect(URI) as websocket:
            print("✅ ¡Conectado exitosamente al servidor!")

            # Armar un paquete de datos simulando tu equipo AiFace
            datos_registro = {
                "cmd": "reg",
                "sn": "AXTG-SIMULADOR",
                "devinfo": {
                    "modelname": "AiFace-Test",
                    "cpu_temp": 45.5,
                    "mac": "AA-BB-CC-DD-EE-FF"
                }
            }

            # Enviar los datos al servidor
            mensaje_json = json.dumps(datos_registro)
            await websocket.send(mensaje_json)
            print(f">>> Mensaje enviado: {mensaje_json}")

            # Esperar la respuesta del servidor
            respuesta = await websocket.recv()
            print(f"<<< Respuesta del servidor: {respuesta}")

    except ConnectionRefusedError:
        print(f"❌ Error: Conexión rechazada. ¿Está el servidor corriendo en {SERVER_IP}:{SERVER_PORT}?")
    except TimeoutError:
        print(f"❌ Error: Tiempo de espera agotado (Timeout). Revisa reglas de Firewall para {SERVER_IP}.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    # Ejecutar la rutina asíncrona
    asyncio.run(run_client())