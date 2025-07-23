import mediapipe as mp
import cv2

class HandTracker:
  def __init__(self):
    self.hands = mp.solutions.hands.Hands()
    self.mp_draw = mp.solutions.drawing_utils

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
