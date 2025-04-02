# 🩺 Smart Bracelet for Early Sepsis Detection

This project aims to build a **wearable detection system** that helps identify early indicators of **sepsis** through the monitoring of abnormal movements such as tremors or chills. It leverages motion data captured by an **ESP32** microcontroller combined with an **MPU6050** sensor and uses a finely tuned **Support Vector Machine (SVM)** model to classify movement patterns in real time.

## 🚀 Project Overview

- **Hardware**: ESP32 (microcontroller) + MPU6050 (accelerometer + gyroscope)
- **Model**: Support Vector Machine (SVM), trained on custom movement data
- **Input**: Accelerometer & gyroscope motion data
- **Output**: Live classification of movement (normal / suspicious)
- **Use Case**: Early detection of potential neurological distress linked to sepsis in clinical settings

## 🧠 Machine Learning Details

The motion classification model was trained using custom-collected and labelled data. Data was segmented using a sliding window approach, and features were extracted both in time and frequency domains (via FFT).

### ✅ Best Model Configuration

| Parameter           | Value           |
|---------------------|-----------------|
| Cutoff frequency    | 20 Hz           |
| Window size         | 150 samples     |
| Stride              | 75 samples      |
| FFT used            | Yes             |
| Model               | SVM             |
| Scoring Metric      | precision_macro |
| Mean Score          | 0.9979          |
| Std Deviation       | 0.0043          |

_Notebooks for data processing, feature extraction, and model training are included in this repository._

---

## 🔧 How to Use

### 1. Configure the ESP32 Firmware

Edit the following lines in `basic_readings/basic_readings.ino` with your own network and server configuration:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* host = "YOUR_PC_IP_ADDRESS";
```

### 2. Upload the Firmware

- Plug the ESP32 into your computer using a USB cable.
- Open the `.ino` file in the Arduino IDE or PlatformIO.
- Press and hold the **BOOT** button on the ESP32.
- Click **Upload** to flash the script.
- Release the **BOOT** button when the upload starts.

### 3. Power the Bracelet

You can power the ESP32 bracelet via:

- USB connection to your PC
- A power bank
- Any 5V USB power source

---

### 4. Run the Detection or Data Collection Scripts

#### 🟢 Real-time Detection

To start detecting abnormal movements using the trained model, run:

```bash
python server.py
```

This script listens for data from the ESP32 and classifies incoming motion in real time.

## 🧪 Collect Labelled Data (to improve the model)

```
python server_labeled.py
```

Use this script to record labelled movement sessions (e.g., rest, tremor, rotation) and add them to your dataset.

## 📁 Project Structure

```
Bracelet-Intelligent/
├── analyse_mouvements_sepsis.ipynb # Exploratory Data Analysis (EDA)
├── entrainement_modele.ipynb # Model training pipeline
├── EvaluationModelsEtParametres.ipynb # Hyperparameter testing
├── basic_readings/
│   └── basic_readings.ino # ESP32 firmware
├── data/ # Collected movement datasets
│   ├── frisson.csv
│   ├── repos.csv
│   └── ...
├── features_dataset.csv # Final features used for training
├── modele_entraine.joblib # Trained SVM model
├── scaler.joblib # StandardScaler for input normalisation
├── resultats/ # Output from the servers
│   └── test2.csv
├── resultats_grid_search.csv # Evaluation of parameter tuning
├── server.py # Real-time classification server
├── server_labeled.py # Data collection server
├── www/
│   ├── index.html # GitHub Pages frontend
│   └── 1.html
```

## 🤝 Acknowledgements

Developed by Francesco Ali VENTURA, Allison STIOUI, Virgil TOUCHEBOEUF, Hugo AUPERIN
In collaboration with Dr. Pierre Jacquet – Hôpital de Saint-Denis
ESILV Engineering School – Pi² Project
