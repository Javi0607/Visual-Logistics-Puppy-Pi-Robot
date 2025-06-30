#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from puppy_control.msg import Velocity

class PuppyCmdVelController:

    def __init__(self):
        rospy.init_node('puppy_cmd_vel_controller')

        # Publisher que envía comandos a PuppyPi
        self.velocity_pub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=10)

        # Subscriber que escucha /cmd_vel
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

        rospy.loginfo("Puppy CMD_VEL controller started.")
        rospy.spin()

    def cmd_vel_callback(self, msg):
        vel = Velocity()

        # Traducimos /cmd_vel (metros/segundo y rad/segundo) a PuppyMove (cm/s)
        vel.x = msg.linear.x * 100.0    # m/s -> cm/s
        vel.y = msg.linear.y * 100.0    # m/s -> cm/s (aunque ahora y no se usa mucho)
        vel.yaw_rate = msg.angular.z    # rad/s, se mantiene igual

        rospy.loginfo(f"Received cmd_vel -> Publishing velocity: x={vel.x:.2f} cm/s, y={vel.y:.2f} cm/s, yaw_rate={vel.yaw_rate:.2f} rad/s")

        self.velocity_pub.publish(vel)

if __name__ == '__main__':
    PuppyCmdVelController()

