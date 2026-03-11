# Operation Sky Guardian (OpSG) 

## Overview
This repository contains the ROS2 workspace, system architecture, and mechanical designs for Operation Sky Guardian. The project is based on the NIDAR disaster management problem statement: designing and deploying autonomous drones to locate survivors and deliver essential supplies in a flooded coastal town.

## System Architecture
The mission utilizes a multi-robot system consisting of two specialized vehicles:
* **Scout Drone:** Engineered to autonomously scan a 30-hectare area, utilize YOLO for human detection, geotag survivors, and stream real-time video.
* **Delivery Drone:** Designed to receive coordinates and autonomously navigate to drop up to ten 200g survival kits using a custom mechanical release system.

## Workspace Structure

```text
nidar_ws/
├── cad/                 # Frame architectures, payload release mechanisms, and drawings
├── docs/                # Mission requirement analysis and electronics wiring diagrams
├── src/                 # ROS2 workspace source directory
│   ├── opsg_core/       # Core flight control, waypoint navigation, and basic ROS2 communication
│   ├── opsg_perception/ # Camera sensor integration, cv_bridge conversions, and YOLO human detection
│   ├── opsg_mission/    # High-level multi-drone spawning, autonomous workflow, and independent control
│   ├── opsg_interfaces/ # Custom ROS2 messages, services, and actions for inter-drone communication
│   └── opsg_description/# URDF models, 3D meshes, and Gazebo simulation environments
├── .gitignore           # Git ignore configurations
└── README.md            # Project documentation
```

## Build Instructions
1. Clone this repository.
2. Navigate to the workspace root: `cd nidar_ws`
3. Build the packages: `colcon build`
4. Source the environment: `source install/setup.bash`