#!/usr/bin/env python3

# Written by Ivan Shevtsov <ishevtsov0108@gmail.com>, October 2023


import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    
    bringup_dir      = get_package_share_directory("master_setup")
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    slam_launch_file = os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')


    params_file  = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')


    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(bringup_dir, 'config', 'slam_params.yaml'),
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')


    start_slam_toolbox_cmd_with_params = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch_file),
        launch_arguments={'use_sim_time': use_sim_time,
                          'slam_params_file': params_file}.items()
    )

    ld = LaunchDescription()
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(start_slam_toolbox_cmd_with_params)

    return ld