#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import sys
import cv2
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "cv_bridge_demo"
        rospy.init_node(self.node_name)
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        # Create the OpenCV display window for the RGB image
        self.cv_window_name = self.node_name
        cv2.NamedWindow(self.cv_window_name, cv2.CV_WINDOW_NORMAL)
        cv2.MoveWindow(self.cv_window_name, 25, 75)
        
        # Create the cv_bridge object
        self.bridge = CvBridge()
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback, queue_size=1)
        
        rospy.loginfo("Waiting for image topics...")
        rospy.wait_for_message("/usb_cam/image_raw", Image)
        rospy.loginfo("Ready.")

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e
        
        # Convert the image to a numpy array since most cv2 functions
        # require numpy arrays.
        frame = np.array(frame, dtype=np.uint8)
        
        # Process the frame using the process_image() function
#        display_image = self.process_image(frame)
                       
        # Display the image.
        cv2.imshow(self.node_name, frame)#display_image)
        
        # Process any keyboard commands
        self.keystroke = cv2.waitKey(5)
        if self.keystroke != -1:
            cc = chr(self.keystroke & 255).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")
    
    def cleanup(self):
        print "Shutting down vision node."
        cv2.DestroyAllWindows()   
    
def main(args):       
    try:
        cvBridgeDemo()
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vision node."
        cv2.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
