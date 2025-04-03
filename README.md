# 🩺 Smart Bracelet for Early Sepsis Detection (french version below)

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

### 1. Wiring Instructions

Connect the MPU6050 accelerometer/gyroscope sensor to your ESP32 using the following pin connections:

| MPU6050 Pin | Connect to ESP32 |
|-------------|-----------------|
| VCC         | 3.3V (or 5V, depending on your module – most support both) |
| GND         | GND             |
| SDA         | GPIO21 (default SDA) |
| SCL         | GPIO22 (default SCL) |

#### Notes

- Most MPU6050 modules support both 3.3V and 5V power supply
- The ESP32 uses GPIO21 and GPIO22 as the default I2C pins
- No additional pull-up resistors are required as the ESP32 has internal pull-ups

### 2. Configure the ESP32 Firmware

Edit the following lines in `basic_readings/basic_readings.ino` with your own network and server configuration:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* host = "YOUR_PC_IP_ADDRESS";
```

### 3. Upload the Firmware

- Plug the ESP32 into your computer using a USB cable.
- Open the `.ino` file in the Arduino IDE or PlatformIO.
- Press and hold the **BOOT** button on the ESP32.
- Click **Upload** to flash the script.
- Release the **BOOT** button when the upload starts.

### 4. Power the Bracelet

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

- Developed by Francesco Ali VENTURA, Allison STIOUI, Virgil TOUCHEBOEUF, Hugo AUPERIN
- In collaboration with Dr. Pierre Jacquet – Hôpital de Saint-Denis
- With the supervision of Nédra MELLOULI
- ESILV Engineering School – Pi² Project

# Version française

# 🩺 Bracelet Intelligent pour la Détection Précoce de Sepsis
Ce projet vise à construire un **système de détection portable** qui aide à identifier les indicateurs précoces de **sepsis** par la surveillance de mouvements anormaux tels que les tremblements ou les frissons. Il exploite les données de mouvement capturées par un microcontrôleur **ESP32** combiné à un capteur **MPU6050** et utilise un modèle **Support Vector Machine (SVM)** finement ajusté pour classifier les modèles de mouvement en temps réel.

## 🚀 Aperçu du Projet
- **Matériel**: ESP32 (microcontrôleur) + MPU6050 (accéléromètre + gyroscope)
- **Modèle**: Support Vector Machine (SVM), entraîné sur des données de mouvement personnalisées
- **Entrée**: Données de mouvement d'accéléromètre et de gyroscope
- **Sortie**: Classification en direct des mouvements (normal / suspect)
- **Cas d'utilisation**: Détection précoce de détresse neurologique potentielle liée au sepsis en milieu clinique

## 🧠 Détails d'Apprentissage Automatique
Le modèle de classification des mouvements a été entraîné à l'aide de données collectées et étiquetées sur mesure. Les données ont été segmentées en utilisant une approche de fenêtre glissante, et les caractéristiques ont été extraites à la fois dans les domaines temporel et fréquentiel (via FFT).

### ✅ Meilleure Configuration du Modèle
| Paramètre           | Valeur          |
|---------------------|-----------------|
| Fréquence de coupure| 20 Hz           |
| Taille de la fenêtre| 150 échantillons|
| Pas                 | 75 échantillons |
| FFT utilisée        | Oui             |
| Modèle              | SVM             |
| Métrique d'évaluation| precision_macro |
| Score moyen         | 0.9979          |
| Écart type          | 0.0043          |

*Les notebooks pour le traitement des données, l'extraction des caractéristiques et l'entraînement du modèle sont inclus dans ce dépôt.*

---

## 🔧 Comment Utiliser

### 1. Instructions de Câblage
Connectez le capteur accéléromètre/gyroscope MPU6050 à votre ESP32 en utilisant les connexions suivantes :

| Broche MPU6050 | Connexion à l'ESP32 |
|----------------|---------------------|
| VCC            | 3.3V (ou 5V, selon votre module - la plupart supportent les deux) |
| GND            | GND                 |
| SDA            | GPIO21 (SDA par défaut) |
| SCL            | GPIO22 (SCL par défaut) |

#### Remarques
- La plupart des modules MPU6050 supportent une alimentation de 3.3V et 5V
- L'ESP32 utilise les broches GPIO21 et GPIO22 comme broches I2C par défaut
- Aucune résistance de tirage (pull-up) supplémentaire n'est nécessaire car l'ESP32 possède des résistances de tirage internes

### 2. Configurer le Firmware ESP32
Modifiez les lignes suivantes dans `basic_readings/basic_readings.ino` avec votre propre configuration réseau et serveur:
```cpp
const char* ssid = "NOM_DE_VOTRE_WIFI";
const char* password = "MOT_DE_PASSE_WIFI";
const char* host = "ADRESSE_IP_DE_VOTRE_PC";
```

### 3. Téléverser le Firmware
- Branchez l'ESP32 à votre ordinateur à l'aide d'un câble USB.
- Ouvrez le fichier `.ino` dans l'IDE Arduino ou PlatformIO.
- Appuyez et maintenez le bouton **BOOT** sur l'ESP32.
- Cliquez sur **Téléverser** pour flasher le script.
- Relâchez le bouton **BOOT** lorsque le téléversement commence.

### 4. Alimenter le Bracelet
Vous pouvez alimenter le bracelet ESP32 via:
- Connexion USB à votre PC
- Une batterie externe
- N'importe quelle source d'alimentation USB 5V

---

### 4. Exécuter les Scripts de Détection ou de Collecte de Données
#### 🟢 Détection en Temps Réel
Pour commencer à détecter les mouvements anormaux en utilisant le modèle entraîné, exécutez:
```bash
python server.py
```
Ce script écoute les données provenant de l'ESP32 et classifie les mouvements entrants en temps réel.

## 🧪 Collecter des Données Étiquetées (pour améliorer le modèle)
```
python server_labeled.py
```
Utilisez ce script pour enregistrer des sessions de mouvements étiquetés (par exemple, repos, tremblement, rotation) et les ajouter à votre ensemble de données.

## 📁 Structure du Projet
```
Bracelet-Intelligent/
├── analyse_mouvements_sepsis.ipynb # Analyse Exploratoire des Données (EDA)
├── entrainement_modele.ipynb # Pipeline d'entraînement du modèle
├── EvaluationModelsEtParametres.ipynb # Test des hyperparamètres
├── basic_readings/
│   └── basic_readings.ino # Firmware ESP32
├── data/ # Ensembles de données de mouvements collectés
│   ├── frisson.csv
│   ├── repos.csv
│   └── ...
├── features_dataset.csv # Caractéristiques finales utilisées pour l'entraînement
├── modele_entraine.joblib # Modèle SVM entraîné
├── scaler.joblib # StandardScaler pour la normalisation des entrées
├── resultats/ # Sorties des serveurs
│   └── test2.csv
├── resultats_grid_search.csv # Évaluation du réglage des paramètres
├── server.py # Serveur de classification en temps réel
├── server_labeled.py # Serveur de collecte de données
├── www/
│   ├── index.html # Interface frontend GitHub Pages
│   └── 1.html
```

## 🤝 Remerciements
- Développé par Francesco Ali VENTURA, Allison STIOUI, Virgil TOUCHEBOEUF, Hugo AUPERIN
- En collaboration avec Dr. Pierre Jacquet – Hôpital de Saint-Denis
- Supervisé par Nédra MELLOULI
- École d'ingénierie ESILV – Projet Pi²
