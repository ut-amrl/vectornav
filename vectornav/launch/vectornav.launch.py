import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    this_dir = get_package_share_directory('vectornav')
    
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='vectornav',
        description='Frame ID for vectornav messages'
    )

    rate_divisor_arg = DeclareLaunchArgument(
        'rate_divisor',
        default_value='8',
        description='BO1 rate divisor used by VectorNav binary output (default 8 for 100hz)'
    )

    port_arg = DeclareLaunchArgument(
        'port',
        default_value='/dev/ttyUSB0',
        description='Serial port device for VectorNav sensor'
    )

    baud_arg = DeclareLaunchArgument(
        'baud',
        default_value='230400',
        description='Serial baud rate for VectorNav sensor'
    )
    
    # Vectornav
    start_vectornav_cmd = Node(
        package='vectornav', 
        executable='vectornav',
        output='screen',
        parameters=[os.path.join(this_dir, 'config', 'vectornav.yaml'),
                   {
                       'frame_id': LaunchConfiguration('frame_id'),
                       'port': ParameterValue(
                           LaunchConfiguration('port'),
                           value_type=str
                       ),
                       'baud': ParameterValue(
                           LaunchConfiguration('baud'),
                           value_type=int
                       ),
                       'BO1.rateDivisor': ParameterValue(
                           LaunchConfiguration('rate_divisor'),
                           value_type=int
                       ),
                   }])
    
    start_vectornav_sensor_msgs_cmd = Node(
        package='vectornav', 
        executable='vn_sensor_msgs',
        output='screen',
        parameters=[os.path.join(this_dir, 'config', 'vectornav.yaml')])

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(frame_id_arg)
    ld.add_action(rate_divisor_arg)
    ld.add_action(port_arg)
    ld.add_action(baud_arg)
    ld.add_action(start_vectornav_cmd)
    ld.add_action(start_vectornav_sensor_msgs_cmd)

    return ld
