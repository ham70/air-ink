import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT, TOUCH_THRESHOLD
from utils import distance
from hand_tracker import HandTracker
from drawer import Drawer
import os

os.makedirs("output", exist_ok=True)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

tracker = HandTracker()
drawer = Drawer()

while True:
  ret, frame = cap.read()
  frame = cv2.flip(frame, 1)
  results = tracker.process(frame)

  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      lm = tracker.get_landmarks(hand_landmarks, frame.shape)
      tracker.draw_landmarks(frame, hand_landmarks)

      if distance(lm[8], lm[12]) < TOUCH_THRESHOLD:
        drawer.add_point(lm[8])
        cv2.circle(frame, lm[8], 10, (0, 255, 0), cv2.FILLED)
      else:
        cv2.circle(frame, lm[8], 10, (0, 0, 255), 2)

  combined = drawer.overlay(frame)
  cv2.imshow("Virtual Canvas", combined)

  if cv2.waitKey(1) & 0xFF == 27:
    break

drawer.save_canvas()
cap.release()
cv2.destroyAllWindows()
