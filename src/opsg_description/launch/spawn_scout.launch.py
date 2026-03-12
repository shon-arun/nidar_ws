import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_opsg_description = get_package_share_directory('opsg_description')
    
    # CRITICAL FIX: Tell Gazebo where to find the ROS 2 workspace share folder
    workspace_share_dir = os.path.join(get_package_prefix('opsg_description'), 'share')
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=workspace_share_dir
    )

    urdf_file = os.path.join(pkg_opsg_description, 'urdf', 'scout_drone.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Launch Gazebo Harmonic with an empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_desc}]
    )

    # Spawn the drone using the ros_gz bridge
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-string', robot_desc,
                   '-name', 'scout_drone',
                   '-allow_renaming', 'true',
                   '-z', '0.5'] # Spawn slightly above ground
    )

    return LaunchDescription([
        set_gz_resource_path,
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])