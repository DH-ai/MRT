#!/usr/bin/env python

import cv2 
from cv2 import aruco
import numpy as np
import math
import random

class Node():
    def __init__(self,x,y):
        self.x =x
        self.y = y
        self.path_x = []
        self.path_y = []

def collision(x1,y1,x2,y2):
    color=[]
    x = list(np.arange(x1,x2,(x2-x1)/100))
    y = []
    print(f"Collison between ({x1},{y1}) and {({x2},{y2})}")
    for x_cord in x:
        y.append(((y2-y1)/(x2-x1))*(x_cord-x1) + y1)
    for i in range(len(x)):
        color.append(sampling_image[int(y[i]),int(x[i])]) 
        # cv2.circle(sampling_image,(int(x[i]),int(y[i])),1,(2*i),thickness=3) ## such a pain in the ass
    
    for i in range(len(color)-5):
       
        
        if color[i]==0:
            print("Collision returning with value of color ad ",color[i])
            return True
        
    return False
    # if (np.isin()) :
    #     return True
 

def checkCollisons(x1,y1,x2,y2):
    _,theta = dist_and_angle(x1,y1,x2,y2)
 
    x = x2+ stepSize*np.cos(theta)
    y = y2+ stepSize*np.sin(theta)
    print(x,y)
    # checking the direct connection between the Q_new and the final end
    if collision(x,y,end[1],end[0]):
        print("Cheking direct connection to the end .........")
        direcCon = False
    else:
        direcCon = True
    print(f"Direct Connection between {x,y} and end is {direcCon}")
    print("Checking the connection between our new node and the nearest node ")
    #checks the connection between the two nodes
    if collision(x,y,x2,y2):
        nodeCon = False
    else:
        nodeCon = True
    print(f"Direct Connection between {x,y} {x2,y2}is {direcCon}")

    return(x,y,direcCon,nodeCon) # return the coordinates for new node and direcCon-> if that new node directly connectes to the goal end or not and nodeCon-> if the rqandom genrated node has free path or not
    
def nearest_node(x,y):
    temp_dist=[]
    for i in range(len(node_list)):
        dist,_ = dist_and_angle(x,y,node_list[i].x,node_list[i].y)
        temp_dist.append(dist)
    return temp_dist.index(min(temp_dist)) # return the index of the node closest to the new node



def rnd_pnt():
    new_y = random.randint(0,len(frame))
    new_x = random.randint(0, len(frame[0]))
    return (new_x,new_y)


def dist_and_angle(x1,y1,x2,y2):
    dist = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
    angle = math.atan2(y1-y2,x1-x2)
    return (dist,angle)


frame = cv2.imread("src/rrt_assn/rrt_assn/arucoMarker.jpg") #(1080,1920,3)
start = (0,0)
end= (len(frame)-1,len(frame[0])-1)
stepSize = 200

node_list = [None]
node_list[0]= Node(start[0],start[1])
node_list[0].path_x.append(start[0])
node_list[0].path_y.append(start[1])
sampling_image = np.full((len(frame),len(frame[0])),255.0,dtype=np.uint8)
# sampling_image = cv2.cvtColor(sampling_image,cv2.COLOR_GRAY2BGR)

cv2.circle(frame,(start[1]+10,start[0]+10),10,(0,255,0),4)
cv2.circle(frame,(end[1]-10,end[0]-10),10,(0,0,255),4)
gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
arucoDict = cv2.aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters()
detectors = cv2.aruco.ArucoDetector(arucoDict,arucoParams)
corners, ids, rejectedMarkers = detectors.detectMarkers(gray_img)


