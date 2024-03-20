import cv2
import rclpy 
from rclpy.node import Node
import rrt_assn.srv import Aruco
import sys




class VideoClient(Node):
    def __init__(self):
        super().__init__("VideoClient")
        self.cli = self.create_client(Aruco,'processor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Aruco.Request()

    def send_request(self,image):
        self.req = image
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
vid = cv2.VideoCapture("assn6/srvcli/src/mrt_assn_6/mrt_assn_6/feed/DSC_1797.MOV")
def main(args = None):
    rclpy.init(args=args)
    client = VideoClient()
    ret, frame = vid.read()
        
    response = client.send_request(frame)
    client.get_logger().info(
        response[0]
    )
    client.destroy_node()
    rclpy.shutdown()

if __name__ =="__main__":
    main()