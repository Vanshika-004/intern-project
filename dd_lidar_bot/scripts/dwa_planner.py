#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
import math
from geometry_msgs.msg import Twist, PointStamped, Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_point

class DWAPlanner:
    def __init__(self, config):
        self.config = config
        
    def compute_dynamic_window(self, current_vel):
        dt = self.config['dt']
        min_v = max(self.config['min_vel'], current_vel.linear.x - self.config['max_acc'] * dt)
        max_v = min(self.config['max_vel'], current_vel.linear.x + self.config['max_acc'] * dt)
        min_w = max(self.config['min_rot_vel'], current_vel.angular.z - self.config['max_rot_acc'] * dt)
        max_w = min(self.config['max_rot_vel'], current_vel.angular.z + self.config['max_rot_acc'] * dt)
        return [min_v, max_v, min_w, max_w]
    
    def predict_trajectory(self, v, w, initial_pose):
        x, y, theta = initial_pose
        trajectory = []
        time = 0.0
        while time < self.config['predict_time']:
            x += v * math.cos(theta) * self.config['dt']
            y += v * math.sin(theta) * self.config['dt']
            theta += w * self.config['dt']
            trajectory.append([x, y, theta])
            time += self.config['dt']
        return trajectory
    
    def calculate_cost(self, trajectory, goal, laser_scan):
        # Goal cost
        dx = goal[0] - trajectory[-1][0]
        dy = goal[1] - trajectory[-1][1]
        goal_dist = math.sqrt(dx**2 + dy**2)
        goal_cost = self.config['goal_weight'] * goal_dist
        
        # Obstacle cost - improved with direct scan checks
        min_obs_dist = float('inf')
        for point in trajectory:
            # Calculate distance to point in trajectory
            dist = math.sqrt(point[0]**2 + point[1]**2)
            
            # Get angle of point relative to robot
            angle = math.atan2(point[1], point[0])
            
            # Normalize angle to laser scan range
            if angle < laser_scan.angle_min:
                angle += 2 * math.pi
            if angle > laser_scan.angle_max:
                angle -= 2 * math.pi
                
            # Find corresponding laser scan index
            if laser_scan.angle_min <= angle <= laser_scan.angle_max:
                idx = int((angle - laser_scan.angle_min) / laser_scan.angle_increment)
                if 0 <= idx < len(laser_scan.ranges):
                    if laser_scan.ranges[idx] < min_obs_dist:
                        min_obs_dist = laser_scan.ranges[idx]
        
        # Apply safety threshold
        if min_obs_dist < self.config['obstacle_threshold']:
            min_obs_dist = self.config['obstacle_threshold']
        
        obs_cost = self.config['obs_weight'] / (min_obs_dist + 1e-5)
        
        # Speed cost
        speed_cost = self.config['speed_weight'] * (self.config['max_vel'] - abs(v))
        
        return goal_cost + obs_cost + speed_cost
    
    def plan(self, current_pose, current_vel, goal, laser_scan):
        dw = self.compute_dynamic_window(current_vel)
        min_cost = float('inf')
        best_v, best_w = 0.0, 0.0
        
        # Sample velocities
        for v in np.linspace(dw[0], dw[1], self.config['v_samples']):
            for w in np.linspace(dw[2], dw[3], self.config['w_samples']):
                trajectory = self.predict_trajectory(v, w, current_pose)
                cost = self.calculate_cost(trajectory, goal, laser_scan)
                
                if cost < min_cost:
                    min_cost = cost
                    best_v = v
                    best_w = w
                    
        return best_v, best_w

