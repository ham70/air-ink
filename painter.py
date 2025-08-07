import cv2
import numpy as np
import os
from config import FRAME_WIDTH, FRAME_HEIGHT

class Painter():
  def __init__(self):
    self.imgCanvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)

  #methods ==================================================
  def paint(self, prev, curr, color, thickness):
    cv2.line(self.imgCanvas, prev, curr, color, thickness)

  def getCanvas(self):
    return self.imgCanvas
  
  def getInvCanvas(self):
    imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    return imgInv
  
  def save_canvas(self, path='output/drawing_canvas.png'):
    cv2.imwrite(path, self.canvas)