#!/usr/bin/env python3

# Written by Ivan Shevtsov <ishevtsov0108@gmail.com>, October 2023

# Launch slam and rviz

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    bringup_dir = get_package_share_directory("master_setup")
    launch_dir = os.path.join(bringup_dir, 'launch')


    use_sim_time = LaunchConfiguration('use_sim_time')
    use_respawn = LaunchConfiguration('use_respawn')


    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_use_respawn_cmd = DeclareLaunchArgument(
        'use_respawn', default_value='False',
        description='Whether to respawn if a node crashes. Applied when composition is disabled.')


    bringup_cmd_group = GroupAction([

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'master_slam.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time,
                              'autostart': 'true',
                              'use_respawn': use_respawn}.items()),

        Node(
            package='aruco_pkg',
            namespace='',
            executable='aruco_scan',
            name='aruco_scan'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'rviz.launch.py')),
            launch_arguments={}.items()
        )
    ])
    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')


    ld = LaunchDescription()


    ld.add_action(stdout_linebuf_envvar)

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_respawn_cmd)

    ld.add_action(bringup_cmd_group)

    cmd_vel_warper = Node(
        package = "cmd_vel_warper",
        executable = "cmd_vel_warper",
        output = "screen"
    )

    ld.add_action(cmd_vel_warper)

    return ld