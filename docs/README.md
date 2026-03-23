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
