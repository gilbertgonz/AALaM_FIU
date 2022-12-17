#!/usr/bin/env python3

import rospy
import cv2
from bboxarray.msg import custom
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge 

global pointR, pointL, pointM                                                               # Initializing the 'point' variables for the middle, left, and right of the camera frame
w = 640
h = 480

pointR = (int(w*3/4),int(h/2))
pointL = (int(w/4),int(h/2))
pointM = (int(w/2), int(h/2))

pointTR = (int(w*3/4),int(h/4))
pointTL = (int(w/4),int(h/4))
pointTM = (int(w/2), int(h/4))

pointBR = (int(w*3/4),int(h*3/4))
pointBL = (int(w/4),int(h*3/4))
pointBM = (int(w/2), int(h*3/4))


def distanceFinder(ros_img):
    global pointR, pointL, pointM 
    br = CvBridge()
    offset = 1500 
    
    depth_img = br.imgmsg_to_cv2(ros_img)                                                   # Converting between ROS and OpenCV images
  
    distanceR = depth_img[pointR[1], pointR[0]]
    distanceL = depth_img[pointL[1], pointL[0]]
    distanceM = depth_img[pointM[1], pointM[0]]

    distanceTR = depth_img[pointTR[1], pointTR[0]]
    distanceTL = depth_img[pointTL[1], pointTL[0]]
    distanceTM = depth_img[pointTM[1], pointTM[0]]

    distanceBR = depth_img[pointBR[1], pointBR[0]]
    distanceBL = depth_img[pointBL[1], pointBL[0]]
    distanceBM = depth_img[pointBM[1], pointBM[0]]

    all_distances1 = custom()

    all_distances = [distanceTL, distanceTM, distanceTR,
                          distanceL, distanceM, distanceR,
                          distanceBL, distanceBM, distanceBR]

    transform = [0, 0, 0, 0, 0, 0, 0, 0, 0]    
    for i in range(len(all_distances)):
        if all_distances[i] == 0:
            transform[i] = offset
        else:
            transform[i] = all_distances[i]


    all_distances1.data = transform
            

    all_distance_pub = rospy.Publisher('obstacle_distances', custom, queue_size=1)    
    all_distance_pub.publish(all_distances1)                                                 # Publishing all distance values
    # rospy.loginfo(all_distances1)

    r = rospy.Rate(1)
    r.sleep 

def imageVisual(data):
    br = CvBridge()                                                                         # Used to convert between ROS and OpenCV images
    img = br.imgmsg_to_cv2(data)

    color = (0, 255, 0)

    cv2.circle(img, pointR, 4, color)
    cv2.circle(img, pointL, 4, color)
    cv2.circle(img, pointM, 4, color)

    cv2.circle(img, pointTR, 4, color)
    cv2.circle(img, pointTL, 4, color)
    cv2.circle(img, pointTM, 4, color)

    cv2.circle(img, pointBR, 4, color)
    cv2.circle(img, pointBL, 4, color)
    cv2.circle(img, pointBM, 4, color)

    
    # Show camera
    cv2.imshow("Camera", img)
    cv2.waitKey(1)

def receive_message():
    rospy.init_node('obstacle_detect')                                                       # Initializing node
    rospy.Subscriber('/camera/depth/image_rect_raw', Image, distanceFinder, queue_size=1)    # Subsribing to raw depth image '/camera/depth/image_rect_raw'
    rospy.Subscriber('/camera/color/image_raw', Image, imageVisual, queue_size=1)            # Subsribing to raw color image '/camera/color/image_raw'
    rospy.spin()

if __name__== '__main__':
    receive_message()
    