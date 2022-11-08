#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty, String, Int16
from bboxarray.msg import custom

def callback(data):
    rospy.loginfo(rospy.get_name()+ "I heard %s", data.data)
    bbox = data.data
    r = rospy.Rate(0.35)
    move= Twist()
    speed = 0.1
    size = 640
    ranges = 40
    range_plus = (size/2)+ranges
    range_minus = (size/2)-ranges

    x1, x2, y1, y2 = bbox[0], bbox[2], bbox[1], bbox[3]
    x_val = (x1 + x2) / 2
    rospy.loginfo(rospy.get_name()+ "I heard %s", x_val)

    if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:
        if y2 < 475:
            if x_val > range_plus: # When vehicle is the left of the target
                move.linear.x = 0
                move.linear.y = 0
                move.linear.z = 0
                move.angular.x = -speed
                move.angular.y = -speed
                move.angular.z = -speed
                rospy.loginfo("TwistR")
                step_cmd_vel.publish(move)
            elif x_val < range_minus: # When vehicle is the right of the target
                move.linear.x = 0
                move.linear.y = 0
                move.linear.z = 0
                move.angular.x = speed
                move.angular.y = speed
                move.angular.z = speed
                rospy.loginfo("TwistL")
                step_cmd_vel.publish(move)
            elif range_minus < x_val <range_plus:
                move.linear.x = speed
                move.linear.y = 0
                move.linear.z = 0
                move.angular.x = 0
                move.angular.y = 0
                move.angular.z = 0
                rospy.loginfo("TwistForward")
                step_cmd_vel.publish(move)
            else:
                move.linear.x = 0
                move.linear.y = 0
                move.linear.z = 0
                move.angular.x = 0
                move.angular.y = 0
                move.angular.z = 0
                rospy.loginfo("Twist0")
                step_cmd_vel.publish(move)
        else:
                move.linear.x = 0
                move.linear.y = 0
                move.linear.z = 0
                move.angular.x = 0
                move.angular.y = 0
                move.angular.z = 0
                rospy.loginfo("Stop")
                step_cmd_vel.publish(move)

if __name__== '__main__':
    rospy.init_node('diff_drive')
    sub = rospy.Subscriber('bounding_box',custom,callback)
    step_cmd_vel = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    pub = rospy.Publisher('print_cycle1', Empty,queue_size=10)
    rospy.spin()