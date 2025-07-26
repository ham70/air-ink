import mediapipe as mp
import cv2

class HandTracker():
  def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
    self.mode = mode
    self.maxHands = maxHands
    self.detectionCon = detectionCon
    self.trackCon = trackCon

    self.mphands = mp.solutions.hands
    self.hands = self.mphands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
    self.mp_draw = mp.solutions.drawing_utils
  
  def findHands(self, img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)

    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        if draw:
          self.mp_draw.draw_landmarks(img, handLms)
        # for id, lm in enumerate(handLms.landmark):
        #   h, w, c = img.shape
        #   cx, cy = int(lm.x  * w), int(lm.y * h)
        #   print(id, cx, cy)
        #   cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    return img
  def finPosition(self, img, handNo=8, draw=True):
    lmList = []
    if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNo]
      for id, lm in enumerate(myHand.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x  * w), int(lm.y * h)
        lmList.append([id, cx, cy])
        if draw:
          cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

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
