#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from puppy_control.msg import Velocity

class SimpleObstacleAvoidance:

    def __init__(self):
        rospy.init_node('simple_obstacle_avoidance')
        self.velocity_pub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.safe_distance = 0.4  # Distancia mínima segura en metros (ajústala)
        self.state = "FORWARD"  # Estado inicial: avanzar
        rospy.loginfo("Simple Obstacle Avoidance node started.")
        rospy.spin()

    def scan_callback(self, scan):
        min_distance = min(scan.ranges)

        if min_distance < self.safe_distance:
            # Obstáculo detectado: girar
            self.state = "TURN"
        else:
            # Ningún obstáculo cerca: avanzar
            self.state = "FORWARD"

        self.publish_velocity()

    def publish_velocity(self):
        vel = Velocity()

        if self.state == "FORWARD":
            vel.x = -0.5  # Caminar adelante (cm/s)
            vel.y = 0.0
            vel.yaw_rate = 0.0
        elif self.state == "TURN":
            vel.x = 0.5
            vel.y = 0.0
            vel.yaw_rate = 0  # Girar hacia la izquierda (rad/s)

        self.velocity_pub.publish(vel)

if __name__ == '__main__':
    SimpleObstacleAvoidance()







