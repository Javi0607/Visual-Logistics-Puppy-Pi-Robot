#!/usr/bin/env python3
# coding=utf-8
# Date:2025/27/05
# Author:nab

import sys
import cv2
import math
import rospy
import numpy as np
from threading import RLock, Timer

from std_srvs.srv import *
from sensor_msgs.msg import Image

from sensor.msg import Led
from object_tracking.srv import *
from puppy_control.msg import Velocity, Pose

from puppy_pi import PID
from puppy_pi import Misc

from puppy_control.srv import SetRunActionName
from puppy_pi import apriltag


PuppyPose = {}
PuppyMove = {'x':0, 'y':0, 'yaw_rate':0}
detector = apriltag.Detector(searchpath=apriltag._get_demo_searchpath())
haved_detect = False
start_move = True

x_dis = 500
y_dis = 0.167
Z_DIS = 0.2
z_dis = Z_DIS
x_pid = PID.PID(P=0.06, I=0.005, D=0)  # pid初始化
y_pid = PID.PID(P=0.00001, I=0, D=0)
z_pid = PID.PID(P=0.003, I=0, D=0)

lock = RLock()


velocity_pub = None
image_pub = None

color_range = None
org_image_sub_ed = False
__isRunning = False


def init():
    global color_range 
    
    rospy.loginfo("Tag following start")
    color_range = rospy.get_param('/lab_config_manager/color_range_list', {})  # get lab range from ros param server
    initMove()
    reset()
    
def apriltagDetect(img):   
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    detections = detector.detect(gray, return_image=False)
    if len(detections) != 0:
        for detection in detections:                       
            corners = np.rint(detection.corners)  # 获取四个角点
            cv2.drawContours(img, [np.array(corners, int)], -1, (0, 255, 255), 5, cv2.LINE_AA)
            tag_family = str(detection.tag_family, encoding='utf-8')  # 获取tag_family

            if tag_family == 'tag36h11':
                tag_id = str(detection.tag_id)  # 获取tag_id
                return tag_id
            else:
                return None
    else:
        return None
    



