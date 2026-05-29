#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
import os
def generate_launch_description():
    controllers_file = PathJoinSubstitution([
        FindPackageShare("mini_pupper_simulation"),
        "config/ros2_control",
        "mini_pupper_2_controllers_sim.yaml"
    ])

    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controllers_file, {"use_sim_time": True}],
        output="screen",
        remappings=[("/robot_description", "/robot_description")],
    )

    robot_model = os.getenv("ROBOT_MODEL", default="mini_pupper_2")
    description_package = FindPackageShare("mini_pupper_description")
    bringup_package = FindPackageShare("mini_pupper_bringup")

    urdf_file = PathJoinSubstitution([
        description_package,
        "urdf",
        robot_model,
        "mini_pupper_description.urdf.xacro"
    ])

    robot_description = ParameterValue(
    Command(["xacro ", urdf_file, " use_gazebo_hardware:=true"]),
    value_type=str,
    )
    gazebo_ros2_control = Node(
    package='gazebo_ros2_control',
    executable='gazebo_ros2_control',
    name='gazebo_ros2_control',
    output='screen',
    parameters=[
        {'robot_description': robot_description},
        PathJoinSubstitution([FindPackageShare('mini_pupper_simulation'),
                             'config/ros2_control/mini_pupper_2_controllers_sim.yaml'])
    ],
)
    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager", "--activate"],
        output="screen"
    )

    quadruped_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["simple_quadruped_controller", "--controller-manager", "/controller_manager", "--activate"],
        output="screen"
    )

    # Event handlers
    joint_handler = RegisterEventHandler(
        OnProcessStart(target_action=controller_manager_node, on_start=[joint_state_spawner])
    )

    quadruped_handler = RegisterEventHandler(
        OnProcessExit(target_action=joint_state_spawner, on_exit=[quadruped_spawner])
    )

    return LaunchDescription([
        gazebo_ros2_control,
        controller_manager_node,
        joint_handler,
        quadruped_handler,
    ])