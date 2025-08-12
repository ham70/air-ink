import requests
import json
import os
import cv2
import numpy as np
from PIL import Image
from dotenv import load_dotenv

load_dotenv() 

APP_KEY = os.getenv('KEY')
APP_ID = os.getenv('ID')

def preprocessImage(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img)
    
    kernel = np.ones((2,2), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    
    return Image.fromarray(img)

def img2Latex():
  path = 'output/drawing_canvas.png'
  r = requests.post("https://api.mathpix.com/v3/text",
    files={"file": open(path,"rb")},
    data={
      "options_json": json.dumps({
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
      })
    },
    headers={
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
  )
  response_data = r.json()
  print(json.dumps(response_data, indent=4, sort_keys=True))
  return response_data.get("latex_styled")