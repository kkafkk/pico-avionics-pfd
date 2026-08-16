# 🛩️ RP2040 Primary Flight Display (Artificial Horizon)
A real-time digital avionics horizon and Primary Flight Display (PFD) running on a **Raspberry Pi Pico (RP2040)** using **MicroPython**. 

The system reads 6-DoF inertial motion data from an **MPU-6050** IMU, calculates pitch and roll angles, and renders a dynamic artificial horizon with an aircraft crosshair, ground shading, and stall-warning LED indicators on an **SSD1306 OLED** display.

## 📸 Showcase

### Demo Video
https://github.com/user-attachments/assets/9a5ac9d3-0c27-4f7b-96cf-2140ffe8367e


### Hardware Assembly & Wiring
<img width="1185" height="1280" alt="image" src="https://github.com/user-attachments/assets/16d9e067-17e6-44af-abc8-f1a704b246b7" />
*Current breadboard prototype.*

<img width="873" height="464" alt="image" src="https://github.com/user-attachments/assets/ee6d1cfe-3443-4b1c-8276-93fb859e4041" />
*Connection schematic showcasing the dual-bus I2C architecture.*

## ✨ Features

- **Dual-Bus I2C Architecture:** Utilizes both independent hardware I2C controllers (`I2C0` and `I2C1`) on the RP2040 to prevent bus congestion and frame drops between the IMU and the display.
- **Dynamic Graphical Horizon:** Renders real-time ground shading, pitch ladder bars, roll tilt, and a fixed aircraft reference symbol.
- **Stall / Bank Angle Warning:** Hardware LED status indicators and on-screen HUD alerts when bank or pitch angles exceed critical flight envelopes ($\pm 30^\circ$).
- **Optimized Frame Loop:** Lightweight geometry rendering in pure MicroPython maintaining a steady and smooth refresh rate.

---

## 🛠️ Hardware & Pinout

| Component | Pin / Signal | Raspberry Pi Pico Pin | Pin Description |
| :--- | :--- | :--- | :--- |
| **MPU-6050 (IMU)** | `SDA` | **GP4** | I2C0 SDA (Physical Pin 6) |
| | `SCL` | **GP5** | I2C0 SCL (Physical Pin 7) |
| | `VCC` | **3V3(OUT)** | 3.3V Power (Physical Pin 36) |
| | `GND` | **GND** | Ground (Physical Pin 38) |
| **SSD1306 (OLED)**| `SDA` | **GP2** | I2C1 SDA (Physical Pin 4) |
| | `SCK / SCL` | **GP3** | I2C1 SCL (Physical Pin 5) |
| | `VDD / VCC` | **3V3(OUT)** | 3.3V Power (Physical Pin 36) |
| | `GND` | **GND** | Ground (Physical Pin 38) |
| **Status LEDs** | Green LED | **GP14** | Normal Attitude Indicator |
| | Red LED | **GP15** | Stall / Excessive Bank Warning |

*Note: LEDs require 220Ω current-limiting resistors connected to GND.*

---

## 📂 Project Structure

To run this project, you need the main script and the hardware drivers (libraries). 

```text
├── docs/
│   ├── photo.jpg        # Assembly photo
│   └── schematic.png    # Circuit schematic
├── main.py              # Main avionics loop and rendering engine
├── mpu6050.py           # MPU-6050 MicroPython driver
├── ssd1306.py           # SSD1306 MicroPython framebuf driver
└── README.md
