import cv2
import rclpy
from rclpy.node import Node
# from cv_bridge import CvBridge
# from sensor_msgs.msg import Image
from rrt_assn.srv import Aruco


import numpy
# print(rrt_assn)
 # takes images return corners

class Vfn(Node):
    def __init__(self):
        super().__init__("VideoServer")
        self.srv = self.create_service(Aruco,'processor',self.corner_callback)

    def corner_callback(self,request,response):

        img = numpy.array(request.image)
        img = numpy.array(img.reshape(1080,1920,3))
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        # print(f"img shape =  {img.shape} \n type = {type(img)}")

        corners, ids = self.aruco(img)
        corners = numpy.array(corners)
        corners = corners.flatten().tolist()
        corn= []
        for corner in corners:
            corn.append(int(corner))
        # print(type(corners))
        # print(corners)
        response.corners = corn
        ids = ids.flatten().tolist()
        # print(ids,type(ids)) 
        
        response.ids = ids
        self.get_logger().info("send")
        return response
    
    
    def aruco(self, image):
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        arucoParams = cv2.aruco.DetectorParameters()
        detectors = cv2.aruco.ArucoDetector(arucoDict,arucoParams)
        corners, ids, rejectedCandidates = detectors.detectMarkers(gray_image)
        return corners ,ids
    

def main(args=None):
    rclpy.init(args=args)
    server = Vfn()
    rclpy.spin(server)
    rclpy.shutdown()


if __name__ == '__main__':
    main()