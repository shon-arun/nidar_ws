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
│   └── scout_drone/     # Onshape export configurations and staging for the scout drone
├── docs/                # Mission requirement analysis and electronics wiring diagrams
├── src/                 # ROS2 workspace source directory
│   ├── opsg_core/       # Core flight control, waypoint navigation, and basic ROS2 communication
│   ├── opsg_perception/ # Camera sensor integration, cv_bridge conversions, and YOLO human detection
│   ├── opsg_mission/    # High-level multi-drone spawning, autonomous workflow, and independent control
│   ├── opsg_interfaces/ # Custom ROS2 messages, services, and actions for inter-drone communication
│   └── opsg_description/# URDF models, 3D meshes, and Gazebo simulation environments
│       ├── meshes/      # 3D mesh files (.stl) categorized by drone (e.g., scout_drone/)
│       └── urdf/        # Unified Robot Description Format files (e.g., scout_drone.urdf)
├── .gitignore           # Git ignore configurations
└── README.md            # Project documentation
```

## Prerequisites & Installation Dependencies

Operation Sky Guardian relies on a modern, decoupled robotics stack. To replicate this environment, you must install the following core systems and dependencies.

### 1. Operating System & Core Middleware
* **Ubuntu Linux:** 24.04 LTS (Noble Numbat).
* **ROS 2 (Jazzy Jalisco):** The core communication framework. 
  * Follow the [Official ROS 2 Jazzy Installation Guide](https://docs.ros.org/en/jazzy/Installation.html).
  * *Pro-tip:* Installing the `ros-jazzy-desktop` meta-package automatically bundles `colcon` and the necessary workspace build tools, saving you from manually installing `ros-dev-tools`.

### 2. The Simulation Engine (Gazebo Harmonic)
Gazebo renders the 3D meshes, calculates collision physics, and applies gravity and thrust.
* Follow the [Official Gazebo Harmonic Installation Guide](https://gazebosim.org/docs/harmonic/install).
* Install the ROS-Gazebo bridge to sync the simulation clock and environment:
  ```bash
  sudo apt install ros-jazzy-ros-gz
  ```

### 3. The Flight Stack (PX4 Autopilot)
PX4 handles the drone's internal physics calculations, EKF (Estimator), and motor mixing.
* Clone the [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) repository.
* Run the included Ubuntu setup script to install necessary toolchains (ARM compilers, CMake, Python dependencies):
  ```bash
  bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
  ```

### 4. Inter-Process Communication (Micro XRCE-DDS)
PX4 uses internal `uORB` messaging, while ROS 2 uses `DDS`. The Micro XRCE-DDS Agent acts as the real-time translation layer.
* **Install the Agent globally:**
  ```bash
  git clone [https://github.com/eProsima/Micro-XRCE-DDS-Agent.git](https://github.com/eProsima/Micro-XRCE-DDS-Agent.git)
  cd Micro-XRCE-DDS-Agent
  mkdir build
  cd build
  cmake ..
  make
  sudo make install
  sudo ldconfig /usr/local/lib/
  ```
* **The Autonomy Dictionary (`px4_msgs`):** While not required to fly manually in Gazebo, you must clone `px4_msgs` into your ROS 2 `src/` directory to write autonomous nodes. Ensure the branch matches your PX4 version, then run `colcon build` so ROS 2 can generate the translation headers.

## Build Instructions
1. Clone this repository.
2. Navigate to the workspace root: `cd nidar_ws`
3. Build the packages: `colcon build`
4. Source the environment: `source install/setup.bash`

## ROS Task Progress Tracker (Week 0, 1)

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

* **Task 5 - Configure PX4 + Gazebo + ROS2 bridge**
  * ✅ drone visible in Gazebo
  * ✅ topics visible in ROS2

* **Task 6 - Autonomous Takeoff and Landing**
  Takeoff to
  * ⬜ 2m
  * ⬜ 5m
  * ⬜ 10m

* **Task 7 - Waypoint Navigation**
  * ✅ Waypoint control node
  * ✅ Trajectory following videos for square, triangle, figure 8
  
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

**12. Launching a launch file:**
```bash
ros2 launch opsg_description spawn_scout.launch.py
```
**Gazebo Harmonic SQLite Crash (`libspatialite.so.8: undefined symbol: sqlite3_enable_load_extension`)**
If Gazebo instantly crashes on launch with this error, it means a local Python environment (like Conda) is overriding the system's SQLite library. 
**Fix:** Force the system library to load first by prepending `LD_PRELOAD` to your launch command:
```bash
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libsqlite3.so.0 ros2 launch opsg_description spawn_scout.launch.py
```