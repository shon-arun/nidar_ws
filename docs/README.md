### Camera Comparison Table

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

### Motor Comparison Table

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
