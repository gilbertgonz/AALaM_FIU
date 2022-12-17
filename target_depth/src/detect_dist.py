#!/usr/bin/env python3

import rospy
import numpy as np
from bboxarray.msg import custom
from std_msgs.msg import Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 

global point                                                                          # Initializing the 'point' variable, which is the middle of the target
point = (0,0)

def callback(data):
    global point
    bbox = data.data
    r = rospy.Rate(0.35)

    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
    
    point = (int((x2+x1)/2), int((y2+y1)/2))                                          # Find middle of target bbox (x, y)
    #rospy.loginfo(point) 

def callback1(ros_img):
    global point
    br = CvBridge() 
    
    depth_img = br.imgmsg_to_cv2(ros_img)                                              # Converting between ROS and OpenCV images
  
    distance = depth_img[point[1], point[0]]
    target_distance_pub = rospy.Publisher('target_distance', Int16, queue_size=1)
    target_distance_pub.publish(distance)                                              # Publishing distance value
    #rospy.loginfo(distance)

    r = rospy.Rate(1)
    r.sleep 

def receive_message():
    rospy.init_node('target_distance')                                                 # Initializing node
    rospy.Subscriber('bounding_box', custom, callback, queue_size=1)                   # Subsribing to bbox
    rospy.Subscriber('/camera/depth/image_rect_raw', Image, callback1, queue_size=1)   # Subsribing to raw depth image
    rospy.spin()

if __name__== '__main__':
    receive_message()
    