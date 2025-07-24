import numpy as np
import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT, DRAW_COLOR, CANVAS_COLOR

class Drawer:
    def __init__(self):
        self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        self.strokes = []           # List of strokes (each stroke is a list of points)
        self.current_stroke = []    # Ongoing stroke
        self.drawing = False        # Gesture state flag

    def update(self, is_drawing, point):
        if is_drawing:
            if not self.drawing:
                # Start a new stroke
                self.current_stroke = [point]
                self.drawing = True
            else:
                self.current_stroke.append(point)
        else:
            if self.drawing:
                # Gesture ended, save the stroke
                if len(self.current_stroke) > 1:
                    self.strokes.append(self.current_stroke)
                self.current_stroke = []
                self.drawing = False

    def draw_strokes(self):
        self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        for stroke in self.strokes:
            for i in range(1, len(stroke)):
                cv2.line(self.canvas, stroke[i-1], stroke[i], DRAW_COLOR, 2)
        # Also draw the current stroke in progress
        for i in range(1, len(self.current_stroke)):
            cv2.line(self.canvas, self.current_stroke[i-1], self.current_stroke[i], DRAW_COLOR, 2)

    def overlay(self, frame):
        self.draw_strokes()
        return cv2.addWeighted(frame, 1, self.canvas, 1, 0)

    def save_canvas(self, path='output/drawing_canvas.png'):
        cv2.imwrite(path, self.canvas)

    def clear(self):
        self.strokes = []
        self.current_stroke = []
        self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
