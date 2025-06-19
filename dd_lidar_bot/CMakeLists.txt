cmake_minimum_required(VERSION 3.8)
project(dd_lidar_bot)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(ros_gz_sim REQUIRED)

# Install Python scripts as executables
install(PROGRAMS
  scripts/dwa_planner.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# Install URDF, config, and worlds
install(DIRECTORY
  urdf
  config
  worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
