import cv2
import rclpy
from rclpy.node import Node
import numpy
from rrt_assn.srv import Aruco




class Vfn(Node):
    def __init__(self):
        super().__init__("VideoServer")
        self.srv = self.create_service(Aruco,'processor',self.corner_callback)

    def corner_callback(self,request,response):

        img = numpy.array(request.image)
        img = numpy.array(img.reshape(1080,1920,3))
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        cv2.imshow("lam",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return 
        corners, ids = self.aruco(img)
        corners = numpy.array(corners)
        corners = corners.flatten().tolist()
        corn= []
        for corner in corners:
            corn.append(int(corner))
        response.corners = corn
        ids = ids.flatten().tolist()
        
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