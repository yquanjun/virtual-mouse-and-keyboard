import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pyautogui import press, typewrite, hotkey
import win32api, win32con
import ctypes
import numpy as np

cap = cv2.VideoCapture(0)


# set cv2 window size
wCam = 1280
hCam = 720

cap.set(3,wCam)
cap.set(4,hCam)

# get screen size
user32 = ctypes.windll.user32
wScr,hScr = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# set values to smoothen mouse
clocX,plocX,clocY,plocY = 0,0,0,0
smoothening = 7

# cv2.namedWindow('keyboard', cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty('keyboard', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Hand detection AI with 80% confidence
detector = HandDetector(detectionCon=0.8, maxHands=2)

keyboardcaps = True

# class to store keyboard button
class Button():
    def __init__ (self,pos,text,size):
        self.pos = pos
        self.size = size
        self.text = text

# function to draw buttons
def drawall(img,buttonList):
    for button in buttonList:
        x1,y1 = button.pos
        x2 = x1 + button.size[0]
        y2 = y1 + button.size[1]
        # x1,y1 ------
        # |          |
        # |          |
        # |          |
        # --------x2,y2

        # draw rectangle
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),cv2.FILLED)

        # draw the text 
        cv2.putText(img,button.text,(x1+5,y1+30), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    return img

# function to set keys
def setkeys():
    keys = []
    if(keyboardcaps == True):
        # caps
        keys = [
        ['backspace','Q','W','E','R','T','Y','U','I','O','P'],
        ['enter','A','S','D','F','G','H','J','K','L',';'],
        ['caps','Z','X','C','V','B','N','M',',','.','/']
      ]
    else:
        # no caps
        keys = [
        ['backspace','q','w','e','r','t','y','u','i','o','p'],
        ['enter','a','s','d','f','g','h','j','k','l',';'],
        ['caps','z','x','c','v','b','n','m',',','.','/']
      ]
    buttonList = []
    
    # add in the button class
    # for loop to cycle the 3 arrays
    for i in range(0,3):
        # enumerate to get x count
        for x, key in enumerate(keys[i]):
            if(x == 0):
                buttonList.append(Button([50*x+50,50 * (i+1)] , key, [200,40]))
            else:
                buttonList.append(Button([50*x+210,50 * (i+1)] , key, [40,40]))
    return buttonList

# click the mouse
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    sleep(0.35)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while True:

    # get the image from webcam
    success, img = cap.read()

    # flip the image horizontally
    img = cv2.flip(img, 1)

    # find the hands
    hands, img = detector.findHands(img,flipType=False)

    # add the box around the hands
    # lmList, bboxInfo = detector.findPosition(img)

    # draw the keyboard buttons
    buttonList = setkeys()
    img = drawall(img,buttonList)

    # if there is a hand detected
    if hands:
        # hand1 = hands[0]
        # lmList1 = hand1["lmList"]
        # bbox1 = hand1["bbox"]

        # loop all hands available (to enable 2 hands at the same time)
        for hand in hands:
            fingersup = detector.fingersUp(hand)
            length,info,img = detector.findDistance(hand["lmList"][8],hand["lmList"][12],img)
            print(length)
            # mouse control
            if(hand["type"] == "Right"):
                if(fingersup == [0,1,0,0,0]):
                    x3 = np.interp(hand["lmList"][8][0] , (0,wCam), (0,wScr))
                    y3 = np.interp(hand["lmList"][8][1], (0,hCam), (0,hScr))

                    # to smoothening the mouse cursor movements
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) /smoothening

                    # move mouse cursor
                    win32api.SetCursorPos((int(clocX),int(clocY)))

                    # to save previous mouse coordinates
                    plocX = clocX
                    plocY = clocY
                
                if(length<30 and fingersup == [0,1,1,0,0]):
                    click()

            for button in buttonList:
                x1, y1 = button.pos
                x2 = x1 + button.size[0]
                y2 = y1 + button.size[1]

                if x1< hand["lmList"][8][0] < x2 and y1 < hand["lmList"][8][1] < y2:
                    # draw rectangle
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),cv2.FILLED)

                    # draw the text 
                    cv2.putText(img,button.text,(x1+5,y1+30), cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
                    
                    if(length<30 and fingersup == [1,1,1,0,0]):
                        if(button.text == "caps"):
                            keyboardcaps = not keyboardcaps
                        else:
                            press(button.text)



    # show the image captured (webcam) using cv2
    cv2.imshow("keyboard" , img)

    # cv2.waitKey(1) basically to make live video
    cv2.waitKey(1)