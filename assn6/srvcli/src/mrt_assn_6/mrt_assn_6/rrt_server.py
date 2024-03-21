import random
import math
import rclpy
import cv2
from rclpy.node import Node
from rrt_assn.srv import Aruco
import numpy


class Nodes():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.x_path = []
        self.y_path = []

class rrt_server(Node):
    def __init__(self):
        super().__init__("RrtServer")
        self.srv = self.create_service(Aruco,"processor",self.rrt_callback)
        self.node_list = [None]
        self.node_list[0] = Nodes(0,0)
        self.node_list[0].x_path.append(0)
        self.node_list[0].y_path.append(0)
        self.stepSize = 20


    def rrt_callback(self,request,response):
        img = numpy.array(request.image)
        img = numpy.array(img.reshape(1080,1920,3))
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        self.end = (len(img)-1,len(img[0])-1)
        corners, ids,frame = self.rrt(img)

        corners = numpy.array(corners)
        corners = corners.flatten().tolist()
        corn= []
        for corner in corners:
            corn.append(int(corner))
        response.corners = corn
        
        ids = ids.flatten().tolist()
        
        response.ids = ids
        
        cv2.imshow(frame)
        self.get_logger().info("send")
        
        return response

    
    def aruco(self, image):
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        arucoParams = cv2.aruco.DetectorParameters()
        detectors = cv2.aruco.ArucoDetector(arucoDict,arucoParams)
        corners, ids, rejectedCandidates = detectors.detectMarkers(gray_image)
        return corners ,ids
    
    def collison(self,x1,y1,x2,y2):
        color = []

        x = list(numpy.arange(x1,x2,(x2-x1)/100))
        y = []
        for x_cord in x:
            y.append(((y2-y1)/(x2-x1))*(x_cord-x1) + y1)
        for i in range(len(y)):
            
        
    
    
    def rnd_pnt(self):
        x = random.randint(0,len(self.sample_image))
        y = random.randint(0,len(self.sample_image[0]))
        return x,y
    
    
    
    def dist_and_angle(self,x1,y1,x2,y2)
        dist = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
        theta = math.atan2(y1-y2,x2-x1)
        # was facing progbelm with the angles lates come to i wast exchaing x1 and y1
        return dist,theta

    
    def nearest_node(self,x,y):
        
        temp_dist=[]
        for i in range(len(self.node_list)):
            dist,_ = self.dist_and_angle(x,y,self.node_list[i].x,self.node_list[i].y)
            temp_dist.append()
        return temp_dist.index(min(temp_dist))

    def checkCollisons(self,x1,y1,x2,y2):
        _, theta = self.dist_and_angle(x1,y1,x2,y2)

        x = x2 + self.stepSize*numpy.cos(theta)
        y = y2 + self.stepSize*numpy.sin(theta)

        if self.collison(x,y,self.end[1],self.end[0]):
            directCon = True
        else : 
            directCon = False
        if self.collison(x,y,x2,y2):
            nodeCon = True
        else:
            nodeCon = False

        return x,y,directCon,nodeCon

    def rrt(self,img):
        self.frame = img
        self.sample_image = numpy.full((len(img),len(img[0])),255.0,dtype=numpy.uint8,)
        self.corners, self.ids = self.aruco(img)
        if len(self.corners)>0:
            self.ids = self.ids.flatten()
            for corner,ids in zip(self.corners,self.ids):
                (tl,tr,br,bl) = corner
                topLeft=(int(tl[0]),int(tl[1]))
                topRight=(int(tr[0]),int(tr[1]))
                bottomRight=(int(br[0]),int(br[1]))
                bottomLeft=(int(bl[0]),int(bl[1]))
                # for frame or orignal image
                cv2.line(self.frame,topLeft,topRight,(0,0,255),2)
                cv2.line(self.frame,topRight,bottomRight,(0,0,255),2)
                cv2.line(self.frame,bottomRight,bottomLeft,(0,0,255),2)
                cv2.line(self.frame,bottomLeft,topLeft,(0,0,255),2)
                points= numpy.array(
                        [
                        [int(tl[0]),int(tl[1])],
                        [int(tr[0]),int(tr[1])],
                        [int(br[0]),int(br[1])],
                        [int(bl[0]),int(bl[1])]
                        ]
                    )
                # for sampled image 
                cv2.fillPoly(self.sample_image, [points], color=(0, 0, 0)) 
        self.i = 1
        self.pathFound = False
        while not self.pathFound :
            # genration of random points 
            nx,ny= random
            # getting the closses node to it 
            nearest_ind = self.nearest_node(nx,ny)
            nearest_x = self.node_list[nearest_ind].x
            nearest_y = self.node_list[nearest_ind].y

            tx,ty,directCon,nodeCon = self.checkCollisons(nx,ny,nearest_x,nearest_y)
            
