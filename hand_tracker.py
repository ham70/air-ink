import mediapipe as mp
import cv2
import time
import math
import numpy as np

class HandTracker():
  def __init__(self, mode=False, maxHands=2):
    self.mode = mode
    self.maxHands = maxHands
    #self.detectionCon = detectionCon
    #self.trackCon = trackCon

    self.mphands = mp.solutions.hands
    self.hands = self.mphands.Hands(self.mode, self.maxHands)
    self.mp_draw = mp.solutions.drawing_utils

    self.tipId = [4, 8, 12, 16, 20]
  
  def findHands(self, img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)

    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        if draw:
          self.mp_draw.draw_landmarks(img, handLms)
    return img
  
  def findPosition(self, img, handNo=8, draw=True):
    self.lmList = []
    if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNo]
      for id, lm in enumerate(myHand.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x  * w), int(lm.y * h)
        self.lmList.append([id, cx, cy])
        if draw:
          cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    return self.lmList

  def fingersUp(self):
    fingers = []
    if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
      fingers.append(1)
    else:
      fingers.append(0)

    # Fingers
    for id in range(1, 5):
      if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
        fingers.append(1)
      else:
        fingers.append(0)
    return fingers

  def process(self, frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return self.hands.process(rgb)

  def get_landmarks(self, hand_landmarks, frame_shape):
    h, w, _ = frame_shape
    return {
      4: (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)),
      8: (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)),
      12: (int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h)),
    }

  def draw_landmarks(self, frame, hand_landmarks):
    self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandTracker()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
        (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
