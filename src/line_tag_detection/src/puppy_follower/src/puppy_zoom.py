#!/usr/bin/env python3

import cv2
import rospy
import threading
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
zoom_factor = 1.5  # valor inicial por defecto
zoom_lock = threading.Lock()

def digital_zoom(img, zoom):
    if zoom <= 1.0:
        return img

    h, w = img.shape[:2]
    new_w = int(w / zoom)
    new_h = int(h / zoom)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    x2 = x1 + new_w
    y2 = y1 + new_h

    cropped = img[y1:y2, x1:x2]
    zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
    return zoomed

def image_callback(msg):
    global zoom_factor
    try:
        frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        with zoom_lock:
            zoom = zoom_factor
        zoomed = digital_zoom(frame, zoom)
        cv2.imshow("Zoom Digital", zoomed)
        cv2.waitKey(1)
    except Exception as e:
        rospy.logerr(f"Error procesando imagen: {e}")

def user_input_thread():
    global zoom_factor
    while not rospy.is_shutdown():
        try:
            user_input = input("Introduce el zoom (ej. 1.0 a 5.0): ")
            new_zoom = float(user_input)
            if new_zoom >= 1.0:
                with zoom_lock:
                    zoom_factor = new_zoom
                rospy.loginfo(f"Nuevo zoom: {zoom_factor}")
            else:
                rospy.logwarn("El valor de zoom debe ser >= 1.0")
        except ValueError:
            rospy.logwarn("Por favor, introduce un número válido.")

if __name__ == '__main__':
    rospy.init_node("digital_zoom_node")

    # Iniciar hilo para entrada del usuario
    hilo = threading.Thread(target=user_input_thread)
    hilo.daemon = True
    hilo.start()

    rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
    rospy.spin()
