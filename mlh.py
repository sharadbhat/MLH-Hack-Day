"""
- Sharad Bhat
- 2nd December, 2017
"""
import requests
import ast

base_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/"

subscription_key = ""
with open("key.txt", "r") as f:
    subscription_key = (f.readline()).strip()

choice = int(input("1. Upload missing person photo\n2. Upload found person photo\n3. List of missing persons\n"))

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key
}
params = {
'returnFaceId': 'true'
}

if choice == 1:

    body = open('a.jpg', 'rb').read()
    try:
        response = requests.post(url= base_url + "facelists/mlh/persistedFaces?userData=IDK.", data = body, headers = headers, params = params)
        a = ast.literal_eval(response.text)
        print(a["persistedFaceId"])
    except Exception as e:
        print('Error in getting Face ID:')
        print(e)

if choice == 2:
    faceId = ""
    body = open('a.jpg', 'rb').read()
    try:
        response = requests.post(url= base_url + "detect", data = body, headers = headers, params = params)
        a = ast.literal_eval(response.text)
        faceId = a[0]["faceId"]
    except Exception as e:
        print('Error in getting Face ID:')
        print(e)

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    try:
        data = "{\"faceId\" : \""+ faceId +"\", \"faceListId\" : \"mlh\", \"mode\" : \"matchFace\"}"
        r = requests.post(url=base_url + "findsimilars", headers=headers, data=data)
        a = ast.literal_eval(r.text)
        print(a)
    except Exception as e:
        print("Error in finding similar:")
        print(e)

if choice == 3:
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    try:
        r = requests.get(url=base_url + "facelists/mlh", headers=headers)
        a = ast.literal_eval(r.text)
        for i in a["persistedFaces"]:
            print(i["persistedFaceId"])
    except Exception as e:
        print("Error in getting face lists:")
        print(e)
