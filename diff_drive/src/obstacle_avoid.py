#!/usr/bin/env python3

import rospy
import cv2
from bboxarray.msg import custom
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge 
import rospy
from geometry_msgs.msg import Twist


def callback_bbox(data):
    global x1, x2, y1, y2, x_val

    # rospy.loginfo(rospy.get_name()+ "I heard %s", data.data)
    bbox = data.data 
    x1, x2, y1, y2 = bbox[0], bbox[2], bbox[1], bbox[3]
    x_val = (x1 + x2) / 2
    
def callback_obs(data):
    move= Twist()
    speed = 0.1
    size = 640
    ranges = 40
    distance = 800
    range_plus = (size/2)+ranges
    range_minus = (size/2)-ranges
    r = rospy.Rate(1)
    obs_dist = data.data
    #rospy.loginfo(rospy.get_name()+ " I heard %s", data.data)

    tl, tm, tr, l, m, r, bl, bm, br = obs_dist[0], obs_dist[1], obs_dist[2], obs_dist[3], obs_dist[4], obs_dist[5], obs_dist[6], obs_dist[7], obs_dist[8]


    if tl > distance and tm > distance and tr > distance and l > distance and m > distance and r > distance and br > distance and bm > distance and bl > distance:
        if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:
            if y2 < 475:
                if x_val > range_plus: # When vehicle is the left of the target
                    move.angular.z = -speed
                    rospy.loginfo("Twist Right")
                    step_cmd_vel.publish(move)
                elif x_val < range_minus: # When vehicle is the right of the target
                    move.angular.x = speed
                    move.angular.y = speed
                    rospy.loginfo("Twist Left")
                    step_cmd_vel.publish(move)
                elif range_minus < x_val <range_plus:
                    move.linear.x = speed
                    rospy.loginfo("Twist Forward")
                    step_cmd_vel.publish(move)
                else:
                    move.linear.x = 0
                    rospy.loginfo("Stop")
                    step_cmd_vel.publish(move)
            else:
                move.linear.x = 0
                rospy.loginfo("Arrived at target")
                step_cmd_vel.publish(move)
        else:
            move.linear.x = 0
            rospy.loginfo("No target detected")
            step_cmd_vel.publish(move)
    else:
        move.linear.x = 0
        rospy.loginfo("Nearby object detected!")
        step_cmd_vel.publish(move)


if __name__== '__main__':
    rospy.init_node('diff_drive')
    sub = rospy.Subscriber('bounding_box',custom,callback_bbox)
    sub = rospy.Subscriber('obstacle_distances',custom,callback_obs)
    step_cmd_vel = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    rospy.spin()