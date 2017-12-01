"""
- Sharad Bhat
- 2nd December, 2017
"""
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import ast

CLIENT_ID = ""

with open('key.txt', 'r') as f:
    CLIENT_ID = (f.readline()).strip()


app = ClarifaiApp(api_key=CLIENT_ID)

model = app.models.get('general-v1.3')
image = ClImage(file_obj=open('a.jpg', 'rb'))
r = model.predict([image])

for i in r["outputs"][0]["data"]["concepts"]:
    print(i["name"], i["value"])
