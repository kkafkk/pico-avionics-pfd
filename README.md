# ✈️ RP2040 Artificial Horizon (Primary Flight Display)
A real-time digital avionics horizon and Primary Flight Display (PFD) developed by [Katya (kkafkk)](https://github.com/kkafkk). Built using an **RP2040 Microcontroller** (Raspberry Pi Pico). 
The system reads 6-DoF inertial motion data from an **MPU-6050** IMU and renders a dynamic, stylized artificial horizon with stall-warning indicators on an **SSD1306 OLED** display.

## 🛠️ Hardware Stack
* **Microcontroller:** Raspberry Pi Pico (RP2040)
* **Display:** SSD1306 OLED (128x64, I2C)
* **Sensor:** MPU-6050 (6-DoF Accelerometer & Gyroscope, I2C)
* **Indicators:** 2x LEDs (Green, Red) with 220Ω current-limiting resistors
* **Power Supply:** 3.3V from RP2040 (via USB power bank or PC)

## 🏗️ System Architecture
```text
[ MPU-6050 IMU ] --(I2C0 / GP4, GP5)--> [ RP2040 Pico ] --(I2C1 / GP2, GP3)--> [ SSD1306 OLED ]
                                        (MicroPython)                          [ Status LEDs ] 
```
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

🚀 Quick Start
1. Setup RP2040 (Flight Computer)

2. Flash standard MicroPython firmware onto the RP2040 board.

3. Clone this repository to your local machine:
```bash
git clone [https://github.com/kkafkk/rp2040-avionics-pfd.git](https://github.com/kkafkk/rp2040-avionics-pfd.git)
cd rp2040-avionics-pfd
```
4. Connect the RP2040 to your computer via USB.

5. Using Thonny IDE or VS Code (with MicroPico), upload main.py, mpu6050.py, and ssd1306.py directly to the root directory of the Pico.

6. Wire the components: MPU-6050 to GP4/GP5, SSD1306 to GP2/GP3, and LEDs to GP14/GP15.

7. Restart the board (Ctrl + D) to launch the avionics system.

## ⚙️ Key Features & Tuning
Dual-Bus I2C Protocol: Completely eliminates hardware collisions by splitting the sensor and display onto independent hardware lines.

Math Optimization: Uses math.atan2 for robust 3D angle calculations, avoiding division-by-zero errors and gimbal lock.

Dynamic Ground Shading: Algorithmic checkerboard rendering under the horizon line for spatial awareness.

Stall Envelope Limits: Adjust the conditional if abs(pitch) > 30 or abs(roll) > 30: in main.py to change the angle at which the red warning LED and HUD alerts trigger.

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
```

## 💡Modularity & Low-Cost Architecture
One of the key advantages of this decoupled architecture is its **extreme flexibility and low cost**:

**Standalone Operation**: Unlike PC-dependent tracking systems, this PFD is a true embedded device. It requires no host computer once flashed and runs entirely off a standard USB power bank.
Ultra Budget-Friendly (~$10 total):
 **RP2040 Microcontroller**: ~$4
 **MPU-6050 IMU**: ~$2
 **SSD1306 OLED**: ~$3
 **LEDs, Resistors & Breadboard**: ~$1

**Adaptability**: The math and logic can be easily integrated into RC planes, drones, or robotics projects needing basic orientation awareness.

## 🛠️ Development Log & Engineering Challenges
During the design, assembly, and debugging phases, several hardware and software challenges were identified and solved:

1.**I2C Bus Collisions (The Dual-Bus Pivot)**:

  *Initial Plan*: Connect both the MPU-6050 and the SSD1306 OLED to a single shared I2C bus (I2C0), as is standard for many simple Arduino projects.

  *The Problem*: Pushing a 1024-byte video buffer to the OLED display at 400kHz collided with the continuous polling requests to the MPU-6050. This caused the RP2040's hardware I2C controller to freeze, resulting in [Errno 110] ETIMEDOUT and a totally unresponsive system.

  *Solution*: Redesigned the architecture to utilize the RP2040's dual hardware I2C blocks. MPU-6050 was isolated on I2C0, and the OLED was moved to I2C1. This completely eliminated packet collisions and allowed smooth, uninterrupted frame rendering.

2. **UI/UX Redesign: From Text to Graphical PFD**:

  *Initial Plan*: Display raw numerical data (Pitch and Roll degrees) with a basic horizontal line to verify sensor readings.

  *The Problem*: Raw numbers were functional but lacked the intuitive spatial awareness required for an actual avionics display. It didn't "feel" like a flight instrument.

  *Solution*: Completely overhauled the rendering engine to draw a full Primary Flight Display (PFD). Implemented trigonometric projections (math.sin, math.cos, math.tan) to dynamically rotate the horizon line, added pitch ladders (±15° bars), and designed a fixed aircraft crosshair to simulate a true 3D spatial environment on a 2D monochrome OLED.

3. **Rendering Performance & Fill Limits**:

  *Issue*: Drawing a solid block of pixels to represent the "ground" below the horizon line using standard MicroPython commands was too computationally heavy, dropping the framerate significantly.

  *Solution*: Implemented a math-driven alternating pixel step (checkerboard shading). By calculating the vertical step bounds and skipping redundant pixels (oled.pixel(x + (y % 4 == 0), y, 1)), the visual effect of a solid ground was achieved without sacrificing loop speed.

4. **Floating Wires & Hardware Jitter**:

  *Issue*: Using long, loose jumper wires for the MPU-6050 caused micro-disconnects on the SCL/SDA lines during physical movement, crashing the MicroPython script instantly with [Errno 5] EIO.

  *Solution*: The sensor was mounted directly flush into the breadboard for rigid contact. Added a try/except recovery loop to prevent the software from halting during temporary hardware disconnects.

## 👤 Author
Katya — @kkafkk

## 📝 License
This project is open-source and available under the MIT License.
