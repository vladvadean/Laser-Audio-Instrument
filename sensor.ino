int sensorValue = 0;

void setup() {
  pinMode(A0, INPUT);
  Serial.begin(115200);
}

void loop() {
  sensorValue = analogRead(A0);

  // Send sensor data and timestamp as binary data
  Serial.println(sensorValue);
}
