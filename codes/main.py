import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

# 3 = edit video width
cap.set(3,1208)

#  4 = edit video height
cap.set(4,728)

# Hand detection AI with 80% confidence
detector = HandDetector(detectionCon=0.8)

while True:
    # get the image from webcam
    success, img = cap.read()

    # find the hands
    img = detector.findHands(img)

    # add the box around the hands
    lmList, bboxInfo = detector.findPosition(img)

    # show the image captured (webcam) using cv2
    cv2.imshow("Image" , img)

    # cv2.waitKey(1) basically to make live video
    cv2.waitKey(1)