<<<<<<< HEAD
# Install script for directory: /home/pi/Desktop/catkin_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/Desktop/catkin_ws/install")
=======
# Install script for directory: /home/pi/puppy_pi/src

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
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/_setup_util.py")
=======
   "/home/pi/puppy_pi/install/_setup_util.py")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE PROGRAM FILES "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/_setup_util.py")
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE PROGRAM FILES "/home/pi/puppy_pi/build/catkin_generated/installspace/_setup_util.py")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/env.sh")
=======
   "/home/pi/puppy_pi/install/env.sh")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE PROGRAM FILES "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/env.sh")
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE PROGRAM FILES "/home/pi/puppy_pi/build/catkin_generated/installspace/env.sh")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/setup.bash;/home/pi/Desktop/catkin_ws/install/local_setup.bash")
=======
   "/home/pi/puppy_pi/install/setup.bash;/home/pi/puppy_pi/install/local_setup.bash")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE FILE FILES
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/setup.bash"
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/local_setup.bash"
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE FILE FILES
    "/home/pi/puppy_pi/build/catkin_generated/installspace/setup.bash"
    "/home/pi/puppy_pi/build/catkin_generated/installspace/local_setup.bash"
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/setup.sh;/home/pi/Desktop/catkin_ws/install/local_setup.sh")
=======
   "/home/pi/puppy_pi/install/setup.sh;/home/pi/puppy_pi/install/local_setup.sh")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE FILE FILES
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/setup.sh"
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/local_setup.sh"
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE FILE FILES
    "/home/pi/puppy_pi/build/catkin_generated/installspace/setup.sh"
    "/home/pi/puppy_pi/build/catkin_generated/installspace/local_setup.sh"
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/setup.zsh;/home/pi/Desktop/catkin_ws/install/local_setup.zsh")
=======
   "/home/pi/puppy_pi/install/setup.zsh;/home/pi/puppy_pi/install/local_setup.zsh")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE FILE FILES
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/local_setup.zsh"
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE FILE FILES
    "/home/pi/puppy_pi/build/catkin_generated/installspace/setup.zsh"
    "/home/pi/puppy_pi/build/catkin_generated/installspace/local_setup.zsh"
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
   "/home/pi/Desktop/catkin_ws/install/.rosinstall")
=======
   "/home/pi/puppy_pi/install/.rosinstall")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pi/Desktop/catkin_ws/install" TYPE FILE FILES "/home/pi/Desktop/catkin_ws/build/catkin_generated/installspace/.rosinstall")
=======
file(INSTALL DESTINATION "/home/pi/puppy_pi/install" TYPE FILE FILES "/home/pi/puppy_pi/build/catkin_generated/installspace/.rosinstall")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
<<<<<<< HEAD
  include("/home/pi/Desktop/catkin_ws/build/gtest/cmake_install.cmake")
  include("/home/pi/Desktop/catkin_ws/build/puppy_follower/cmake_install.cmake")
  include("/home/pi/Desktop/catkin_ws/build/puppy_navigation/cmake_install.cmake")
  include("/home/pi/Desktop/catkin_ws/build/puppy_avoidance/cmake_install.cmake")
=======
  include("/home/pi/puppy_pi/build/gtest/cmake_install.cmake")
  include("/home/pi/puppy_pi/build/lidar_app/cmake_install.cmake")
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
<<<<<<< HEAD
file(WRITE "/home/pi/Desktop/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}"
=======
file(WRITE "/home/pi/puppy_pi/build/${CMAKE_INSTALL_MANIFEST}"
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
