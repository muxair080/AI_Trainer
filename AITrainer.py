import cv2
import numpy as np 
import time 
import poseModule as pm
import math

# Set the desired window size
width = 640
height = 480

cap  = cv2.VideoCapture(0)

# Create a window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", width, height)


detector = pm.poseDetector()
cTime = 0
pTime = 0

# Count dumbels
count = 0
dir = 0
while True:
    success, img = cap.read()
    # img = cv2.imread('1.jpg')
    if not success:
        break

  
    # print(lmlist)

    # cv2.putText()
    img = cv2.resize(img, (1366, 768), interpolation=cv2.INTER_AREA)
    
    img = detector.findPose(img)
    lmlist = detector.findPosition(img, False)
    
   
    if len(lmlist) != 0:
        # Rigth Hand
        # angle = detector.findAngle(img, 12, 14, 16)
        # Left Hand
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (210,310),(0,100))
        print(angle, per)
        if per == 100:
                if dir == 0:
                    count +=0.5
                    dir = 1
                
        if per == 0:
                if dir == 1:
                    count +=0.5
                    dir = 0

        print(count)
        cv2.rectangle(img, (0, 450), (250, 720),(0,255,0), cv2.FILLED)
        cv2.putText(img, f'{str(int(count))}', (45,670),
         cv2.FONT_HERSHEY_PLAIN,15,(255,0,0),25)

    cTime = time.time()
    fps = 1 /(cTime - pTime)
    pTime = cTime 
    cv2.putText(img, f'FPS: {str(int(fps))}', (50,100), cv2.FONT_HERSHEY_PLAIN,
        5,(255,0,0),5)






    cv2.imshow('image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
