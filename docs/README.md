## Camera Comparison Table

| Camera Model | Sensor Size / MP | Shutter Type | Frame Rate | Weight (g) | Interface |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Sony RX0 II** | 1.0-inch / 15.3 MP | Anti-distortion (Global-like) | 4K @ 30fps | 132g | Micro HDMI / WiFi |
| **Raspberry Pi Cam V3** | 1/2.8-inch / 12 MP | Rolling Shutter | 1080p @ 50fps | 3g | MIPI CSI-2 |
| **OAK-D Lite** | 1/3.1-inch / 13 MP | Rolling Shutter | 4K @ 60fps | 61g | USB-C |
| **Intel RealSense D435i** | 2 MP (RGB) | Global Shutter | 1080p @ 30fps | 72g | USB-C 3.0 |

### Justification of Camera Choice

**Selected Camera: Raspberry Pi Camera Module 3 (Wide)**

**Engineering Trade-off (Expensiiev!!):** The Sony RX0 II.

Scanning 30 hectares requires a delicate balance of high-resolution imagery and extreme weight savings to maximize flight time while being cheap compared to well, Sony RX0. The Pi Cam V3 weighs a mere 3 grams, completely minimizing payload strain on the drone's thrust-to-weight ratio. 

### The Scanning Process

To effectively map the 30-hectare area, the drone will execute an automated **lawnmowertrajectory**. 
* **Flight Altitude:** ~50 meters. This ensures safe obstacle clearance, hopefully while maintaining a high-quality Ground Sample Distance (GSD).
* **Image Overlap (Not final, to be decided):** The mission will be programmed with a **70% frontal and 60% side overlap**.

## Motor Comparison Table

| Motor Model | KV Rating | Propeller | Max Thrust | Max Current | Efficiency (Hover) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Brotherhobby Tornado T5 3115** | 900KV | 9-inch (9045) | ~2800g | 55A (6S) | ~6.5 g/W |
| **T-Motor F90 2806.5** | 1300KV | 7-inch (7040) | ~2100g | 48A (6S) | ~5.8 g/W |
| **EMAX Eco II 2807** | 1300KV | 7-inch (7040) | ~1950g | 46A (6S) | ~5.5 g/W |

### ESC Comparison Table

| ESC Model | Continuous Current | Burst Current | Input Voltage | Protocol |
| :--- | :---: | :---: | :---: | :--- |
| **Hobbywing XRotor Micro 60A** | 60A | 80A | 3-6S | DShot1200 / BLHeli_32 |
| **T-Motor F55A Pro II** | 55A | 75A | 3-6S | DShot1200 / BLHeli_32 |
| **SpeedyBee 50A BLS** | 50A | 55A | 3-6S | DShot600 / BLHeli_S |

### Justification of Motor + ESC Combination

**Selected Combination: Brotherhobby Tornado T5 3115 (900KV) + Hobbywing XRotor Micro 60A 4-in-1 ESC**

**Why this fits the mission(probably):**
* **Motor (The Tornado T5 3115):** Scanning a 30-hectare area requires extended, stable flight times. The 3115 is a high-torque stator designed to effortlessly swing large 8 to 9-inch propellers. By pairing the 900KV variant with a 6S LiPo battery, the drone achieves exceptional grams-per-watt (g/W) efficiency at lower RPMs. 
* **ESC (Hobbywing XRotor 60A):** A massive 3115 stator generates incredible torque, but it also pulls significant amperage. At 100% throttle, this motor can draw upwards of 55 Amps. The SpeedyBee 50A would bottleneck the motor and risk blowing a MOSFET. The Hobbywing XRotor 60A provides a safe 5A continuous headroom (with an 80A burst rating) over the motor's absolute maximum draw.

## Propeller Selection
**Selected Propeller: HQProp MacroQuad 9050 (9-inch diameter, 5.0 pitch)**

* **Diameter & Pitch:** 9-inch diameter with a 5.0 pitch.
* **Material:** Carbon-Reinforced Nylon.
* **Thrust & Efficiency Reasoning:** The 9-inch propeller is the mathematical sweet spot for the Tornado T5 3115 (900KV) motor. A 7-inch prop would be under-propped and inefficient, while a 10-inch prop would over-draw current and risk burning out the 60A ESCs. The 9050 provides exceptional lift efficiency (~6.5 g/W at hover), maximizing flight time for the 30-hectare grid scan. The carbon-reinforced material ensures the blade remains stiff under heavy loads, preventing thrust loss from blade-flattening.

## Core Electronics Components

