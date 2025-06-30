<<<<<<< HEAD
# Install script for directory: /home/pi/Desktop/catkin_ws/src/puppy_navigation

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/Desktop/catkin_ws/install")
=======
# Install script for directory: /home/pi/puppy_pi/src/puppy_navigation

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/puppy_pi/install")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
<<<<<<< HEAD
    set(CMAKE_INSTALL_CONFIG_NAME "")
=======
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pi/Desktop/catkin_ws/build/puppy_navigation/catkin_generated/installspace/puppy_navigation.pc")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pi/puppy_pi/build/puppy_navigation/catkin_generated/installspace/puppy_navigation.pc")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/puppy_navigation/cmake" TYPE FILE FILES
<<<<<<< HEAD
    "/home/pi/Desktop/catkin_ws/build/puppy_navigation/catkin_generated/installspace/puppy_navigationConfig.cmake"
    "/home/pi/Desktop/catkin_ws/build/puppy_navigation/catkin_generated/installspace/puppy_navigationConfig-version.cmake"
=======
    "/home/pi/puppy_pi/build/puppy_navigation/catkin_generated/installspace/puppy_navigationConfig.cmake"
    "/home/pi/puppy_pi/build/puppy_navigation/catkin_generated/installspace/puppy_navigationConfig-version.cmake"
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/puppy_navigation" TYPE FILE FILES "/home/pi/Desktop/catkin_ws/src/puppy_navigation/package.xml")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/puppy_navigation" TYPE FILE FILES "/home/pi/puppy_pi/src/puppy_navigation/package.xml")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()

