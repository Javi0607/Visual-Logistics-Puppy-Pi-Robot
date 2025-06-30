#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Quaternion
import math

x = 0.0
y = 0.0
theta = 0.0

def cmd_vel_callback(msg):
    global x, y, theta

    dt = 0.1  # intervalo de simulación 10Hz

    vx = msg.linear.x
    vy = msg.linear.y
    vth = msg.angular.z

    # Actualizar posición simulada
    delta_x = (vx * math.cos(theta) - vy * math.sin(theta)) * dt
    delta_y = (vx * math.sin(theta) + vy * math.cos(theta)) * dt
    delta_theta = vth * dt

    x += delta_x
    y += delta_y
    theta += delta_theta

def simulator():
    global x, y, theta
    rospy.init_node('simple_motion_simulator')
    pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()

        # Publicar transformación odom -> base_link
        br.sendTransform((x, y, 0.0),
                         tf.transformations.quaternion_from_euler(0, 0, theta),
                         current_time,
                         "base_link",
                         "odom")

        # Publicar mensaje de odometría
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(*tf.transformations.quaternion_from_euler(0, 0, theta))

        pub.publish(odom)

        rate.sleep()

if __name__ == '__main__':
    simulator()

