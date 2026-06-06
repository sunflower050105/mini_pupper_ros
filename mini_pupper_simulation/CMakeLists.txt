cmake_minimum_required(VERSION 3.5)
project(mini_pupper_simulation)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(gz_plugin_vendor REQUIRED)
find_package(gz_sim_vendor REQUIRED)

# Then find the actual Gazebo libraries
find_package(gz-plugin REQUIRED)
find_package(gz-sim REQUIRED)

# For gz_ros2_control
find_package(gz_ros2_control REQUIRED)
find_package(rclpy REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  mini_pupper_simulation/odom_tf_broadcaster.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch resource worlds config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
