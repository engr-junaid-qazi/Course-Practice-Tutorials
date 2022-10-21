import cv2
import mediapipe as mp
from pyfirmata import Arduino
from time import sleep
 
board = Arduino('Select your COM port')
#Arduino define pins
digitalPins =[7, 6, 5, 4]  

for pins in digitalPins:
    board.digital[pins].write(1)

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

cap.set(10, 250)#brightness
cap.set(11, 50)#Contrast
cap.set(12, 100)#saturation

class handDetector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity=1,detectionCon=0.75, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
										self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
                                
        
    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (178, 102, 255), cv2.FILLED)
        return lmlist

counter, counter1, counter2, counter3 = 0,0,0,0
flag, flag1, flag2, flag3 = 0,0,0,0

detector = handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    y1, y2 = 15, 80
    grey_color = (211,219,218)
    if lmList:

        tip8_x, tip8_y= lmList[8][1], lmList[8][2]  # tracking tip of index finger
        #button 1
        if tip8_x > 25 and tip8_x < 65 and tip8_y > 28 and tip8_y < 62:
            counter += 1
            cv2.rectangle(img, (15,y1),(85,y2), (255, 255, 0), cv2.FILLED)
            if counter == 1:
                flag = not flag
        else :
            counter = 0
            if flag:
                board.digital[digitalPins[0]].write(0)
                cv2.rectangle(img,(15,y1),(85,y2),(76,138,246),cv2.FILLED)
                cv2.putText(img, "BULB1", (25, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
            else:
                board.digital[digitalPins[0]].write(1)
                cv2.rectangle(img,(15,y1),(85,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "BULB1", (25, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
        
        #button 2
        if tip8_x > 115 and tip8_x < 155 and tip8_y > 28 and tip8_y < 62:
            counter1 += 1
            cv2.rectangle(img, (175,y1),(105,y2), (255, 255, 0), cv2.FILLED)
            if counter1 == 1:
                flag1 = not flag1
        else :
            counter1 = 0
            if flag1:
                board.digital[digitalPins[1]].write(0)
                cv2.rectangle(img,(175,y1),(105,y2),(77,198,254),cv2.FILLED)
                cv2.putText(img, "BULB2", (115, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
            else:
                board.digital[digitalPins[1]].write(1)
                cv2.rectangle(img,(175,y1),(105,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "BULB2", (115, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
        #button 3
        if tip8_x > 200 and tip8_x < 245 and tip8_y > 28 and tip8_y < 62:
            counter2 += 1
            cv2.rectangle(img, (265,y1),(195,y2),(255, 255, 0), cv2.FILLED)
            if counter2 == 1:
                flag2 = not flag2
        else :
            counter2 = 0
            if flag2:
                board.digital[digitalPins[2]].write(0)
                cv2.rectangle(img,(265,y1),(195,y2),(135,186,118),cv2.FILLED)
                cv2.putText(img, "BULB3", (205, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
            else:
                board.digital[digitalPins[2]].write(1)
                cv2.rectangle(img,(265,y1),(195,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "BULB3", (205, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
        #button 4
        if tip8_x > 295 and tip8_x < 335 and tip8_y > 28 and tip8_y < 62:
            counter3 += 1
            cv2.rectangle(img, (355,y1),(285,y2),(255, 255, 0), cv2.FILLED)
            if counter3 == 1:
                flag3 = not flag3
        else :
            counter3 = 0
            if flag3:
                board.digital[digitalPins[3]].write(0)
                cv2.rectangle(img,(355,y1),(285,y2),(127,129,29),cv2.FILLED)
                cv2.putText(img, "BULB4", (295, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
            else:
                board.digital[digitalPins[3]].write(1)
                cv2.rectangle(img,(355,y1),(285,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "BULB4", (295, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
            
        # Exit button    
        cv2.rectangle(img,(600,y1),(530,y2),(102,102,255),cv2.FILLED)
        cv2.putText(img, "EXIT", (550, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
        #EXIT by index finger
        cv2.circle(img, (tip8_x, tip8_y), 10, (255, 255, 51), cv2.FILLED)
        if tip8_x > 550 and tip8_x < 590 and tip8_y > 28 and tip8_y < 62:
            cv2.destroyAllWindows()
            cap.release()
            break
        
        
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
