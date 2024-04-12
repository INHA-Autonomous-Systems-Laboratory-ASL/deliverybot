#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.conditions import IfCondition

# this is the function launch  system will look for
def generate_launch_description():
    
    slam_arg = DeclareLaunchArgument(
		name="slam",
		default_value="True",
		description="Launch SLAM or launch localization and navigation",
		choices=["True", "False"],
	)
    
    # create and return launch description object
    return LaunchDescription(
        [
            slam_arg,
            OpaqueFunction(function=launch_setup),
        ]
    )


def launch_setup(context, *args, **kwargs):

    nav2_bringup_dir = get_package_share_directory("deliverybot_bringup")
    nav2_launch_file = os.path.join(nav2_bringup_dir, "launch", "sw_navigation_launch.py")
    # nav2_launch_file = os.path.join(nav2_bringup_dir, "launch", "kazim_navigation_launch.py")

    # Real robot
    params_file_name = "sw_nav2_params.yaml"
    use_sim_time = "false"
    # map_file = "airlab/map_lidar3d_v2.yaml"

    # parameters file path
    nav2_params_file = os.path.join(nav2_bringup_dir, "param", params_file_name)
    
    description_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('deliverybot_description'), 
                    '/launch/launch_deliverybot.launch.py']),
    )

    livox_ros_driver_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('livox_ros_driver2'), 
                    '/launch_ROS2/rviz_MID360_launch.py']),
    )

    pointcloud_to_laserscan_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('pointcloud_to_laserscan'), 
                    '/launch/livox_pointcloud_to_laserscan_launch.py']),
    )

    realsense_camera_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('realsense2_camera'), 
                    '/launch/rs_launch.py']),
    )

    depthimage_to_laserscan_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [get_package_share_directory('depthimage_to_laserscan'), 
                    '/launch/depthimage_to_laserscan-launch.py']),
    )

    livox_frame_remapping_publisher = Node(
        package='livox_frame_remap',
        executable='livox_frame_remap_node',
        output='screen',
    )

    # odom_publisher = Node(
    #     package='livox_frame_remap',
    #     executable='livox_frame_remap_node',
    #     output='screen',
    # )

    nav2_launch = IncludeLaunchDescription(
		        PythonLaunchDescriptionSource(nav2_launch_file),
		        launch_arguments={
		        	"use_sim_time": use_sim_time,
		        	"params_file": nav2_params_file,  # full configuration parameters
		        	"slam": LaunchConfiguration("slam"),  # slam activated
		        	# "slam": slam,  # slam activated
                    # "autostart" : True,
		        	"map": "",  # no map,
		        }.items(),
		        condition=IfCondition(PythonExpression([LaunchConfiguration("slam"), " == True"])),
		        # condition=IfCondition(PythonExpression([slam, " == True"])),
    )


    # return [nav2_slam_launch, nav2_amcl_nav_launch, rviz_node, static_tf]
    return [description_launch, livox_ros_driver_launch, pointcloud_to_laserscan_launch, realsense_camera_launch, depthimage_to_laserscan_launch, livox_frame_remapping_publisher, nav2_launch]