class DWA_Planner(Node):
    def __init__(self):
        super().__init__('dwa_planner')
        
        # Declare parameters with default values
        param_defs = [
            ('max_vel', 0.6),
            ('min_vel', 0.1),
            ('max_rot_vel', 1.8),
            ('min_rot_vel', -1.8),
            ('max_acc', 0.5),
            ('max_rot_acc', 1.2),
            ('robot_radius', 0.35),
            ('dt', 0.1),
            ('predict_time', 2.0),
            ('goal_weight', 1.5),
            ('obs_weight', 1.2),
            ('speed_weight', 0.4),
            ('v_samples', 12),
            ('w_samples', 20),
            ('goal_tolerance', 0.25),
            ('obstacle_threshold', 0.5),
            ('initial_goal', [8.0, 0.0])  # Predefined goal in odom frame
        ]
        
        # Declare parameters
        self.declare_parameters(namespace='', parameters=param_defs)
        
        # Build config dictionary
        self.config = {}
        for name, default in param_defs:
            self.config[name] = self.get_parameter(name).value

        self.get_logger().info("DWA Planner initialized with parameters:")
        for key, value in self.config.items():
            self.get_logger().info(f"  {key}: {value}")
        
        # Setup publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.laser_sub = self.create_subscription(LaserScan, '/scan', self.laser_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        # TF setup
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Initialize state variables
        self.planner = DWAPlanner(self.config)
        self.current_vel = Twist()
        self.laser_scan = None
        self.goal_reached = False
        self.current_pose = [0.0, 0.0, 0.0]  # x, y, theta
        
        # Set predefined goal
        self.goal_map = Point()
        self.goal_map.x = self.config['initial_goal'][0]
        self.goal_map.y = self.config['initial_goal'][1]
        self.get_logger().info(f"Predefined goal set: x={self.goal_map.x:.2f}, y={self.goal_map.y:.2f}")
        
        # Control loop timer
        self.timer = self.create_timer(0.1, self.control_loop)
        
    def laser_callback(self, msg):
        self.laser_scan = msg
        # ADDED DEBUG LINE
        self.get_logger().info(f"Received laser scan: {len(msg.ranges)} ranges, min: {min(msg.ranges):.2f}, max: {max(msg.ranges):.2f}")
        
    def odom_callback(self, msg):
        self.current_vel = msg.twist.twist
        
        # Update current pose
        self.current_pose[0] = msg.pose.pose.position.x
        self.current_pose[1] = msg.pose.pose.position.y
        
        # Convert quaternion to Euler angles (yaw)
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_pose[2] = math.atan2(siny_cosp, cosy_cosp)
        
    def control_loop(self):
        if self.laser_scan is None:
            self.get_logger().warn('Waiting for laser scan data...')
            return
            
        if self.goal_reached:
            return
            
        try:
            # Transform goal to base_link frame
            now = rclpy.time.Time()
            if not self.tf_buffer.can_transform('base_link', 'odom', now):
                self.get_logger().warn('TF not available: base_link to odom')
                return
                
            transform = self.tf_buffer.lookup_transform(
                'base_link', 'odom', now, timeout=rclpy.duration.Duration(seconds=0.5))
            
            goal_point = PointStamped()
            goal_point.header.frame_id = 'odom'
            goal_point.header.stamp = now.to_msg()
            goal_point.point.x = self.goal_map.x
            goal_point.point.y = self.goal_map.y
            goal_point.point.z = 0.0
            goal_base = do_transform_point(goal_point, transform)
            
            # Check if goal is reached
            dist_to_goal = math.sqrt(goal_base.point.x**2 + goal_base.point.y**2)
            if dist_to_goal < self.config['goal_tolerance']:
                self.get_logger().info('Goal reached!')
                self.goal_reached = True
                self.stop_robot()
                return
                
            # Plan using DWA
            v, w = self.planner.plan(
                [0.0, 0.0, 0.0],  # Robot is at origin in base_link frame
                self.current_vel, 
                [goal_base.point.x, goal_base.point.y],
                self.laser_scan
            )
            
            # Publish velocity command
            cmd_vel = Twist()
            cmd_vel.linear.x = v
            cmd_vel.angular.z = w
            self.cmd_vel_pub.publish(cmd_vel)
            
            # Log current state
            self.get_logger().info(f'Command: v={v:.2f} m/s, w={w:.2f} rad/s, Dist: {dist_to_goal:.2f}m')
            
        except Exception as e:
            self.get_logger().error(f'TF error: {str(e)}')
            # Publish zero velocity for safety
            self.stop_robot()
            
    def stop_robot(self):
        cmd_vel = Twist()
        self.cmd_vel_pub.publish(cmd_vel)
        self.get_logger().info('Robot stopped')

def main(args=None):
    rclpy.init(args=args)
    node = DWA_Planner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
