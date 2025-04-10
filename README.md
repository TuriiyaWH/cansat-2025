# CanSat Project – UK CanSat Competition 2025

This repository documents the CanSat project developed by **Team HPS1** at **Highams Park School** for the UK CanSat Competition 2025. The CanSat was designed to measure atmospheric conditions and flight dynamics during descent using a custom-built electronics system and multiple sensors.

---

## 🚀 Mission Overview

- **Primary Mission**: Measure atmospheric temperature and pressure during descent using a BMP280 sensor.
- **Secondary Mission**: Capture orientation (pitch, roll, yaw), acceleration, and GPS coordinates to analyze stability and flight path. Output data is used to generate a 3D animation of the descent.

---

## 🧠 My Contributions

- Developed embedded software for Raspberry Pi Pico to interface with:
  - BMP280 (pressure & temperature)
  - Adafruit Ultimate GPS (position)
  - BNO055 IMU (orientation)
  - RFM96W LoRa transceiver (telemetry)
  - SD card module (local logging)
- Supported hardware integration and soldering
- Processed and visualized data using Python and `matplotlib`
- Contributed to 3D animation using Blender by preparing and aligning sensor data

---

## 📊 Data Analysis

Visualizations from post-flight analysis:

<p align="center">
  <img src="Images/graphs/Pressure Vs Time.png" width="400">
  <img src="Images/graphs/Temperature Vs Time.png" width="400">
</p>

---

## 📂 Repo Structure

- `code/`: Embedded code and data parsing scripts
- `data/`: Raw and processed telemetry logs
- `images/`: Graphs, wiring diagrams, and build photos
- `animation/`: Blender-based 3D visualization of the descent
- `docs/`: Reports, design reviews, and reference materials

---

## 🛠️ Hardware Overview

- **Microcontroller**: Raspberry Pi Pico
- **Sensors**: BMP280 (pressure/temp), BNO055 (IMU), Adafruit Ultimate GPS
- **Radio**: RFM96W LoRa 433 MHz
- **Storage**: MicroSD card adapter
- **Shell**: 3D-printed PLA casing with internal shock protection

---

## 📅 Timeline

Key phases included:
- Prototyping and component testing
- Thermal and shock testing
- Flight operations and recovery
- Post-flight data analysis and visualization

---

## 🎥 3D Animation

[Flight Animation – Blender Render (Coming Soon)](animation/flight_animation.mp4)

---

## 📘 Documentation

- [Critical Design Review (PDF)](docs/Final_Report.pdf)
- [Launch Test Notes](docs/launch_notes.pdf)

---

## 📫 Contact

For questions, feel free to reach out via GitHub or [LinkedIn](#).

