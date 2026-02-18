cmake_minimum_required(VERSION 3.10)

project(fast_lio_sam)

# Set the C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -fexceptions")
add_definitions(-DROOT_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/\")

# Default to Release build
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Processor count logic
if(CMAKE_SYSTEM_PROCESSOR MATCHES "(x86)|(X86)|(amd64)|(AMD64)" )
  include(ProcessorCount)
  ProcessorCount(N)
  if(N GREATER 4)
    add_definitions(-DMP_EN -DMP_PROC_NUM=3)
  elseif(N GREATER 3)
    add_definitions(-DMP_EN -DMP_PROC_NUM=2)
  else()
    add_definitions(-DMP_PROC_NUM=1)
  endif()
else()
  add_definitions(-DMP_PROC_NUM=1)
endif()

# Include directories and dependencies
find_package(OpenMP QUIET)
if (OPENMP_FOUND)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}   ${OpenMP_C_FLAGS}")
endif()

find_package(PythonLibs REQUIRED)

# Find ROS2 packages
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(pcl_ros REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(livox_ros_driver2 REQUIRED)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "/usr/share/cmake/geographiclib")
find_package(Eigen3 REQUIRED)
find_package(PCL REQUIRED)
find_package(OpenCV REQUIRED)
find_package(GeographicLib REQUIRED)
# Use ROS2 version of GTSAM
find_package(GTSAM REQUIRED PATHS /opt/ros/humble/lib/cmake/GTSAM NO_DEFAULT_PATH)

# Generate messages and services
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Pose6D.msg"
  "msg/CloudInfo.msg"
  "srv/SaveMap.srv"
  "srv/SavePose.srv"
  DEPENDENCIES geometry_msgs std_msgs nav_msgs sensor_msgs
)

# Include directories
include_directories(
  include
  ${EIGEN3_INCLUDE_DIR}
  ${PCL_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
  ${GTSAM_INCLUDE_DIR}
  ${OpenCV_INCLUDE_DIRS}
  ${GeographicLib_INCLUDE_DIRS}
  /opt/ros/humble/include
  /opt/ros/humble/include/gtsam
)

# Set ROS2 dependencies
set(dependencies
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
  tf2
  tf2_ros
  tf2_eigen
  tf2_geometry_msgs
  pcl_ros
  pcl_conversions
  cv_bridge
  image_transport
  livox_ros_driver2
)

# Add libraries
add_library(ikd_Tree include/ikd-Tree/ikd_Tree.cpp)
add_library(preprocess src/preprocess.cpp)
add_library(sc include/sc-relo/Scancontext.cpp)
add_library(incremental_mapping include/multi-session/Incremental_mapping.cpp include/sc-relo/Scancontext.cpp)
add_library(pose_estimator include/online-relo/pose_estimator.cpp include/sc-relo/Scancontext.cpp)
add_library(tgrs include/dynamic-remove/tgrs.cpp)

# Link libraries with dependencies
ament_target_dependencies(ikd_Tree ${dependencies})
ament_target_dependencies(preprocess ${dependencies})
ament_target_dependencies(sc ${dependencies})
ament_target_dependencies(incremental_mapping ${dependencies})
ament_target_dependencies(pose_estimator ${dependencies})
ament_target_dependencies(tgrs ${dependencies})

# Add include directories for generated messages
target_include_directories(preprocess PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>"
)
target_include_directories(sc PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>"
)
target_include_directories(incremental_mapping PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>"
)
target_include_directories(pose_estimator PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>"
)
target_include_directories(tgrs PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp>"
)

# Executables
add_executable(fastlio_sam_mapping src/laserMapping.cpp)
target_link_libraries(fastlio_sam_mapping 
  ${PCL_LIBRARIES} 
  ${PYTHON_LIBRARIES} 
  ${GeographicLib_LIBRARIES} 
  ${OpenCV_LIBRARIES} 
  ikd_Tree 
  preprocess 
  sc 
  gtsam 
  stdc++fs
  curl
)
ament_target_dependencies(fastlio_sam_mapping ${dependencies})

add_executable(multi_session src/multi_session.cpp)
target_link_libraries(multi_session 
  ${PCL_LIBRARIES} 
  ${PYTHON_LIBRARIES} 
  ${GeographicLib_LIBRARIES} 
  incremental_mapping 
  gtsam 
  stdc++fs
  curl
)
ament_target_dependencies(multi_session ${dependencies})

add_executable(online_relo src/online_relocalization.cpp)
target_link_libraries(online_relo 
  ${PCL_LIBRARIES} 
  ${PYTHON_LIBRARIES} 
  ${GeographicLib_LIBRARIES} 
  ${OpenCV_LIBRARIES} 
  pose_estimator 
  incremental_mapping 
  gtsam 
  stdc++fs
  curl
)
ament_target_dependencies(online_relo ${dependencies})

add_executable(object_update src/object_update.cpp)
target_link_libraries(object_update 
  ${PCL_LIBRARIES} 
  ${PYTHON_LIBRARIES} 
  ${GeographicLib_LIBRARIES} 
  ${OpenCV_LIBRARIES} 
  tgrs 
  gtsam 
  stdc++fs
  curl
)
ament_target_dependencies(object_update ${dependencies})

# Install targets
install(TARGETS
  fastlio_sam_mapping
  multi_session
  online_relo
  object_update
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS
  ikd_Tree
  preprocess
  sc
  incremental_mapping
  pose_estimator
  tgrs
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install config files
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

# Install rviz files
install(DIRECTORY rviz_cfg
  DESTINATION share/${PROJECT_NAME}
)

# Generate interface dependencies for executables and libraries
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")

# Link typesupport to libraries
target_link_libraries(preprocess "${cpp_typesupport_target}")
target_link_libraries(sc "${cpp_typesupport_target}")
target_link_libraries(incremental_mapping "${cpp_typesupport_target}")
target_link_libraries(pose_estimator "${cpp_typesupport_target}")
target_link_libraries(tgrs "${cpp_typesupport_target}")

# Link typesupport to executables
target_link_libraries(fastlio_sam_mapping "${cpp_typesupport_target}")
target_link_libraries(multi_session "${cpp_typesupport_target}")
target_link_libraries(online_relo "${cpp_typesupport_target}")
target_link_libraries(object_update "${cpp_typesupport_target}")

ament_package()
