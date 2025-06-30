#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
from std_srvs.srv import SetBool
from sensor_msgs.msg import LaserScan
from puppy_control.msg import Velocity, Pose, Gait

ROS_NODE_NAME = 'puppy_wall_follower'

PuppyMove = {'x': 3.0, 'y': 0.0, 'yaw_rate': 0.0}
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

def cleanup():
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    rospy.loginfo('Apagando movimiento...')

def lidar_callback(scan: LaserScan):
    global PuppyMove

    ranges = scan.ranges
    total = len(ranges)

    idx_right = int((math.radians(-90) - scan.angle_min) / scan.angle_increment)
    idx_front = int((0.0 - scan.angle_min) / scan.angle_increment)

    right = ranges[idx_right] if 0 <= idx_right < total else float('inf')
    front = ranges[idx_front] if 0 <= idx_front < total else float('inf')

    # Debug
    rospy.loginfo(f"Front: {front:.2f} m, Right: {right:.2f} m")

    # Parámetros
    desired_dist = 0.2
    Kp = 1.0
    max_yaw = 0.89

    # Gira en esquina: hay pared delante y NO hay pared a la derecha
    if front < 0.4:
        rospy.loginfo("⚠️ Esquina detectada: girando a la izquierda")
        #PuppyMove['x'] = 2.0
        PuppyMove['yaw_rate'] = 0.2

    # Sigue la pared derecha normalmente
    elif right > 0.3 and front > 0.4:
        error = right - desired_dist
        yaw_correction = -Kp * error
        #PuppyMove['x'] = 5.0
        PuppyMove['yaw_rate'] = max(min(yaw_correction, max_yaw), -max_yaw)

    # Si nada útil, sigue recto
    else:
        #PuppyMove['x'] = 5.0
        PuppyMove['yaw_rate'] = 0.0



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
        PuppyVelocityPub.publish(x=PuppyMove['x'], y=0.0, yaw_rate=PuppyMove['yaw_rate'])
        rate.sleep()