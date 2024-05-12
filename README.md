# Asphalt-Machine
**The files seen above have been developed by me (Gilberto Gonzalez) and David Perez for FIU'S Autonomous vehicle for asphalt laying that uses computer vision to detect potholes and avoid objects.**

Watch demos here:
 [AALaM Demo 1](https://www.youtube.com/shorts/Uu6aOz50WAc)
 [AALaM Demo 2](https://youtu.be/w-ecqEZU0mM?si=NLj24GkuHDqwQaUX)
## Pre-requisites to utlizing the files above are:

    ROS Noetic

    common_msgs (acquire from source)  // this ensures you have all message type dependencies

    realsense-ros (acquire from source)  // driver for the Intel RealSense Depth Camera

    roboclaw (acquire from source)  // driver for the roboclaw motor controller

## The launch files for these packages (on the base machine) is:

    roslaunch yolocamm asphalt_cam_diff.launch

**However, the YOLO program is needed to be run seperate:**

    rosrun yolocamm rosified_stop_detect.py 

## The launch files for these packages (on the remote machine) is:

    roslaunch realsense2_camera rs_camera.launch

    roslaunch roboclaw diffdrive.launch 
