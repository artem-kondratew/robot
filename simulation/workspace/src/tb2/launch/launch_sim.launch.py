import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'tb2'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')]
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    spawn_entity_master = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'tb2_1',
                                   '-x', '-0.50',
                                   '-y', '0.50',
                                   '-z', '0.23',
                                   '-Y', '1.57'],
                        output='screen',
                        namespace='master',
                        )

    goal_pose_pub = Node(
        package='graph_travel',
        executable='goal_pose_publisher',
        name='goal_pose_publisher',
    )

    return LaunchDescription([
        rsp,
        spawn_entity_master,
        goal_pose_pub,
    ])
