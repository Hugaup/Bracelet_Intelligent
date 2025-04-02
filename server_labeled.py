import csv
import asyncio
import time
import os
from aiohttp import web, WSMsgType

clients = set()
csv_writer = None
csv_file = None
recording = True
end_time = None

# 🔹 Demande le label
label = input("🏷️  Type de mouvement (ex: repos, frisson, convulsion) : ").strip().lower()
if label == "":
    label = "non_defini"

# 🔹 Crée le dossier s'il n'existe pas
folder_path = os.path.join("data", label)
os.makedirs(folder_path, exist_ok=True)

# 🔹 Demande le nom du fichier
csv_filename = input("📁 Nom du fichier CSV (ex: test1.csv) : ").strip()
if not csv_filename.endswith(".csv"):
    csv_filename += ".csv"

csv_path = os.path.join(folder_path, csv_filename)

# 🔹 Durée d'enregistrement
duration_input = input("⏱️ Durée d'enregistrement en secondes (laisser vide pour illimité) : ").strip()
if duration_input:
    try:
        duration_seconds = int(duration_input)
        end_time = time.time() + duration_seconds
        print(f"⏳ Enregistrement pendant {duration_seconds} secondes...")
    except ValueError:
        print("⛔ Durée invalide. Enregistrement illimité activé.")
        end_time = None
else:
    print("🔄 Enregistrement illimité activé.")
    end_time = None

async def websocket_handler(request):
    global csv_writer, csv_file, recording, end_time

    ws = web.WebSocketResponse(protocols=["arduino"])
    await ws.prepare(request)
    clients.add(ws)

    if recording:
        csv_file = open(csv_path, mode="a", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "accel.x", "accel.y", "accel.z",
                             "gyro.x", "gyro.y", "gyro.z", "label"])

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            now = time.time()
            print(f"📥 Reçu : {msg.data}")

            if end_time and now > end_time:
                if recording:
                    print(f"🛑 Enregistrement terminé (temps écoulé).")
                    recording = False
                    if csv_file:
                        csv_file.close()

            if recording and csv_writer:
                values = msg.data.strip().split(",")
                values.append(label)
                csv_writer.writerow(values)
                csv_file.flush()

            for client in clients.copy():
                if client != ws:
                    try:
                        await client.send_str(msg.data)
                    except:
                        clients.discard(client)

    clients.discard(ws)
    return ws

async def index_handler(request):
    return web.FileResponse('./www/index.html')

app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    print(f"🚀 Serveur lancé sur : http://localhost:8000")
    web.run_app(app, host='0.0.0.0', port=8000)
