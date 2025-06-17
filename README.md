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



