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
#UPDATES
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


                          ### Turtlesim working

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

<p align="center">
  <img src="[https://github.com/user-attachments/assets/c732f61c-2e3b-48a8-b4d6-7b1476401236](https://github.com/user-attachments/assets/b135490c-143d-4b13-aafd-07a26e67f6da)" alt="2WD Robot Demo" width="500"/>
</p>









