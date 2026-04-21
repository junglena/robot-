import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    # 获取rviz配置文件路径
    urdf_package_path = os.path.join(get_package_share_directory('bot_desc'))
    urdf_path = os.path.join(urdf_package_path, 'urdf', 'first_robot.urdf')
    default_rviz_config_path = os.path.join(urdf_package_path, 'config', 'display_robot_model.rviz')
    #声明一个urdf目录的参数，方便修改
    action_declare_arg_mode_path=launch.actions.DeclareLaunchArgument(
        'model',
        default_value=urdf_path,
        description='URDF file path'
    )

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        parameters=[{
            'robot_description': launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])
        }]
    )

    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )


    # 启动rviz2，并加载配置文件
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path]
    )
    

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])