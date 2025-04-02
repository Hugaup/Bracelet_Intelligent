#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const char* ssid = "X";
const char* password = "X";
const char* host = "X"; // IP de ton PC
const uint16_t port = 8080;

WebSocketsClient webSocket;
Adafruit_MPU6050 mpu;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  // (Pas utilisé ici, mais requis par la lib)
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // ESP32 SDA = 21, SCL = 22

  if (!mpu.begin()) {
    Serial.println("MPU6050 non détecté !");
    while (1);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_94_HZ);

  WiFi.begin(ssid, password);
  Serial.print("Connexion WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté à Wi-Fi !");
  Serial.println(WiFi.localIP());
  // Avant de démarrer la connexion
  webSocket.setExtraHeaders(nullptr);             // ← pour supprimer tout header type 'arduino'
  webSocket.begin(host, 8000, "/ws");
  webSocket.onEvent(webSocketEvent);

}

void loop() {
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  String data = String(millis()) + "," +
                String(accel.acceleration.x) + "," +
                String(accel.acceleration.y) + "," +
                String(accel.acceleration.z) + "," +
                String(gyro.gyro.x) + "," +
                String(gyro.gyro.y) + "," +
                String(gyro.gyro.z);

  webSocket.loop();
  webSocket.sendTXT(data); // Envoi au serveur

  delay(10); // 71.4 Hz réél probablement a cause des retards de transmissions 
}
