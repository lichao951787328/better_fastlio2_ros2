import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('fast_lio_sam')
    
    # Declare launch arguments
    rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Launch RViz'
    )
    
    # Config file path
    config_file = os.path.join(pkg_dir, 'config', 'hap_livox.yaml')
    
    # Launch the main mapping node
    mapping_node = Node(
        package='fast_lio_sam',
        executable='fastlio_sam_mapping',
        name='laserMapping',
        output='screen',
        parameters=[config_file]
    )
    
    # RViz node
    rviz_config = os.path.join(pkg_dir, 'rviz_cfg', 'loam_livox.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', rviz_config],
        condition=LaunchConfiguration('rviz')
    )
    
    return LaunchDescription([
        rviz_arg,
        mapping_node,
        rviz_node
    ])
