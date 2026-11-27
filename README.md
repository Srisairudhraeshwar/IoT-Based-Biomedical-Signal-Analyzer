# IoT-Based Biomedical Signal Analyzer

An embedded IoT system designed to acquire, process, and stream real-time physiological signals—specifically Electrocardiogram (ECG) waveforms and Blood Oxygen Saturation (SpO2/Heart Rate)—using an **ESP32 microcontroller**, an **AD8232 ECG sensor**, and a **MAX30102 optical sensor**. Telemetry data is transmitted over serial/Wi-Fi to a custom **Python desktop GUI** for real-time visualization and monitoring.

---

## Key Features
* **Dual-Sensor Physiological Acquisition:** Simultaneously interfaces with an AD8232 single-lead heart rate monitor (ECG) and a MAX30102 pulse oximetry sensor (SpO2 & BPM).
* **ESP32 Core Processing:** Handles high-speed analog-to-digital sampling, I2C communication, and wireless/serial data packaging.
* **Custom Python Monitoring UI:** A desktop graphical interface built to plot live biosignals, track vital statistics, and log telemetry data.
* **Robust Signal Filtering:** Implements baseline wander removal and noise filtering techniques in firmware to ensure clean waveform representation on the display.

---

## Hardware & Software Stack
* **Microcontroller:** ESP32 DevKit V1 (Wi-Fi/Bluetooth enabled SoC)
* **Biosensors:** 
  * AD8232 ECG Analog Front-End (Heart Monitor)
  * MAX30102 High-Sensitivity Pulse Oximeter & Heart-Rate Sensor (I2C)
* **Communication:** UART Serial / Wi-Fi UDP-TCP Telemetry
* **IDE & Toolchain:** Arduino IDE / ESP-IDF, Python 3 (`tkinter`, `matplotlib`, `pyserial`)

---

## Pinout & Wiring Connections

| Component / Module | ESP32 Pin | Function / Description |
| :--- | :--- | :--- |
| **AD8232 OUT** | `GPIO 36 (VP / A0)` | Analog ECG waveform output |
| **AD8232 LO+ / LO-** | `GPIO 4`, `GPIO 5` | Lead-off detection digital pins |
| **MAX30102 SDA** | `GPIO 21` | I2C Serial Data |
| **MAX30102 SCL** | `GPIO 22` | I2C Serial Clock |
| **MAX30102 INT** | `GPIO 13` | Sensor interrupt flag |
| **Power Bus** | `3.3V / GND` | Regulated power supply with common ground |

---

## Repository Structure
* `firmware/esp32_biomedical.ino` – ESP32 C++ firmware for AD8232 sampling, MAX30102 I2C configuration, and serial/Wi-Fi data streaming
* `gui/biomedical_dashboard.py` – Python desktop application for real-time plotting and vital sign monitoring
