import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    # 获取功能包的share路径
    urdf_package_path = os.path.join(get_package_share_directory('bot_desc'))
    default_xacro_path = os.path.join(urdf_package_path, 'urdf', 'mybot/labot.urdf.xacro')
    default_gazebo_world_path=os.path.join(urdf_package_path,'world','custom_room.world')
    #声明一个urdf目录的参数方便修改
    action_declare_arg_mode_path=launch.actions.DeclareLaunchArgument(
        'model',
        default_value=default_xacro_path,
        description='URDF file path'
    )

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])
        }]
    )

    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments=[('world', default_gazebo_world_path),('verbose', 'true')]
    )

    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'mybot'
        ],
        output='screen'
    )

    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd='ros2 control load_controller mybot_joint_state_broadcaster --set-state active'.split(' '),
        output='screen'
    )
    
    #action_load_effort_controller = launch.actions.ExecuteProcess(
        #cmd='ros2 control load_controller mybot_effort_controller --set-state active'.split(' '),
        #output='screen'
    #)

    action_load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd='ros2 control load_controller mybot_diff_drive_controller --set-state active'.split(' '),
        output='screen'
    )
    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[action_load_joint_state_controller]
            )
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_load_joint_state_controller,
                on_exit=[action_load_diff_drive_controller]
            )
        ),

    ])