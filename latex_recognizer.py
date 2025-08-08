import cv2
import numpy as np
from PIL import Image
from pix2tex.cli import LatexOCR

def preprocess_math_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img)
    
    kernel = np.ones((2,2), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    
    return Image.fromarray(img)

def img2Latex():
  img_path = 'output/drawing_canvas.png'
  
  #check if image exists and has content
  img = Image.open(img_path)
  if img.size[0] < 100 or img.size[1] < 50:
      return "Image too small for OCR"
  
  processed_img = preprocess_math_image(img_path)
  processed_img.save('output/processed_for_ocr.png')
  
  model = LatexOCR()
  result = model(processed_img)
  print(f"Raw OCR result: {result}")
  
  return result