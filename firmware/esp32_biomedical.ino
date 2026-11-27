#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30102 particleSensor;

// Pin Definitions for AD8232 ECG Sensor
const int ECG_OUTPUT = 36; // VP (A0)
const int LOC_PLUS   = 4;  // Lead-off detection +
const int LOC_MINUS  = 5;  // Lead-off detection -

// Timing for sampling rate control
unsigned long lastSampleTime = 0;
const int sampleInterval = 10; // ~100 Hz sampling rate for ECG

void setup() {
  Serial.begin(115200);
  
  // Initialize ECG Pins
  pinMode(LOC_PLUS, INPUT);
  pinMode(LOC_MINUS, INPUT);
  pinMode(ECG_OUTPUT, INPUT);

  // Initialize MAX30102 Sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found. Please check wiring/power!");
    while (1);
  }

  // Setup sensor with default configuration for SpO2/HR
  particleSensor.setup(); // Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); // Turn Red LED to low to indicate running
  particleSensor.setPulseAmplitudeGreen(0);  // Disable unused green LED

  Serial.println("--- Biomedical Signal Analyzer Initialized ---");
}

void loop() {
  // 1. Check Lead-Off Status for AD8232
  if ((digitalRead(LOC_PLUS) == 1) || (digitalRead(LOC_MINUS) == 1)) {
    // Leads are detached
    Serial.println("ECG_STATUS: Leads Off");
  } else {
    // 2. Sample ECG at ~100Hz
    if (millis() - lastSampleTime >= sampleInterval) {
      lastSampleTime = millis();
      int ecgValue = analogRead(ECG_OUTPUT);

      // 3. Read MAX30102 IR/Red values for heart rate / SpO2 estimation
      long irValue = particleSensor.getIR();

      // Format output string for Python GUI: "ECG:<val>,IR:<val>"
      Serial.print("ECG:");
      Serial.print(ecgValue);
      Serial.print(",IR:");
      Serial.println(irValue);
    }
  }
}
