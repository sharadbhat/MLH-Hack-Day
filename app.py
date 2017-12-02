from flask import Flask, render_template, request, send_file, url_for, redirect
import requests
import ast
import base64
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

subscription_key = ""
with open("key.txt", "r") as f:
    subscription_key = (f.readline()).strip()

base_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/"

@app.route("/")
def main_page():
    """
    - Displays list of missing persons.
    """
    if request.method == 'GET':
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        r = requests.get(url=base_url + "facelists/mlh", headers=headers)
        a = ast.literal_eval(r.text)
        face_IDs = []
        for i in a["persistedFaces"]:
            face_IDs.append((i["persistedFaceId"]))
        return render_template("home.html", IDs = face_IDs)


def get_ID():
    """
    """
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
    'returnFaceId': 'true'
    }
    body = open("./static/images/a.jpg", 'rb').read()
    response = requests.post(url= base_url + "facelists/mlh/persistedFaces?userData=IDK.", data = body, headers = headers, params = params)
    a = ast.literal_eval(response.text)
    print(a)
    filename = (a["persistedFaceId"])
    return filename

@app.route("/report", methods = ['GET', 'POST'])
def report_missing():
    if request.method == 'GET':
        return render_template("report-missing.html")

    if request.method == 'POST':
        file = request.files['file']
        file.save("./static/images/{}.jpg".format("a"))
        os.rename("./static/images/a.jpg", "./static/images/{}.jpg".format(get_ID()))
        return redirect(url_for("main_page"))


@app.route("/found", methods = ['GET', 'POST'])
def found():
    if request.method == 'GET':
        return render_template("found.html")

    if request.method == 'POST':
        file = request.files['file']
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        params = {
        'returnFaceId': 'true'
        }
        response = requests.post(url= base_url + "detect", data = file, headers = headers, params = params)
        a = ast.literal_eval(response.text)
        faceId = a[0]["faceId"]



        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        data = "{\"faceId\" : \""+ faceId +"\", \"faceListId\" : \"mlh\", \"mode\" : \"matchFace\"}"
        r = requests.post(url=base_url + "findsimilars", headers=headers, data=data)
        a = ast.literal_eval(r.text)
        matches = []
        for i in a:
            if i['confidence'] > 0.60:
                matches.append(i['persistedFaceId'])
        return render_template("matches.html", matches = matches)


if __name__ == '__main__':
    app.run(port=9000, debug=True)
