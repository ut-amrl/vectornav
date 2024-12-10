cmake_minimum_required(VERSION 2.8.3)
project(vectornav)

# Compile options to ensure compatibility with C++11
add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
    roscpp
    message_generation
    message_runtime
)

## Add message files (if your package defines custom messages)
add_message_files(
    FILES
    Ins.msg
)

## Generate message headers and dependencies
generate_messages(
    DEPENDENCIES
    std_msgs
)

## Dynamically find the amrl_msgs include directory
execute_process(
    COMMAND rospack find amrl_msgs
    OUTPUT_VARIABLE AMRL_MSGS_PATH
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(AMRL_MSGS_INCLUDE_DIR "${AMRL_MSGS_PATH}/msg_gen/cpp/include")

include_directories(${AMRL_MSGS_INCLUDE_DIR})

###################################
## catkin specific configuration ##
###################################
catkin_package(
#   INCLUDE_DIRS include
# LIBRARIES vectornav  # Uncomment if your package provides libraries
  CATKIN_DEPENDS roscpp sensor_msgs message_runtime
)

###########
## Build ##
###########

# Include the additional library directory
add_subdirectory(vnproglib-1.2.0.0/cpp)

## Specify additional locations of header files
include_directories(
  vnproglib-1.2.0.0/cpp/include 
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ executable
add_executable(vnpub src/main.cpp)

## Ensure that vnpub depends on the generated message headers
add_dependencies(vnpub 
  ${${PROJECT_NAME}_EXPORTED_TARGETS} 
  ${catkin_EXPORTED_TARGETS}
)

## Specify libraries to link a library or executable target against
target_link_libraries(vnpub
  libvncxx
  ${catkin_LIBRARIES}
)

## Install the executable
install(TARGETS vnpub
   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)