import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'robot'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'world': '$(find robot)/worlds/maze.world'}.items()
    )

    maze_world = os.path.join(get_package_share_directory(
        package_name), 'worlds', 'maze.world')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': maze_world}.items()
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'robot',
                                   '-x', '0.50',
                                   '-y', '0.50',
                                   '-Y', '1.57'],
                        output='screen')

    joy_params = os.path.join(get_package_share_directory(
        'robot'), 'config', 'joystick.yaml')

    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[joy_params],
    )

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_node',
        parameters=[joy_params],
        # remappings=[('/cmd_vel', 'diff_cont/cmd_vel_unstamped')],
    )

    rviz_file = os.path.join(get_package_share_directory(
        package_name), 'config', 'robot_rviz.rviz')

    rviz = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_file]
    )

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(
            'slam_toolbox'), 'launch', 'online_async_launch.py')]),
        launch_arguments={
            # 'params_file' : 'src/robot/config/mapper_params_online_async.yaml',
            'use_sim_time': 'true'

        }.items()
    )

    rtabmap = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        arguments=[
            '-d', rviz_file,
            'map_always_update', 'true',
            'frame_id', 'base_link'
        ],
        remappings=[
            ('rgb/image', '/camera/image_raw'),
            ('rgb/camera_info', '/camera/camera_info'),
            ('depth/image', '/camera/depth/image_raw')
        ],
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        joy_node,
        teleop_node,
        rviz,
        # slam_toolbox,
    ])
