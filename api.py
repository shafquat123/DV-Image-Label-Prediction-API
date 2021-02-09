import flask
import sqlite3
import json
import numpy as np
import math
import pandas
import cv2
import glob
from skimage.transform import downscale_local_mean
from skimage.feature import hog
import ntpath
from skimage import feature as ft
from skimage.io import imread
import skimage.feature
from flask import request, jsonify
from flask_cors import CORS
import os

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/images', methods=['GET'])
def getimages():
    try:
        path = request.args['path']
        file = os.path.join(os.getcwd(), 'images', path)
        print(file)
        result = [lbpimage(file)]
    except IOError:
        return "error"
    response = flask.jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def lbpimage(file):
    sqldbfile = 'mwdbSql1.sqlite'
    img = imread(file)
    k = 6
    data={}
    x={}
    y={}
    conn = sqlite3.connect(sqldbfile)
    c = conn.cursor()
    conn.commit()
    save = {}
    save_eu={}

    #RGB to GrayScale
    eps = 1e-7
    hist = []
    # Initializing LBP settings - radius and number of points
    radius = 3
    numPoints = 8 * radius
    gray = cv2.cvtColor(img, cv2.cv2.COLOR_BGR2GRAY)
    lbp = ft.local_binary_pattern(gray, numPoints, radius, method="uniform")
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, numPoints + 3), range=(0, numPoints + 2))
    # normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + eps)

    img_fd = np.asarray(hist).tolist()

    # Retrieve all the Image Features except Query Image
    c.execute("SELECT * from imageslbp")
    rows = c.fetchall()

    # Calculate Distance Metric and Compare for k similar images
    for row in rows:
      fd_load = json.loads(row[1])
      fd = np.array(fd_load)
      data[row[0]]=fd
      score = chi2_distance(img_fd,data[row[0]])
      #distance= euclidean0_1(img_fd, data[row[0]])

      x[row[0]]=score
      #y[row[0]]=distance
    save = sorted(x.items(), key=lambda z: z[1])
    #save_eu = sorted(y.items(), key=lambda z: z[1])

    print("Chi Squared:")
    j=0

    res = []
    d = dict(save)
    dets = pandas.read_csv(r"./pro_combined.csv", encoding='latin-1')
    for i in d:
        print(i)
        n = i.split('.')[0]
        ixd = int(n)
        row = dets.iloc[ixd]
        sim = int(100 / (1 + d[i]))
        if j < k:
            ele = {
                "imgname": n,
                "name": dets.iloc[ixd]['scientificName'],
                "genus": dets.iloc[ixd]['genus'],
                "country": dets.iloc[ixd]['country'],
                "state": dets.iloc[ixd]['stateProvince'],
                "county": dets.iloc[ixd]['county'],
                "value": (j + 1) * 20,
                "similarity": sim
            }
            print(ele)
            res.append(ele)
        else:
            print(res)
            return res
        j=j+1

def chi2_distance(histA, histB, eps=1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                      for (a, b) in zip(histA, histB)])

    # return the chi-squared distance
    return d

app.run(host='0.0.0.0', port=8001)
