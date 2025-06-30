#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import RPi.GPIO as GPIO
from std_msgs.msg import *
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Cargar el clasificador preentrenado para detección de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class FaceDetector:
    def __init__(self):
        rospy.init_node('face_detection_puppypi', anonymous=True)
        self.bridge = CvBridge()
        
        # Configuración GPIO
        GPIO.setup(21, GPIO.OUT)  # Asegurarse de que el pin 21 se configura como salida
        
        # Suscribirse al tópico de la cámara (ajústalo si es diferente)
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

    def callback(self, img_msg):
        try:
            # Convertir la imagen de ROS a OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
            
            # Convertir la imagen a escala de grises (necesario para el detector de caras)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Detectar las caras en la imagen
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            if len(faces) > 0:
                if self.face_detected_time is None:
                    self.face_detected_time = time.time()  # Start timer when a face is first detected
                elif time.time() - self.face_detected_time >= 3:  # If face is detected for 3+ seconds
                    rospy.loginfo("Face detected for more than 3 seconds! Activating buzzer.")
                    GPIO.output(21, 1)  # Turn buzzer ON
                    time.sleep(1)  # Buzzer ON for 1 second
                    GPIO.output(21, 0)  # Turn buzzer OFF
                    self.face_detected_time = None  # Reset the timer after buzzer activation
            else:
                self.face_detected_time = None  # Reset timer if no face is detected

            # Dibujar rectángulos alrededor de las caras detectadas
            for (x, y, w, h) in faces:
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Mostrar el número de caras detectadas
            cv2.putText(cv_image, f"Faces detected: {len(faces)}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Mostrar el frame con las caras detectadas
            cv2.imshow('Face Detection PuppyPi', cv_image)
            cv2.waitKey(1)
        
        except Exception as e:
            rospy.logerr("Error al procesar la imagen: %s", str(e))
    

if __name__ == "__main__":
    try:
        face_detector = FaceDetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
        GPIO.cleanup()  # Limpiar la configuración de GPIO al finalizar
