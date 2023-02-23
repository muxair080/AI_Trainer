import cv2
import mediapipe as mp
import time 
import math

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
    detectionCon=0.5, trackCon=0.5):
        self.mode = mode 
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = int(detectionCon)
        self.trackCon = int(trackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose 
        self.pose = self.mpPose.Pose()
        # self.mode, self.upBody,
        # self.smooth, self.detectionCon, self.trackCon

    
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                self.mpPose.POSE_CONNECTIONS)
        
        return img 
    

    def findPosition(self, img, draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:
            # myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)

                self.lmlist.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy),15,(255,0,0), cv2.FILLED)
        return self.lmlist


    # 
    def findAngle(self, img, p1,p2,p3, draw=True):
        """
        Find angle between different landmarks
        """
        # Right hand
        x1, y1 = self.lmlist[p1][1:] 
        x2, y2 = self.lmlist[p2][1:] 
        x3, y3 = self.lmlist[p3][1:] 


        # find angle
        angle = math.degrees(math.atan2((y3-y2), (x3-x2))- 
        math.atan2((y1-y2),(x1-x2)))
        if angle < 0:
            angle += 360
        print(angle)

        if draw:
            # Left Hanad
            cv2.line(img, (x1,y1),(x2, y2),(255,255,255),3)
            cv2.line(img, (x3,y3),(x2, y2),(255,255,255),3)
            cv2.circle(img, (x1,y1), 10, (255,0,0), cv2.FILLED)
            cv2.circle(img, (x1,y1), 15, (255,0,0), 2)
            cv2.circle(img, (x2,y2), 10, (255,0,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,0), 2)
            cv2.circle(img, (x3,y3), 10, (255,0,0), cv2.FILLED)
            cv2.circle(img, (x3,y3), 15, (255,0,0), 2)

            cv2.putText(img, str(int(angle)), (x2-20, y2+50),
            cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)
        
        return angle



    