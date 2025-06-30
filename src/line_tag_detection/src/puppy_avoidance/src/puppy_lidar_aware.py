#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
from std_srvs.srv import SetBool
from sensor_msgs.msg import LaserScan
from puppy_control.msg import Velocity, Pose, Gait

ROS_NODE_NAME = 'puppy_lidar_aware'

# Estados de navegación
FORWARD = 0
REVERSE = 1
STOP = 2

PuppyMove = {'x': 5.0, 'y': 0.0, 'yaw_rate': 0.0}
PuppyPose = {
    'roll': math.radians(0),
    'pitch': math.radians(0),
    'yaw': 0.0,
    'height': -10,
    'x_shift': -0.9,
    'stance_x': 0.0,
    'stance_y': 0.0
}

gait = 'Trot'
GaitConfig = {
    'overlap_time': 0.2,
    'swing_time': 0.3,
    'clearance_time': 0.0,
    'z_clearance': 5
}

min_obstacle_dist = 0.4  # metros
surrounded_threshold = 0.6  # si todo alrededor está más cerca que esto, se considera rodeado

current_state = FORWARD

def cleanup():
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    rospy.loginfo('Apagando movimiento...')

def lidar_callback(scan: LaserScan):
    global current_state, PuppyMove

    ranges = scan.ranges
    front = ranges[len(ranges)//2 - 15 : len(ranges)//2 + 15]
    sides = ranges[::30]  # toma medidas en 12 direcciones (aprox. cada 30 grados)

    front_clear = all(r > min_obstacle_dist or math.isnan(r) for r in front)
    surrounded = all(0.1 < r < surrounded_threshold for r in sides if not math.isnan(r))

    if surrounded:
        current_state = STOP
    elif not front_clear:
        current_state = REVERSE
    else:
        current_state = FORWARD

if __name__ == '__main__':
    rospy.init_node(ROS_NODE_NAME)
    rospy.on_shutdown(cleanup)

    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    PuppyGaitConfigPub = rospy.Publisher('/puppy_control/gait', Gait, queue_size=1)
    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)

    rospy.Subscriber('/scan', LaserScan, lidar_callback)

    set_mark_time_srv = rospy.ServiceProxy('/puppy_control/set_mark_time', SetBool)

    rospy.sleep(0.5)
    PuppyPosePub.publish(
        stance_x=PuppyPose['stance_x'],
        stance_y=PuppyPose['stance_y'],
        x_shift=PuppyPose['x_shift'],
        height=PuppyPose['height'],
        roll=PuppyPose['roll'],
        pitch=PuppyPose['pitch'],
        yaw=PuppyPose['yaw'],
        run_time=500
    )

    rospy.sleep(0.5)
    PuppyGaitConfigPub.publish(
        overlap_time=GaitConfig['overlap_time'],
        swing_time=GaitConfig['swing_time'],
        clearance_time=GaitConfig['clearance_time'],
        z_clearance=GaitConfig['z_clearance']
    )

    rospy.sleep(0.5)
    set_mark_time_srv(False)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if current_state == FORWARD:
            PuppyVelocityPub.publish(x=8.0, y=0.0, yaw_rate=0.0)
        elif current_state == REVERSE:
            PuppyVelocityPub.publish(x=0.0, y=0.0, yaw_rate=0.2)
            rospy.sleep(0.5)
            PuppyVelocityPub.publish(x=-3.0, y=0.0, yaw_rate=0.0)
        elif current_state == STOP:
            PuppyVelocityPub.publish(x=0.0, y=0.0, yaw_rate=0.0)
        rate.sleep()


