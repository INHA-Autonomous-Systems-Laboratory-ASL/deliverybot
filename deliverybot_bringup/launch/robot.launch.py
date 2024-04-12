#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():
    livox_frame_remapping_publisher = Node(
        package='livox_frame_remap',
        executable='livox_frame_remap_node',
        output='screen',
    )
    
    return LaunchDescription(
        [
        # robot setting
            # tf setting
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('deliverybot_description'), 
                    '/launch/launch_deliverybot.launch.py']),
                launch_arguments={
                    'use_sim_time' : 'False'
                }.items()
            ),
            # ekf setting
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('deliverybot_bringup'), 
                    '/launch/dual_ekf_navsat.launch.py']),
            ),
            # joystic
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('teleop_twist_joy'), 
                    '/launch/teleop-launch.py']),
                launch_arguments={
                    'joy_config' : 'xbox',
                    'joy_vel' : 'joy_vel'
                }.items()
            ),
            # cmd_vel mux (joy_vel, nav_vel)
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('twist_mux'), 
                    '/launch/twist_mux_launch.py']),
            ),
        # sensor setting
            # gps front (navsat_fix data)
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('ublox_gps'), 
                    '/launch/ublox_f9p_base_launch.py']),
            ),
            # # gps rear (headgin data)
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         [get_package_share_directory('ublox_gps'), 
            #         '/launch/ublox_f9p_rover_launch.py']),
            # ),
            # camera 
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('realsense2_camera'), 
                    '/launch/rs_launch.py']),
            ),
            # camera depth image to laser scan
             IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('depthimage_to_laserscan'), 
                    '/launch/depthimage_to_laserscan-launch.py']),
            ),
            # lidar
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('livox_ros_driver2'), 
                    '/launch_ROS2/rviz_MID360_launch.py']),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('pointcloud_to_laserscan'), 
                    '/launch/livox_pointcloud_to_laserscan_launch.py']),
            ),
            
            #
        ]
    )