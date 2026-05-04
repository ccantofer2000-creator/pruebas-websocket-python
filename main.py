import json
import logging
import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# --- RUTAS HTTP (Health Check para Render) ---
@app.get("/")
async def root():
    # Render recibirá este JSON y sabrá que tu app está viva
    return {"status": "ok", "message": "Servidor AiFace Online"}

# --- RUTAS WEBSOCKET (Para tu equipo Biométrico) ---
# Nota: Uso "/" asumiendo que el equipo se conecta a la raíz. 
# Si tu cliente apunta a "/ws", cámbialo a @app.websocket("/ws")
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] Equipo conectado.")
    
    try:
        while True:
            # 1. Leer el mensaje como texto
            message = await websocket.receive_text()
            logger.info(f"\n--- Mensaje Recibido ({datetime.now().strftime('%H:%M:%S')}) ---")
            logger.info(message)
            
            # 2. Procesar el JSON del equipo
            try:
                data = json.loads(message)
                
                # 3. Responder al comando de registro ("reg")
                if data.get("cmd") == "reg":
                    res = {
                        "ret": "reg",
                        "result": True,
                        "cloudtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "nosenduser": True
                    }
                    # Enviar la respuesta convertida a string JSON
                    await websocket.send_text(json.dumps(res))
                    logger.info(">>> Respuesta de registro enviada.")
                    
            except json.JSONDecodeError:
                logger.error("Error: El mensaje recibido no es un JSON válido.")

    except WebSocketDisconnect:
        logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] Equipo desconectado.")

# --- ARRANQUE DEL SERVIDOR ---
if __name__ == "__main__":
    # Lee el puerto dinámico de Render (o usa 7788 si estás en tu PC local)
    port = int(os.environ.get("PORT", 7788))
    
    # Inicia el servidor usando uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)