#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

def publish_fake_scan():
    rospy.init_node('virtual_obstacle_node')
    pub = rospy.Publisher('/scan', LaserScan, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        scan = LaserScan()
        scan.header.stamp = rospy.Time.now()
        scan.header.frame_id = "laser"
        
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.pi / 180  # 1 degree resolution
        scan.time_increment = 0.0
        scan.range_min = 0.15
        scan.range_max = 6.0
        
        num_readings = int((scan.angle_max - scan.angle_min) / scan.angle_increment)
        scan.ranges = [float('inf')] * num_readings  # No obstacle everywhere
        
        # Ahora añadimos obstáculos artificiales
        # Ejemplo: Obstáculo delante
        center = num_readings // 2
        for i in range(center - 10, center + 10):
            scan.ranges[i] = 0.5  # Obstáculo a 0.5 metros

        pub.publish(scan)
        rate.sleep()

if __name__ == '__main__':
    publish_fake_scan()

