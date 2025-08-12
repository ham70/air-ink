import requests
import json
import os

APP_KEY = os.getenv('KEY')
APP_ID = os.getenv('ID')

def image2latex(path):
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
  print(json.dumps(r.json(), indent=4, sort_keys=True))