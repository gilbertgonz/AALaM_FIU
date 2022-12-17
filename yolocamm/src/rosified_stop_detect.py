#!/usr/bin/env python3

# Import the necessary libraries
import rospy # Python library for ROS
import torch
import cv2
import numpy as np
from sensor_msgs.msg import Image # Image is the message type
from bboxarray.msg import custom
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images

# Load custom model
model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'yolov5/runs/train/exp7/weights/best_.pt', force_reload=True)  # yolov5/runs/train/exp7/weights/best_.pt

global bbox

def callback(data):

    ### Variables ###
    global bbox
    x = 0
    y = 0
    xx = 0
    yy = 0


    ### Initializations ###
    br = CvBridge() # Used to convert between ROS and OpenCV images
    img = br.imgmsg_to_cv2(data)
    #rospy.loginfo("receiving video frame") # Output debugging info to the terminal

    # Make detections
    model.conf = 0.4
    model.max_det = 1
    results = model(img)

    # Retrieve bbox values
    for box in results.xyxy[0]: 
        if box[5]==0:
            x = int(box[0])
            y = int(box[1])
            xx = int(box[2])    
            yy = int(box[3]) 
            
    #print(results.xyxy[0])

    bbox = custom()
    bbox.data = [x, y, xx, yy]
    print(bbox)

    bound_box = rospy.Publisher('bounding_box', custom, queue_size=1)
    bound_box.publish(bbox)
    r = rospy.Rate(1)
    r.sleep 
    
    # Show camera
    cv2.imshow("Camera", np.squeeze(results.render()))
    
    cv2.waitKey(1)

def receive_message():
 
  # Tells rospy the name of the node.
  # Anonymous = True makes sure the node has a unique name.
  rospy.init_node('bounding_boxx')
   
  # Node is subscribing to the video_frames topic
  rospy.Subscriber('/camera/color/image_raw', Image, callback)  # /camera/color/image_raw OR /usb_cam/image_raw
 
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
 
  # Close down the video stream when done
  cv2.destroyAllWindows()

if __name__ == '__main__':
  receive_message()