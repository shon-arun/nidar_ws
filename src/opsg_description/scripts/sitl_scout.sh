#!/bin/bash

echo "🚀 [OpSG] Initiating Pre-Flight Sequence..."

WS_DIR=~/nidar_ws
PX4_DIR=~/PX4-Autopilot

# 1. Tell Gazebo exactly where your 3D models live
export GZ_SIM_RESOURCE_PATH=$WS_DIR/src/opsg_description/models:$GZ_SIM_RESOURCE_PATH

# 2. Inject the master airframe into PX4 temporarily
echo "⚙️  Injecting custom airframe into PX4..."
cp $WS_DIR/src/opsg_description/config/4050_gz_scout_drone $PX4_DIR/ROMFS/px4fmu_common/init.d-posix/airframes/

# 3. Wipe old EEPROM memory to prevent NaN matrix crashes (Why are we even doing this??)
echo "🧹 Wiping old parameters..."
find $WS_DIR $PX4_DIR -name "parameters*.bson" -type f -delete 2>/dev/null

# 4. Force PX4 to boot our specific drone
export PX4_SIM_MODEL=scout_drone
export PX4_SYS_AUTOSTART=4050

# 5. Launch Simulation
echo "🚁 Starting PX4 and Gazebo..."
cd $PX4_DIR
make px4_sitl gz_scout_drone