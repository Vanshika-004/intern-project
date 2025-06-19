# Intern-project- Autonomous Navigation of 2WDD Robot using ROS 2, Gazebo, DWA, and SLAM

## Overview

This project demonstrates the complete simulation of a 2-wheel differential drive robot using ROS 2 and Gazebo. It involves robot modeling, obstacle-filled environment simulation, real-time path planning, and SLAM-based mapping-all within a ROS 2 framework. The goal is to enable the robot to autonomously navigate through an unknown environment using onboard sensors and planning algorithms.

### Robot & Simulation Setup

The robot is modeled using URDF and simulated in Gazebo, configured with a differential drive controller for motion control. A virtual environment is populated with static obstacles. The robot moves based on standard differential drive kinematics, where the linear and angular velocity commands are mapped to individual wheel velocities.

### Obstacle Handling and Planning

To enable autonomous movement, the Dynamic Window Approach (DWA) planner is integrated as the local planner within the ROS 2 Navigation Stack. DWA generates velocity commands in real-time, taking into account dynamic constraints and the local obstacle map to ensure smooth and safe trajectory planning.

### SLAM & Localization

The robot is equipped with a simulated 2D LIDAR, and SLAM Toolbox is used to perform Simultaneous Localization and Mapping. As the robot explores, it builds a map of the environment while localizing itself in it-enabling robust navigation even without prior knowledge of the map.

### Costmap Integration

Navigation is supported by a layered costmap that fuses data from the LIDAR to represent the world around the robot. It includes:
- Obstacle layer: for marking known obstacles
- Inflation layer: for maintaining safe distances from obstacles
- Global and local costmaps: for path planning and reactive navigation

### Core Concepts Demonstrated

- ROS 2-based robot simulation and control  
- Differential drive kinematics  
- Real-time planning with DWA  
- 2D SLAM with LIDAR  
- Dynamic costmap management

---
UPDATES
---
## ROS 2 Installation Verification

### ROS 2 Installed Successfully

The ROS 2 Humble distribution was successfully installed on Ubuntu. Running the `ros2` command confirms the CLI is active and available:

