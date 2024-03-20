import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

import src.rrt_assn.aruco_interface as interface

print(interface)
 # takes images return corners

class Vfn(Node):
    def __init__(self):
        super.__init__("VideoFeed")
        self.srv = self.create_service("")