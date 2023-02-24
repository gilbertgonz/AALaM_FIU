#!/usr/bin/env python3

import rospy
from bboxarray.msg import custom
from geometry_msgs.msg import Twist


def callback_bbox(data):
    global x1, x2, y1, y2, x_val

    # rospy.loginfo(rospy.get_name()+ "I heard %s", data.data)
    bbox = data.data 
    x1, x2, y1, y2 = bbox[0], bbox[2], bbox[1], bbox[3]
    x_val = (x1 + x2) / 2
    
def callback_obs(data):
    move= Twist()
    speed = 0.15
    size = 640
    ranges = 40
    weight = 0.8
    distance = 1200
    range_plus = (size/2)+ranges
    range_minus = (size/2)-ranges
    r = rospy.Rate(1)
    obs_dist = data.data
    #rospy.loginfo(rospy.get_name()+ " I heard %s", data.data)

    tl, tm, tr, l, m, r, bl, bm, br = obs_dist[0], obs_dist[1], obs_dist[2], obs_dist[3], obs_dist[4], obs_dist[5], obs_dist[6], obs_dist[7], obs_dist[8]


    if tl > distance and tm > distance and tr > distance and l > distance and m > distance and r > distance and br > distance and bm > distance and bl > distance:
        if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:     #Target following mode
            if y2 < 475:
                if x_val > range_plus: # When vehicle is the left of the target
                    move.linear.x = speed * weight
                    move.angular.z = -speed
                    rospy.loginfo("Twist Right")
                    step_cmd_vel.publish(move)
                elif x_val < range_minus: # When vehicle is the right of the target
                    move.linear.x = speed
                    move.angular.y = speed
                    rospy.loginfo("Twist Left")
                    step_cmd_vel.publish(move)
                elif range_minus < x_val <range_plus:
                    move.linear.x = speed * weight
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
            move.angular.z = 0
            rospy.loginfo("No target detected")
            step_cmd_vel.publish(move)

    ### Implementing a similar concept to the Braitenburg algorithm if there is objects to the right, left, or middle ###
    elif tl < distance  or l < distance or bl < distance:
        move.linear.x = speed 
        move.angular.z = -speed
        rospy.loginfo("Avoid obstacle to your left, turn right")
        step_cmd_vel.publish(move)    
    elif tr < distance or r < distance or br < distance:
        move.linear.x = speed 
        move.angular.z = speed
        rospy.loginfo("Avoid obstacle to your right, turn left")
        step_cmd_vel.publish(move)
    elif tm < distance  or m < distance or bm < distance:
        if tl < distance  or l < distance or bl < distance:
            move.linear.x = speed 
            move.angular.z = -speed
            rospy.loginfo("Avoid obstacle in the middle, turn right")
            step_cmd_vel.publish(move)  
        if tr < distance or r < distance or br < distance:
            move.linear.x = speed 
            move.angular.z = speed
            rospy.loginfo("Avoid obstacle in the middle, turn left")
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
