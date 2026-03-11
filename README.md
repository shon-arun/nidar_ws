# Operation Sky Guardian (OpSG) 

## Overview
This repository contains the ROS2 workspace, system architecture, and mechanical designs for Operation Sky Guardian. The project is based on the NIDAR disaster management problem statement: designing and deploying autonomous drones to locate survivors and deliver essential supplies in a flooded coastal town.

## System Architecture
The mission utilizes a multi-robot system consisting of two specialized vehicles:
* **Scout Drone:** Engineered to autonomously scan a 30-hectare area, utilize YOLO for human detection, geotag survivors, and stream real-time video.
* **Delivery Drone:** Designed to receive coordinates and autonomously navigate to drop up to ten 200g survival kits using a custom mechanical release system.

## Repository Structure
* `src/`: Contains all ROS2 packages for waypoint navigation, perception (YOLO), and multi-drone mission autonomy.
* `cad/`: Contains the frame architectures, payload release mechanisms, and manufacturing drawings.
* `docs/`: Contains mission requirement analysis, electronics wiring diagrams, and component justifications.

## Build Instructions
1. Clone this repository.
2. Navigate to the workspace root: `cd nidar_ws`
3. Build the packages: `colcon build`
4. Source the environment: `source install/setup.bash`