| Component | Example Model | Purpose + Specs Justification |
| :--- | :--- | :--- |
| **Flight Controller** | Holybro Pixhawk 6C | Native PX4 integration. Features triple-redundant IMUs and isolated vibration damping, which is critical for maintaining stable flight during autonomous ROS 2 waypoint navigation. |
| **GPS Module(maybe)** | Holybro Micro M9N GPS | Utilizes the u-blox M9N receiver for concurrent reception of 4 GNSS systems. Provides highly accurate spatial data essential for precise lawnmower grid execution and geotagging detected humans. |
| **Telemetry Module(Not sure)** | Holybro SiK Radio V3 (915MHz) | Provides a dedicated, long-range (up to 300mW) telemetry link to the QGroundControl base station (maybe), ensuring continuous heartbeat monitoring independent of the companion computer's network. |
| **Onboard Computer** | Raspberry Pi 4 Model B (8GB) | Acts as the ROS 2 orchestrator. Handles the Micro XRCE-DDS bridge, interfaces directly with the lightweight Pi Cam V3 via MIPI, and processes the YOLO human detection models. |
| **Power Module** | Holybro PM02 V3 | Acts as the Power Distribution Board (PDB). Safely steps down the 6S (22.2V) flight battery voltage to a clean 5V to continuously power the Pixhawk, GPS, and Raspberry Pi without browning out. |

## Battery Specification
**Selected Battery: Custom 6S2P 21700 Lithium-Ion Pack (Molicel P42A cells)**

### Parameter Evaluation & Justification

* **LiPo vs Li-Ion:** For a 30-hectare mapping mission, endurance is the primary metric. Lithium-Ion (Li-Ion) cells possess a significantly higher energy density (Watt-hours per kilogram) compared to Lithium Polymer (LiPo) cells. 
* **Cell Configuration (6S / 22.2V):** A 6-cell series (6S) configuration provides a nominal voltage of 22.2V. This is mathematically paired with our Tornado T5 3115 (900KV) motors. Running a low-KV motor at a higher voltage is the standard engineering practice to achieve maximum efficiency.
* **Capacity:** Using Molicel P42A 21700 cells, each cell holds 4200mAh. In a 2P configuration, the total pack capacity is **8400mAh**. 
* **Discharge Rating:** A single Molicel P42A cell has a continuous discharge rating of 45A. Because the pack is wired in 2P, the maximum continuous discharge is **90 Amps**. This provides an incredibly safe electrical buffer, easily covering the combined hover current of the motors without causing voltage sag.
* **Total Power Calculation:** * Nominal Voltage: 22.2V
  * Capacity: 8.4 Ah
  * Total Energy: **~186.4 Watt-hours (Wh)**
  * *Reasoning:* At an estimated cruising draw of 30-40 Amps, this 186Wh reserve provides ample flight time to easily clear the 30-hectare grid without requiring a mid-mission battery swap. Still leaving room for adding more components on to the drone.
 
## Flight Time Estimation
Based on our previous hardware selections, we can calculate the exact mission endurance. 

* **Battery Capacity:** 8.4 Ah (from the 6S2P 8400mAh Li-Ion pack)
* **Estimated Cruising Current Draw:** ~18 Amps (total draw for four Tornado T5 3115 motors cruising at 6 m/s with 9050 props and payload)

**Formula:**
`Flight time (hours) = (Battery capacity × 0.8) / current draw`

**Calculation:**
* **Usable Capacity:** 8.4 Ah × 0.8 = 6.72 Ah
* **Flight Time (hours):** 6.72 Ah / 18 A ≈ 0.373 hours
* **Flight Time (minutes):** 0.373 hours × 60 = **~22.4 minutes**

### Verification: Can 30 Hectares be Scanned in One Flight?

**Conclusion: Yes.**

**The Math (Photogrammetry Flight Plan):**
* **Total Area:** 30 hectares = 300,000 m².
* **Camera Swath Width:** Flying at a 50m altitude with the Pi Cam V3 Wide (120° FOV), the camera captures a massive footprint. Factoring in a 60% side-overlap, the effective distance between parallel flight lines (track spacing) is roughly 60 meters.
* **Speed & Coverage:** Cruising at a conservative 6 m/s, the drone covers 360 square meters per second (6m × 60m).
* **Grid Scan Time:** 300,000 m² / 360 m²/s = 833 seconds (~13.9 minutes).
* **Final Analysis:** Factoring in 2 to 3 minutes (probably) for takeoff, landing, and turns between grid lines, the total mission duration is roughly **17 minutes**. With a calculated flight time of **22.4 minutes**, the drone can complete the scan with over 5 minutes of emergency reserve power remaining.
