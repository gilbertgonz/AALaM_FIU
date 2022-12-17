# Asphalt-Machine
**The files seen above have been developed by me (Gilberto Gonzalez) and David Perez for FIU'S Autonomous vehicle for asphalt laying that uses computer vision to detect potholes and avoid objects.**

## Pre-requisites to utlizing the files above are:

ROS Kinetic

common_msgs (acquire from source)  // this ensures you have all message type dependencies

realsense-ros (acquire from source)  // driver for the Intel RealSense Depth Camera

roboclaw (acquire from source)  // driver for the roboclaw motor controller

## The launch file for these packages is:

roslaunch yolocamm asphalt_cam_diff.launch

**However, the YOLO program is needed to be run seperate because it does not work in the launch file for some reason:**

rosrun yolocamm rosified_stop_detect.py 
