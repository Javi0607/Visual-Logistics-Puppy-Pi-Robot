#!/usr/bin/env python3
# coding=utf-8
# Date:2025/29/05
# Author:nab

import sys
import cv2
import math
import rospy
import numpy as np
from threading import RLock, Timer
import threading

from std_srvs.srv import *
from sensor_msgs.msg import Image

from sensor.msg import Led
from object_tracking.srv import *
from puppy_control.msg import Velocity, Pose, Gait

from puppy_pi import PID
from puppy_pi import Misc

from puppy_control.srv import SetRunActionName
from puppy_pi import apriltag


PuppyPose = {}
PuppyMove = {'x':0, 'y':0, 'yaw_rate':0}
detector = apriltag.Detector(searchpath=apriltag._get_demo_searchpath())
haved_detect = False
start_move = True



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
        

def run(img):
    global tag_centerx, img_centerx, __isRunning
    img_copy = img.copy()
    img_h, img_w = img.shape[:2]

    if not __isRunning:
        return img

    # Centro de la imagen (referencia)
    with lock:
        img_centerx = img_w // 2

    # Dibuja una cruz en el centro de la imagen
    cv2.line(img, (img_centerx - 10, img_h // 2), (img_centerx + 10, img_h // 2), (0, 255, 255), 2)
    cv2.line(img, (img_centerx, img_h // 2 - 10), (img_centerx, img_h // 2 + 10), (0, 255, 255), 2)

    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # Detectar tags
    results = detector.detect(gray)

    if results:
        tag = results[0]  # Solo usamos el primer tag detectado
        corners = tag.corners  # Lista de 4 vértices

        # Calcular centro del tag
        cX = int(sum([p[0] for p in corners]) / 4.0)
        cY = int(sum([p[1] for p in corners]) / 4.0)
        with lock:
            tag_centerx = cX

        # Dibujar contorno y centro del tag
        for i in range(4):
            pt1 = tuple(map(int, corners[i]))
            pt2 = tuple(map(int, corners[(i + 1) % 4]))
            cv2.line(img, pt1, pt2, (0, 255, 0), 2)
        cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)
    else:
        with lock:
            tag_centerx = -1  # Tag no visible

    return img



def initMove(delay=True):
    global GaitConfig
    with lock:
        PuppyMove['x'] = 0
        PuppyMove['yaw_rate'] = math.radians(0)
        PuppyVelocityPub.publish(x=PuppyMove['x'], y=PuppyMove['y'], yaw_rate=PuppyMove['yaw_rate'])

    rospy.ServiceProxy('/puppy_control/go_home', Empty)()

    PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift']
            ,height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 500)
    
    
    PuppyGaitConfigPub.publish(overlap_time = GaitConfig['overlap_time'], swing_time = GaitConfig['swing_time']
                    , clearance_time = GaitConfig['clearance_time'], z_clearance = GaitConfig['z_clearance'])
                    
    with lock:
        pass
    if delay:
        rospy.sleep(0.5)


def reset():
    global line_centerx
    with lock:
        line_centerx = -1
        PuppyMove['x'] = 0
        PuppyMove['yaw_rate'] = math.radians(0)
        PuppyVelocityPub.publish(x=PuppyMove['x'], y=PuppyMove['y'], yaw_rate=PuppyMove['yaw_rate'])

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

img_centerx = 320
tag_centerx = -1
__isCentered = False


def move():
    global PuppyMove, tag_centerx, img_centerx, __isRunning
    global __isCentered

    __isCentered = False
    rospy.sleep(1)

    while not rospy.is_shutdown():
        if __isRunning:
            if tag_centerx != -1:
                with lock:
                    error = tag_centerx - img_centerx

                if abs(error) <= 50:
                    # Tag centrado: avanzar recto
                    with lock:
                        PuppyMove['yaw_rate'] = 0.0
                    __isCentered = True
                elif error > 50:
                    # Tag a la derecha
                    with lock:
                        PuppyMove['yaw_rate'] = math.radians(-15)
                    __isCentered = False
                elif error < -50:
                    # Tag a la izquierda
                    with lock:
                        PuppyMove['yaw_rate'] = math.radians(15)
                    __isCentered = False
            else:
                # No se ve el tag
                with lock:
                    PuppyMove['x'] = 0
                    PuppyMove['yaw_rate'] = 0.0
                __isCentered = False

            # Si está centrado, avanzar
            if __isCentered:
                with lock:
                    PuppyMove['x'] = 5
                    PuppyMove['yaw_rate'] = 0.0
            
            with lock:
                PuppyVelocityPub.publish(
                    x=PuppyMove['x'],
                    y=PuppyMove['y'],
                    yaw_rate=PuppyMove['yaw_rate']
                )

        rospy.sleep(0.02)




th = threading.Thread(target=move,daemon=True)

if __name__ == '__main__':
    rospy.init_node('puppy_follow_apriltag', log_level=rospy.ERROR)#DEBUG
    rospy.sleep(2)
    PP = rospy.get_param('/puppy_control/PuppyPose')
    PuppyPose = PP['Stand'].copy()
    PG = rospy.get_param('/puppy_control/GaitConfig')
    GaitConfig = PG['GaitConfigFast'].copy()


    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)
    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    PuppyGaitConfigPub = rospy.Publisher('/puppy_control/gait', Gait, queue_size=1)

    image_pub = rospy.Publisher('puppy_follow_apriltag/image_result', Image, queue_size=1)  # register result image publisher
    
    enter_srv = rospy.Service('/puppy_follow_apriltag/enter', Trigger, enter_func)
    exit_srv = rospy.Service('/puppy_follow_apriltag/exit', Trigger, exit_func)
    running_srv = rospy.Service('/puppy_follow_apriltag/set_running', SetBool, set_running)
    heartbeat_srv = rospy.Service('/puppy_follow_apriltag/heartbeat', SetBool, heartbeat_srv_cb)
    
    runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)
    puppy_set_running_srv = rospy.ServiceProxy('/puppy_control/set_running', SetBool)
    
    th.start()

    debug = False
    if debug:
        enter_func(1)
        start_running()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    finally:
        cv2.destroyAllWindows()

