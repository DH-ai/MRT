import cv2
import rclpy 
from rclpy.node import Node
from rrt_assn.srv import Aruco
import sys

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
# Aruco = None

class VideoClient(Node):
    def __init__(self):
        super().__init__("VideoClient")
        self.cli = self.create_client(Aruco,'processor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Aruco.Request()

    def send_request(self,image):
        # print(type(image))
        # ros_image = CvBridge.cv2_to_imgmsg(image,)
        
        self.req.image = image
        
        # req = [1,2,22,2,2,2,2,2,2,2,2,2]
        
        future = self.cli.call_async(self.req)
        
        
        
        rclpy.spin_until_future_complete(self, future)


        if future.result() is not None:
            return future.result()  
        else:
            self.get_logger().error("Service call failed: %r" % (future.exception(),))
            return None




vid = cv2.VideoCapture("/home/dhruv/Desktop/MRT/assn6/srvcli/src/mrt_assn_6/mrt_assn_6/feed/DSC_1797.MOV")
def main(args = None):
    rclpy.init(args=args)
    client = VideoClient()
    while True:
            
        ret, frame = vid.read()
        frame = frame.flatten().tolist()
        corners = client.send_request(frame)
        if corners==None:
            break
        print(corners.ids)
    client.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()
    