if len(corners)>0:
    ids = ids.flatten()
    for (corner,id) in zip(corners,ids):
        corner =corner.reshape((4,2))
        (tl,tr,br,bl)= corner
        
        topLeft=(int(tl[0]),int(tl[1]))
        topRight=(int(tr[0]),int(tr[1]))
        bottomRight=(int(br[0]),int(br[1]))
        bottomLeft=(int(bl[0]),int(bl[1]))
        # for frame or orignal image
        cv2.line(frame,topLeft,topRight,(0,0,255),2)
        cv2.line(frame,topRight,bottomRight,(0,0,255),2)
        cv2.line(frame,bottomRight,bottomLeft,(0,0,255),2)
        cv2.line(frame,bottomLeft,topLeft,(0,0,255),2)
        points= np.array(
            [
            [int(tl[0]),int(tl[1])],
            [int(tr[0]),int(tr[1])],
            [int(br[0]),int(br[1])],
            [int(bl[0]),int(bl[1])]]
            )
        # for sampled image 
        # cv2.line(sampling_image,topLeft,topRight,0,2)
        # cv2.line(sampling_image,topRight,bottomRight,0,2)
        # cv2.line(sampling_image,bottomRight,bottomLeft,0,2)
        # cv2.line(sampling_image,bottomLeft,topLeft,0,2)
        cv2.fillPoly(sampling_image, [points], color=(0, 0, 0))

i =1
pathFound =False
while pathFound==False:
    # initialization of some random node 
    nx,ny = rnd_pnt()
    print("Random Points:",nx,ny) 
    # cv2.circle(frame,(nx,ny),3,0,lineType=8,thickness=2)

    # cv2.imshow("test",sampling_image)
    # # cv2.imshow("actual",frame)
    # cv2.waitKey(0)
    
 
    # getting the nearest node to that
    nearest_ind = nearest_node(nx,ny)
    nearest_x = node_list[nearest_ind].x
    nearest_y = node_list[nearest_ind].y
    print("Nearest node coordinates:","(",nearest_x,",",nearest_y,")","Index:",nearest_ind)

    # checking the connection 
    tx,ty,directCon,nodeCon = checkCollisons(nx,ny,nearest_x,nearest_y)
    print("random node position:",tx,ty,directCon,nodeCon)
    if directCon and nodeCon:
        
        node_list.append(i)
        node_list[i] = Node(tx,ty)
        node_list[i].path_x = node_list[nearest_ind].path_x.copy()
        node_list[i].path_y = node_list[nearest_ind].path_y.copy()
        node_list[i].path_x.append(tx)
        node_list[i].path_y.append(ty)

        # drawring the tree 
        cv2.circle(frame,(int(tx),int(ty)),3,(0),lineType=8,thickness=3)
        cv2.line(frame, (int(tx),int(ty)), (int(node_list[nearest_ind].x),int(node_list[nearest_ind].y)), (255,0,0), thickness=1, lineType=8)
       
        cv2.line(frame,(int(tx),int(ty)),(end[1],end[0]),(255,0,0),thickness=2) 

        for j in range(len(node_list[i].path_x)-1):
            cv2.line(frame, (int(node_list[i].path_x[j]),int(node_list[i].path_y[j])), (int(node_list[i].path_x[j+1]),int(node_list[i].path_y[j+1])), (255,0,0), thickness=2)
        # cv2.imshow("LOL",sampling_image)
        break

    elif nodeCon:
        print("Nodes connected")
        node_list.append(i)
        node_list[i] = Node(tx,ty)
        node_list[i].path_x = node_list[nearest_ind].path_x.copy()
        node_list[i].path_y = node_list[nearest_ind].path_y.copy()
        # print(i)cv2.waitKey(1)        
        # print(node_list[nearest_ind].path_y)
        node_list[i].path_x.append(tx)
        node_list[i].path_y.append(ty)
        i=i+1
        # display
        cv2.circle(sampling_image, (int(tx),int(ty)), 2,0,thickness=3, lineType=8)
        cv2.line(sampling_image, (int(tx),int(ty)), (int(node_list[nearest_ind].x),int(node_list[nearest_ind].y)), (0,255,0), thickness=2, lineType=8)
        # cv2.waitKey(0)
        
        
        continue

    else:
        print("No direct con. and no node con. :( Generating new rnd numbers")
     
        continue



# cv2.imshow("sampled",sampling_image)
cv2.imshow("orignal",frame)
cv2.waitKey(0)



# cv2.imwrite("sampling.jpg",sampling_image)
cv2.imwrite("frame.jpg",frame)


cv2.destroyAllWindows()
