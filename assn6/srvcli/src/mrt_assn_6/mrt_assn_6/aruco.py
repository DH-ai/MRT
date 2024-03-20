import cv2
from cv2.aruco import DICT_6X6_100
from cv2 import aruco

frame = cv2.imread("lp1.jpg")



vid = cv2.VideoCapture("/home/dhruv/Desktop/MRT/rrt/feed/DSC_1797.MOV")

while (True):

    ret,frame = vid.read()
 
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    arucoDict = cv2.aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    arucoParams = cv2.aruco.DetectorParameters()
    detectors = cv2.aruco.ArucoDetector(arucoDict,arucoParams)
    
    corners, ids, rejectedCandidates = detectors.detectMarkers(gray_image)
    
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    
    # cv2.line(frame_markers,(0,0),(100,100),(0,0,0),5)
    # resized = cv2.resize(frame_markers,(900,600))
    


    for (crn,id )in zip(corners, ids.flatten()):
        
        crn=crn.reshape((4,2))
        # crn =crn.reshape((900,600))
        (tl,tr,br,bl)= crn
        
        topLeft=(int(tl[0]),int(tl[1]))
        topRight=(int(tr[0]),int(tr[1]))
        bottomRight=(int(br[0]),int(br[1]))
        bottomLeft=(int(bl[0]),int(bl[1]))
        cv2.line(frame_markers,topLeft,topRight,(0,0,255),2)
        cv2.line(frame_markers,topRight,bottomRight,(0,0,255),2)
        cv2.line(frame_markers,bottomRight,bottomLeft,(0,0,255),2)
        cv2.line(frame_markers,bottomLeft,topLeft,(0,0,255),2)
 



    cv2.imshow("lol",frame_markers)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break