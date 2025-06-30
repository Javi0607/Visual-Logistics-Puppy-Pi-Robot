#!/usr/bin/env python3

import rospy
import cv2
import time
import RPi.GPIO as GPIO
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Buzzer pin configuration
GPIO.setwarnings(False)
BUZZER_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, 0)  # Ensure the buzzer is OFF initially

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class FaceDetector:
    def __init__(self):
        rospy.init_node('face_detection_puppypi', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

        self.face_detected_time = None  # Store the time when a face is first detected

    def callback(self, img_msg):
        try:
            # Convert ROS image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                if self.face_detected_time is None:
                    self.face_detected_time = time.time()  # Start timer when a face is first detected
                elif time.time() - self.face_detected_time >= 3:  # If face is detected for 3+ seconds
                    rospy.loginfo("Face detected for more than 3 seconds! Activating buzzer.")
                    GPIO.output(BUZZER_PIN, 1)  # Turn buzzer ON
                    time.sleep(1)  # Buzzer ON for 1 second
                    GPIO.output(BUZZER_PIN, 0)  # Turn buzzer OFF
                    self.face_detected_time = None  # Reset the timer after buzzer activation
            else:
                self.face_detected_time = None  # Reset timer if no face is detected

            # Display detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('Face Detection', cv_image)
            cv2.waitKey(1)

        except Exception as e:
            rospy.logerr("Error processing image: %s", str(e))

if __name__ == "__main__":
    try:
        detector = FaceDetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
        GPIO.cleanup()  # Clean up GPIO on exit
