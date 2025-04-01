import asyncio
import csv
import os
import time
import joblib
import numpy as np
import pandas as pd
from aiohttp import web, WSMsgType
from collections import deque
from datetime import datetime
from scipy.signal import butter, filtfilt

# === Paramètres ===
WINDOW_SIZE = 150
STRIDE = 75
SAMPLING_RATE = 71.4  # fréquence réelle mesurée
buffer = []
window = deque(maxlen=WINDOW_SIZE)
clients = set()
scaler = joblib.load("scaler.joblib")
model = joblib.load("modele_entraine.joblib")

# === Fonction filtre passe-bas ===
def filtre_passe_bas(df, cutoff=10, fs=SAMPLING_RATE, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    for axis in ['accel.x', 'accel.y', 'accel.z', 'gyro.x', 'gyro.y', 'gyro.z']:
        if axis in df.columns:
            df[axis] = filtfilt(b, a, df[axis])
    return df

# === Initialisation fichier CSV ===
csv_writer = None
csv_file = None
recording = True
end_time = None

results_dir = "resultats"
os.makedirs(results_dir, exist_ok=True)

while True:
    base_name = input(" Nom du fichier CSV (ex: test1.csv) : ").strip()
    if not base_name.endswith(".csv"):
        base_name += ".csv"
    csv_filename = os.path.join(results_dir, base_name)
    if os.path.exists(csv_filename):
        print("❌ Ce fichier existe déjà. Choisis un autre nom.")
    else:
        break

try:
    duration = int(input(" Durée d'enregistrement (laisser vide pour illimité) : ") or 0)
    end_time = time.time() + duration if duration > 0 else None
except:
    end_time = None

print(f" Enregistrement dans : {csv_filename}")

# === Fonction d’extraction de features ===
def extraire_features(df):
    feats = {}
    for axis in ['accel.x', 'accel.y', 'accel.z', 'gyro.x', 'gyro.y', 'gyro.z']:
        if axis in df.columns:
            x = df[axis].values
            feats[f"{axis}_mean"] = np.mean(x)
            feats[f"{axis}_std"] = np.std(x)
            feats[f"{axis}_min"] = np.min(x)
            feats[f"{axis}_max"] = np.max(x)
            feats[f"{axis}_energy"] = np.sum(x ** 2)
            yf = np.fft.fft(x)
            xf = np.fft.fftfreq(len(x), 1 / SAMPLING_RATE)
            dominant_freq = abs(xf[np.argmax(np.abs(yf[:len(x)//2]))])
            feats[f"{axis}_dom_freq"] = dominant_freq
    return pd.DataFrame([feats])

prediction_buffer = deque(maxlen=3)

# === WebSocket handler ===
async def websocket_handler(request):
    global csv_writer, csv_file, recording, end_time

    ws = web.WebSocketResponse(protocols=["arduino"])
    await ws.prepare(request)
    clients.add(ws)

    csv_file = open(csv_filename, mode="a", newline="")
    csv_writer = csv.writer(csv_file)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            now = time.time()
            if end_time and now > end_time and recording:
                print(" Temps écoulé. Enregistrement terminé.")
                recording = False
                csv_file.close()

            row = msg.data.strip().split(",")
            if len(row) < 7:
                continue

            try:
                values = list(map(float, row[1:7]))
                window.append(values)
                buffer.append(values)
            except:
                continue

            if recording and csv_writer:
                csv_writer.writerow(row)
                csv_file.flush()

            if len(buffer) >= WINDOW_SIZE:
                segment = buffer[-WINDOW_SIZE:]
                df_window = pd.DataFrame(segment, columns=["accel.x", "accel.y", "accel.z", "gyro.x", "gyro.y", "gyro.z"])
                df_window = filtre_passe_bas(df_window)
                feats = extraire_features(df_window)
                feats_scaled = scaler.transform(feats) if scaler else feats.values
                prediction = model.predict(feats_scaled)[0]

                #  Correction ici : convertir prediction en label texte
                label_str = "frisson" if prediction == 1 else "repos"
                prediction_buffer.append(label_str)
                label_to_send = "frisson" if prediction_buffer.count("frisson") >= 3 else "repos"
                print(f" Mouvement détecté (lissé) : {label_to_send}")

                if recording and csv_writer:
                    csv_writer.writerow(row + [label_to_send])
                    csv_file.flush()

                for client in clients.copy():
                    try:
                        await client.send_str(f"PREDICTION:{label_to_send}")
                    except:
                        clients.discard(client)

            for client in clients.copy():
                if client != ws:
                    try:
                        await client.send_str(msg.data)
                    except:
                        clients.discard(client)

    clients.discard(ws)
    return ws

# === HTML handler ===
async def index_handler(request):
    return web.FileResponse('./www/index.html')

# === Lancer le serveur ===
app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    print("\n🚀 Serveur en ligne : http://localhost:8000")
    web.run_app(app, host='0.0.0.0', port=8000)
