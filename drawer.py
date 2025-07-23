import numpy as np
import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT, DRAW_COLOR, CANVAS_COLOR

class Drawer:
  def __init__(self):
    self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    self.points = []

  def add_point(self, point):
    self.points.append(point)
    if len(self.points) > 1:
      cv2.line(self.canvas, self.points[-2], self.points[-1], DRAW_COLOR, 2)

  def overlay(self, frame):
    return cv2.addWeighted(frame, 1, self.canvas, 1, 0)

  def save_canvas(self, path='output/drawing_canvas.png'):
    cv2.imwrite(path, self.canvas)
