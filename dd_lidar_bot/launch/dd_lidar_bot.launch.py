import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('dd_lidar_bot')
    world_path = os.path.join(pkg_share, 'worlds', 'obstacle_world.world')
    
    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            )
        ]),
        launch_arguments={
            'gz_args': f'-v 4 {world_path}',
            'on_exit_shutdown': 'true'
        }.items()
    )

    urdf_file = os.path.join(pkg_share, 'urdf', 'dd_lidar_bot.urdf')
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True,
            'publish_frequency': 30.0
        }]
    )

    # Spawn robot at safe position
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'dd_lidar_bot',
            '-x', '-4.0',
            '-y', '0.0',
            '-z', '1.0'  # Increased to 1.0m
        ],
        output='screen'
    )
    
    # Bridge with corrected syntax
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry]gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'  # Corrected syntax
        ],
        output='screen'
    )

    # Static Transforms with new-style arguments
    static_tf_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['--x', '0', '--y', '0', '--z', '0',
                   '--roll', '0', '--pitch', '0', '--yaw', '0',
                   '--frame-id', 'odom', '--child-frame-id', 'base_link'],
        output='screen'
    )
    
    static_tf_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['--x', '0.2', '--y', '0', '--z', '0.1',
                   '--roll', '0', '--pitch', '0', '--yaw', '0',
                   '--frame-id', 'base_link', '--child-frame-id', 'lidar'],
        output='screen'
    )

    # DWA Planner
    dwa_planner = Node(
        package='dd_lidar_bot',
        executable='dwa_planner.py',
        parameters=[os.path.join(pkg_share, 'config', 'dwa_params.yaml')]
    )

    return LaunchDescription([
        LogInfo(msg="Launching dd_lidar_bot in obstacle world"),
        gazebo,
        robot_state_publisher,
        spawn_entity,
        bridge,
        static_tf_odom,
        static_tf_lidar,
        dwa_planner
    ])
