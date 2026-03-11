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

## ROS Task Progress Tracker (Week 0)

* **Task 1 - Create ROS2 workspace and packages**
  * ✅ Create workspace (`nidar_ws`)
  * ✅ Create Python ROS2 package
  * ✅ Run a simple node

* **Task 2 - Publishers and Subscribers**
  * ✅ 1 publisher (Publish `/drone_altitude`)
  * ✅ 1 subscriber (Subscribe `/target_altitude`)
  * ✅ Message exchange working

* **Task 3 - Services and Clients**
  * ✅ Working service request-response

* **Task 4 - ROS2 Launch Files**
  * ✅ Run publisher + subscriber using `ros2 launch drone_sim launch.py`
  
*(Further weeks will be tracked as the project progresses).*

## Development Standards: Conventional Commits
This repository adheres to the **Conventional Commits** standard to maintain a clean, readable, and machine-parsable version history. Commits should use the following prefixes:

* **`feat:`** A new feature (e.g., adding a new ROS node or CAD assembly).
* **`fix:`** A bug fix (e.g., correcting a typo in a launch file).
* **`docs:`** Documentation-only changes (e.g., updating this README).
* **`chore:`** Routine tasks, maintenance, or configuration changes that don't modify the source code.
* **`refactor:`** A code change that neither fixes a bug nor adds a feature.
* **`style:`** Changes that do not affect the meaning of the code (formatting, white-space, etc.).
* **`test:`** Adding missing tests or correcting existing tests.
* **`perf:`** A code change that improves performance.
* **`build:`** Changes that affect the build system or external dependencies.
* **`ci:`** Changes to CI/CD configuration files and scripts.

## Testing & Debugging

While the final system will utilize comprehensive launch files, individual nodes and communication streams can be tested using standard ROS2 CLI commands.

**1. Run an individual node:**
```bash
ros2 run opsg_core altitude_node
```

**2. List all currently running nodes:**
```bash
ros2 node list
```

**3. Get detailed information about a specific node:**
```bash
ros2 node info /altitude_node
```

**4. List all active communication topics:**
```bash
ros2 topic list
```

**5. Get detailed information about a specific topic:**
```bash
ros2 topic info /drone_altitude
```

**6. View real-time data being published to a topic:**
```bash
ros2 topic echo /drone_altitude
```

**7. Publish data to a topic manually:**
```bash
ros2 topic pub /target_altitude std_msgs/msg/Float32 "{data: 15.5}"
```

**8. Check the publishing rate (Hz) of a topic:**
```bash
ros2 topic hz /drone_altitude
```

**9. Inspect the structure of a message type:**
```bash
ros2 interface show std_msgs/msg/Float32
```

**10. List all active services:**
```bash
ros2 service list
```

**11. Call a service manually from the terminal:**
```bash
ros2 service call /arm_drone std_srvs/srv/SetBool "{data: true}"
```
```bash
ros2 service call /arm_drone std_srvs/srv/SetBool "{data: false}"
```