![image](https://github.com/user-attachments/assets/b57a7974-ae50-463a-9c3b-dd863f62310c)

---

### Testing ros2 installation via Turtlesim

To validate the ROS 2 installation, the `turtlesim` demo package was launched using the following commands:

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```
Keyboard control was used to draw a pattern on the turtlesim canvas.

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtle_teleop_key
```
ROS nodes were confirmed using the following:

```bash
source /opt/ros/humble/setup.bash
ros2 node list
```
![image](https://github.com/user-attachments/assets/5a87a0c2-385a-4e98-aa21-86cc4f4c8b3d)


<h3 align="center">Turtlesim working</h3>

<div align="center">
  <img src="https://github.com/user-attachments/assets/c732f61c-2e3b-48a8-b4d6-7b1476401236" alt="Turtlesim Demo" width="300"/>
</div>

---

# Differential Drive Robot (2WD) - ROS 2 + Ignition Gazebo

This project implements a simple 2-wheel differential drive robot in ROS 2 Humble and simulates it using Ignition Gazebo. The robot includes a main chassis, two wheels for movement, a passive caster wheel, and standard Gazebo plugins for control and odometry.

---

## Robot Description (URDF Overview)

### Base Link
- Shape: Box
- Dimensions: 0.5 x 0.3 x 0.15 meters
- Material: White

### Left & Right Wheels
- Shape: Cylinder
- Radius: 0.1 m
- Length: 0.05 m
- Mass: 0.5 kg each
- Material: Blue
- Inertia: Diagonal, Ixx = Iyy = Izz = 0.01

### Caster Wheel
- Shape: Sphere
- Radius: 0.05 m
- Mass: 0.1 kg
- Joint Type: Fixed (non-driven)

---

## Gazebo Plugins Configuration

### Differential Drive Plugin
- Type: gz::sim::systems::DiffDrive
- Left Joint: left_wheel_joint
- Right Joint: right_wheel_joint
- Wheel Separation: 0.35 m
- Wheel Diameter: 0.2 m
- Max Torque: 20
- Max Acceleration: 1.0
- Topics:
  - /cmd_vel (velocity commands)
  - /odom (odometry)
- TF Publishing: Enabled

### Joint State Publisher Plugin
- Joints: left_wheel_joint, right_wheel_joint
- Update Rate: 30 Hz
- Topic: /joint_states

---

## Launch Instructions

![image](https://github.com/user-attachments/assets/1cfe73f0-764f-40eb-a86c-1d6111801a8e)


### Terminal 1: Build and Launch Gazebo

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
ros2 launch ignition_robot gazebo.launch.py
```

### Terminal 2: Run Teleop Keyboard Node

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Use the keyboard to control the robot. The teleop node publishes velocity commands to /cmd_vel.

### Demo Video: 2WD Differential Drive Robot in Ignition Gazebo


[Click to watch the demo](./ignition_robot/2WDD%20Demo%20Video.mp4)

---
## Updates: 1st June – 3rd June

### Workspace and Build Issues

**colcon: command not found**  
Installed missing ROS tools and set environment variables.

**ament_cmake build failed**  
Installed missing dependencies via apt.

**Duplicate or incorrect launch file names**  
Renamed and cleaned up files like `robot.launch.py`.

**New packages not detected during build**  
Cleared build folders and used:  
`colcon build --packages-select <package_name>`

---

### Package/Launch Issues

**ros2: command not found**  
Fixed by sourcing ROS 2 setup file.

**Package 'maze_runner' not found**  
Resolved by switching to and sourcing the correct workspace.

**Launch file missing or in wrong path**  
Found file using `find` and updated launch command accordingly.

---

### Gazebo Simulation Issues

**Model not moving despite cmd_vel output**  
Checked controller plugins and remappings.

**Camera plugin UI errors in Ignition Gazebo**  
Removed or replaced plugins causing QML issues.

**URDF/Xacro errors**  
Fixed malformed XML and added missing `xacro` tags.

---

### Navigation & SLAM Issues

**DWB planner not working**  
Integrated `dwb_controller` plugin in Nav2 config.

**SLAM or Nav2 not launching**  
Fixed by setting `use_sim_time` and updating map/controller configs.

---

### System & Dependency Issues

**dpkg interrupted**  
Resolved by running:  
`sudo dpkg --configure -a`

**ROS GPG key warning**  
Fixed by updating to the new keyring format.

Here's a simplified and clearly formatted version of your resolved ROS 2 errors and fixes in **Markdown** format, ready to be added to your `README.md`:

---
## Updates: 4th June – 6th June

## Resolved Issues in ROS 2 Workspace Setup

### 1. Package Not Found (`maze_runner`)

* **Cause**: Workspace was not sourced or built.
* **Fix**: Ran `colcon build` and sourced `install/setup.bash`.

### 2. Wrong Workspace Being Used

* **Cause**: ROS 2 was using `ros2_ws` but package was in `ros2_wsl`.
* **Fix**: Sourced the correct workspace (`ros2_wsl`) or moved the package to `ros2_ws`.

### 3. `ros2` Command Not Found

* **Cause**: ROS 2 environment was not sourced.
* **Fix**: Ran:

  ```bash
  source /opt/ros/humble/setup.bash
  ```

### 4. Package Not Listed in `ros2 pkg list`

* **Cause**: Build incomplete or workspace not sourced.
* **Fix**: Ensured build completed successfully and ran:

  ```bash
  source install/setup.bash
  ```

### 5. CMake Warnings: Unused CATKIN Variables

* **Cause**: Leftover or irrelevant Catkin variables in CMake files.
* **Fix**: Ignored, as these are non-fatal and do not affect ROS 2 functionality.

### 6. Missing Package Directories (e.g., `install/maze_runner`)

* **Cause**: Partial or failed build.
* **Fix**: Cleaned and rebuilt the workspace:

  ```bash
  rm -rf build/ install/ log/
  colcon build
  ```

### 7. Incorrect `AMENT_PREFIX_PATH`

* **Cause**: Workspace was not sourced properly.
* **Fix**: Verified the path and sourced the correct file:

  ```bash
  source install/setup.bash
  ```
---
## Updates: 7th June – 10th June

### Workspace Path Warnings
- AMENT_PREFIX_PATH / CMAKE_PREFIX_PATH warnings  
- Resolved by cleaning `build/`, `install/`, and `log/` directories, then rebuilding the workspace.

### Robot Not Visible in Gazebo
- Model spawned but not displayed  
- Fixed robot description and plugin paths.

### Missing Joint Error
- Joint `[left_wheel_joint]` not found  
- Corrected joint definitions in the URDF file.

### Laser Plugin Not Found
- `libgazebo_ros_laser.so` missing  
- Installed missing package: `ros-humble-gazebo-ros-pkgs`.

### Robot Description Parsing Error
- Unable to parse `robot_description` as YAML  
- Wrapped robot description with the correct launch parameter type:  
  ```python
  value_type=str
  ```
  
### Gazebo Port in Use

* Unable to start server due to address already in use
* Resolved by killing existing Gazebo instances:

  ```bash
  pkill -f gazebo
  ```

### Duplicate Entity Spawn

* Entity `[diff2]` already exists
* Restarted Gazebo or used a unique entity name.

---
## Updates: 10th June –13th June

### ROS 2 Simulation – Error Summary and Fixes

### Resolved Issues

#### Incorrect Variable Usage in Launch File
- **Issue**: Used undefined variable `pkg_share`.
- **Fix**: Corrected to consistent usage of `pkg_share`.

#### Invalid Xacro Path
- **Issue**: Path pointed to `src/install/...`, which doesn't exist.
- **Fix**: Updated to reference the correct source path or used `get_package_share_directory()`.

#### Python `xml.parsers` Error
- **Issue**: `AttributeError: module 'xml' has no attribute 'parsers'`
- **Fix**: No conflicting `xml.py` found in workspace. Likely resolved after fixing the Xacro path.

---

### Current Issues

#### `ros2_control_node` Crash
- **Symptom**: Crash dialog: "`ros2_control_node` has stopped unexpectedly"
- **Possible Causes**: Incorrect joint interfaces or malformed controller YAML.

#### Gazebo Freezing
- **Symptom**: "Gazebo is not responding" during world load.
- **Possible Causes**: Plugin or controller waiting on unavailable hardware.

#### Path Confusion Between `src/` and `install/`
- **Observation**: Multiple instances of launch files in both `src/` and `install/`.
- **Impact**: Can lead to unexpected file execution.

---

### Next Steps

- Validate URDF and joints using a minimal test launch.
- Review and test `diff_drive_controller.yaml`.
- Temporarily disable `ros2_control_node` to isolate the crash source.
- Compare with a working example of `ros2_control` for differential drive robots.

---
## Updates: 14th June –18th June

### 1. TF Transformation Error
**Symptoms**:  
- `[dwa_planner] TF error: name 'v' is not defined`  
- Robot failing to move despite receiving laser scans  

**Cause**:  
- Python `NameError` in TF lookup exception handling (typo where `e` was mistyped as `v`)

**Resolution**:  
Fixed exception handling in TF transformation code:
```python
try:
    transform = self.tf_buffer.lookup_transform(...)
except (tf2_ros.LookupException, 
        tf2_ros.ConnectivityException, 
        tf2_ros.ExtrapolationException) as e:  # Fixed variable name
    self.get_logger().error(f'TF error: {str(e)}')
```

### 2. Publisher Context Error During Shutdown
**Symptoms**:  
- `rclpy._rclpy_pybind11.RCLError: Failed to publish: publisher's context is invalid`  
- Occurred when publishing stop command during shutdown  

**Resolution**:  
Added ROS context validity check before publishing:
```python
def stop_robot(self):
    if rclpy.ok():  # Ensure valid ROS context
        cmd_vel = Twist()
        self.cmd_vel_pub.publish(cmd_vel)
```

### 3. URDF Inertia Warning
**Symptoms**:  
- `[WARN] [kdl_parser]: The root link base_link has an inertia specified...`  

**Resolution**:  
Modified URDF to add dummy root link:
```xml
<link name="base_dummy"/>
<joint name="dummy_joint" type="fixed">
  <parent link="base_dummy"/>
  <child link="base_link"/>
</joint>
```

### 4. Invalid Laser Scan Values
**Symptoms**:  
- Initial scans showing `min: inf, max: inf`  
- Planner skipping scans due to invalid values  

**Resolution**:  
Added scan validation in planner callback:
```python
if any(math.isinf(r) for r in scan.ranges):
    self.get_logger().warn("Skipping invalid scan")
    return
```

### 5. Missing Gazebo Plugin
**Symptoms**:  
- `[Err] Failed to load system plugin [gz-sim-tf-system]`  

**Resolution**:  
Installed missing plugin:
```bash
sudo apt-get install libignition-gazebo6-tf-system-plugin
```

### 6. DWA Planner Initialization Delays
**Symptoms**:  
- Continuous `Waiting for laser scan data...` warnings  
- Delayed startup  

**Resolution**:  
- Verified sensor topic names matched configuration  
- Added initialization timeout handling  
- Implemented scan validation to skip invalid initial readings  

## System Verification

### 1. TF Tree Validation
```bash
ros2 run tf2_tools view_frames
```
Confirm proper transform chain: `odom → base_link → lidar`

### 2. Laser Scan Test
```bash
ros2 topic echo /scan
```
Verify valid range values (non-inf)

### 3. Motion Test
```bash
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.2}}' -1
```
Confirm robot responds to velocity commands

## Key Improvements Implemented
1. Robust exception handling in TF operations
2. Graceful shutdown management
3. Sensor data validation
4. URDF structural compliance
5. Enhanced debugging logs in planner
6. Dependency management for Gazebo plugins

## Current Status
The navigation system is fully functional with the robot successfully navigating to goals while avoiding obstacles in simulation. The DWA planner parameters are optimized for the specific robot configuration and environment.







