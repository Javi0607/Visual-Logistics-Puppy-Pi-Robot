#!/usr/bin/env sh
# generated from catkin/cmake/template/local_setup.sh.in

# since this file is sourced either use the provided _CATKIN_SETUP_DIR
# or fall back to the destination set at configure time
<<<<<<< HEAD
: ${_CATKIN_SETUP_DIR:=/home/pi/Desktop/catkin_ws/devel}
=======
: ${_CATKIN_SETUP_DIR:=/home/pi/puppy_pi/devel}
>>>>>>> c4b322ddf80978833717aae3b81e3646efcd2d4b
CATKIN_SETUP_UTIL_ARGS="--extend --local"
. "$_CATKIN_SETUP_DIR/setup.sh"
unset CATKIN_SETUP_UTIL_ARGS
