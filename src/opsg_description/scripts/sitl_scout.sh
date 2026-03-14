#!/bin/bash
echo "🚀 Starting PX4 SITL with Custom Scout Drone..."

# Apply the SQLite crash fix
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libsqlite3.so.0

# Build and run our new custom airframe!
cd ~/PX4-Autopilot
make px4_sitl gz_scout_drone