def run(img):
    global PuppyMove, PuppyPose
    global start_move, timeLast
    global x_dis, y_dis, z_dis

    img_copy = img.copy()
    img_h, img_w = img.shape[:2]

    # Dibuja una cruz en el centro de la imagen
    cv2.line(img, (img_w // 2 - 10, img_h // 2), (img_w // 2 + 10, img_h // 2), (0, 255, 255), 2)
    cv2.line(img, (img_w // 2, img_h // 2 - 10), (img_w // 2, img_h // 2 + 10), (0, 255, 255), 2)

    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    tags = detector.detect(gray)

    if not tags:
        return img  # No hay tags

    tag = tags[0]  # Solo seguimos uno
    center_x, center_y = tag.center
    corners = tag.corners
    area = cv2.contourArea(np.array(corners, dtype=np.int32))

    # Dibuja el contorno del tag detectado
    corners_int = np.int32(corners)
    cv2.polylines(img, [corners_int], isClosed=True, color=(0, 255, 0), thickness=2)
    cv2.circle(img, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

    if start_move:
        # PID horizontal (roll)
        x_pid.Kp = 0.003
        x_pid.Ki = 0.00
        x_pid.Kd = 0.00
        x_pid.SetPoint = img_w / 2.0
        if abs(x_pid.SetPoint - center_x) > 230:
            x_pid.Kp = 0.004
        x_pid.update(center_x)
        x_dis = np.clip(x_pid.output, np.radians(-30), np.radians(30))
        PuppyPose['roll'] = x_dis

        # Movimiento hacia adelante o atrás según tamaño del tag
        if abs(area - 900) < 150:
            y_dis = 0
        elif area < 750:
            y_dis = 10
        elif area > 1050:
            y_dis = -7
            
        PuppyMove['x'] = y_dis
        
        #PuppyVelocityPub.publish(x=PuppyMove['x'], y=PuppyMove['y'], yaw_rate=PuppyMove['yaw_rate'])
        # PID vertical (pitch)
        z_pid.Kp = 0.0015
        z_pid.Ki = 0.0000
        z_pid.Kd = 0.0000
        z_pid.SetPoint = img_h / 2.0
        if abs(z_pid.SetPoint - center_y) > 180:
            z_pid.Kp = 0.002
        z_pid.update(center_y)
        z_dis = np.clip(z_pid.output, np.radians(-20), np.radians(30))
        PuppyPose['pitch'] = z_dis

        # Publica la pose del robot
        PuppyPosePub.publish(
            stance_x=PuppyPose['stance_x'],
            stance_y=PuppyPose['stance_y'],
            x_shift=PuppyPose['x_shift'],
            height=PuppyPose['height'],
            roll=PuppyPose['roll'],
            pitch=PuppyPose['pitch'],
            yaw=PuppyPose['yaw']
        )

    return img



# def run(img):
#     
#     global haved_detect
# 
#     if not __isRunning:
#         return img
#     
#     tag_id = apriltagDetect(img) # apriltag检测
#     if tag_id is not None and not haved_detect:
#         haved_detect = True
#     cv2.putText(img, tag_id, (10, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
#     return img
#     
#     return img

def initMove(delay=False):
    runActionGroup_srv('stand.d6a',False)#sit.d6ac
    with lock:
        pass
        # target = ik.setPitchRanges((0, y_dis, Z_DIS), -90, -92, -88)
        # if target:
            # servo_data = target[1]
            # bus_servo_control.set_servos(joints_pub, 1500, ((1, 200), (2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
    if delay:
        rospy.sleep(2)


def reset():
    global x_dis, y_dis, z_dis
    
    with lock:
        x_dis = 500
        y_dis = 0.167
        z_dis = Z_DIS
        x_pid.clear()
        y_pid.clear()
        z_pid.clear()

def enter_func(msg):
    global lock
    global image_sub
    global __isRunning
    global org_image_sub_ed
    
    rospy.loginfo("enter puppy_follower tag")
    init()
    with lock:
        if not org_image_sub_ed:
            org_image_sub_ed = True
            image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, image_callback)
            
    puppy_set_running_srv(True)
    return [True, 'enter']


def exit_func(msg):
    global lock
    global image_sub
    global __isRunning
    global org_image_sub_ed
    
    rospy.loginfo("exit puppy_follower tag")
    with lock:
        __isRunning = False
        reset()
        try:
            if org_image_sub_ed:
                org_image_sub_ed = False
                if heartbeat_timer:heartbeat_timer.cancel()
                image_sub.unregister()
        except BaseException as e:
            rospy.loginfo('%s', e)
    

    return [True, 'exit']

def start_running():
    global lock
    global __isRunning
    
    rospy.loginfo("start running object tracking")
    with lock:
        # turn_on_rgb(__target_color)
        __isRunning = True

def stop_running():
    global lock
    global __isRunning
    
    rospy.loginfo("stop running object tracking")
    with lock:
        __isRunning = False
        reset()
        # initMove(delay=False)


def set_running(msg):
    if msg.data:
        start_running()
    else:
        stop_running()
        
    return [True, 'set_running']

def heartbeat_srv_cb(msg):
    global heartbeat_timer

    if isinstance(heartbeat_timer, Timer):
        heartbeat_timer.cancel()
    if msg.data:
        heartbeat_timer = Timer(5, rospy.ServiceProxy('/puppy_apriltag_follower/exit', Trigger))
        heartbeat_timer.start()
    rsp = SetBoolResponse()
    rsp.success = msg.data

    return rsp


def image_callback(ros_image):
    global lock
    
    image = np.ndarray(shape=(ros_image.height, ros_image.width, 3), dtype=np.uint8,
                       buffer=ros_image.data)  # 将自定义图像消息转化为图像
    cv2_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    frame = cv2_img.copy()
    frame_result = frame
    with lock:
        if __isRunning:
            frame_result = run(frame)
    rgb_image = cv2.cvtColor(frame_result, cv2.COLOR_BGR2RGB).tobytes()
    ros_image.data = rgb_image
    
    rospy.sleep(0.0005)
    image_pub.publish(ros_image)

if __name__ == '__main__':
    rospy.init_node('puppy_apriltag_follower', log_level=rospy.ERROR)#DEBUG
    rospy.sleep(2)
    PP = rospy.get_param('/puppy_control/PuppyPose')
    PuppyPose = PP['Stand'].copy()

    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)
    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    
    image_pub = rospy.Publisher('/puppy_apriltag_follower/image_result', Image, queue_size=1)  # register result image publisher
    
    enter_srv = rospy.Service('/puppy_apriltag_follower/enter', Trigger, enter_func)
    exit_srv = rospy.Service('/puppy_apriltag_follower/exit', Trigger, exit_func)
    running_srv = rospy.Service('/puppy_apriltag_follower/set_running', SetBool, set_running)
    heartbeat_srv = rospy.Service('/puppy_apriltag_follower/heartbeat', SetBool, heartbeat_srv_cb)
    
    runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)
    puppy_set_running_srv = rospy.ServiceProxy('/puppy_control/set_running', SetBool)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    finally:
        cv2.destroyAllWindows()
