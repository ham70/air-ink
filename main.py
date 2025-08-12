import cv2
import numpy as np
import time
import os
import hand_tracker as htm
import painter as paint
from config import FRAME_WIDTH, FRAME_HEIGHT, BRUSH_THICKNESS, ERASER_THICKNESS,CLICK_COOLDOWN
from api_service import img2Latex
from solver import processMath

#setting up headers
folderPath = 'header'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
  image = cv2.imread(f'{folderPath}/{imPath}')
  overlayList.append(image)
header = overlayList[0]

#setting up video capture
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

#setting up detector, painter, and previous coords
xp, yp = 0, 0
drawColor  = (255, 255, 255)
detector = htm.HandDetector(detectionCon=0.85)
painter = paint.Painter()
lastClickTime = 0
currSolution = None

while True:
  success, img = cap.read()#import image
  img = cv2.flip(img, 1)

  #find hand landmarks
  img = detector.findHands(img)
  lmList = detector.findPosition(img, draw=False)

  if len(lmList) != 0:
    x1, y1 = lmList[8][1:]#tip of index finger
    x2, y2 = lmList[12][1:]#tip of middle finger
    fingers = detector.fingersUp()#check which fingers are up

    #if select mode (2 fingers up)==============================================
    if fingers[1] and fingers[2]:
      xp, yp = x1, y1
      if y1 < 125: #at header
        currentTime = time.time()
        if currentTime - lastClickTime > CLICK_COOLDOWN:
          if 0 < x1 < 175:
            print('select color')
            canTouchHeader = False
          elif 275 < x1 < 425:
            header = overlayList[0]
            drawColor = (255, 255, 255)
            canTouchHeader = False
          elif 475 < x1 < 650:
            header = overlayList[1]
            drawColor = (0, 0, 0)
            canTouchHeader = False
          elif 800 < x1 < 1200:
            painter.saveCanvas()
            text = img2Latex()
            currSolution = processMath(text)
            print(currSolution)
          lastClickTime = currentTime
      cv2.rectangle(img, (x1, y1 - 18), (x2, y2 + 18), drawColor, cv2.FILLED)
    #draw mode (index finger only up)==============================================
    if fingers[1] and fingers[2] == False:
      if drawColor == (0,0,0):
        cv2.circle(img, (x1, y1), 10, drawColor, ERASER_THICKNESS)
      else:
        cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
      if xp == 0 and yp == 0:
        xp, yp = x1, y1

      if drawColor == (0,0,0):
        painter.paint((xp, yp), (x1, y1), drawColor, ERASER_THICKNESS)
        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, ERASER_THICKNESS)
      else:
        painter.paint((xp, yp), (x1, y1), drawColor, BRUSH_THICKNESS)
      xp, yp = x1, y1

  #get image canvas' and merge with main webcam image==============================================
  imgCanvas = painter.getCanvas()
  imgInv = painter.getInvCanvas()
  img = cv2.bitwise_and(img, imgInv)
  img = cv2.bitwise_or(img, imgCanvas)

  #setting header image
  img[0:125, 0:1280] = header

  cv2.imshow("image", img)
  #cv2.imshow("CanvasInv", imgInv)
  if cv2.waitKey(1) & 0xFF == 27:
    break
  if cv2.waitKey(1) & 0xFF == ord('e'):
    painter.resetCanvas()
cap.release()
cv2.destroyAllWindows()
painter.saveCanvas()