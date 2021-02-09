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
from skimage.io import imread
from skimage import feature as ft
import skimage.feature
import os

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
    dets = pandas.read_csv(r".\pro_combined.csv", encoding='latin-1')
    for i in d:
        print(i)
        n = i.split('.')[0]
        ixd = int(n)
        row = dets.iloc[ixd]
        sim = 100 - int(100 / (1 + d[i]))
        if j < k:
            ele = {
                'imgname': n,
                'name': dets.iloc[ixd]['scientificName'],
                'genus': dets.iloc[ixd]['genus'],
                'country': dets.iloc[ixd]['country'],
                'state': dets.iloc[ixd]['stateProvince'],
                'county': dets.iloc[ixd]['county'],
                'value': sim
            }
            print(ele)
            res.append(ele)
        else:
            return res
        j=j+1

def chi2_distance(histA, histB, eps=1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                      for (a, b) in zip(histA, histB)])

    # return the chi-squared distance
    return d

def euclidean0_1(vector1, vector2):

    d=math.sqrt(np.sum([((a-b) ** 2) for (a,b) in zip(vector1,vector2)]))
    return d
def hogimage():
    sqldbfile = 'mwdbSql1.sqlite'
    name = input("enter the name of the image file: ")
    k = int(input("enter k: "))
    data = {}
    x = {}
    y={}
    conn = sqlite3.connect(sqldbfile)
    c = conn.cursor()
    # img = cv2.imread("C://Users//hp//Desktop//MWDB//Hands//Hands//Few" + name)

    # Retrieve Query Image Features
    c.execute("SELECT * from imageshog where name= (?)", [name])
    fd_query = c.fetchall()
    fd_load1 = json.loads(fd_query[0][1])
    fd1 = np.array(fd_load1)
    print(fd1)
    conn.commit()
    save = {}
    save_eu={}

    # Retrieve all the Image Features except Query Image
    c.execute("SELECT * from imageshog where name != (?)", [name])
    rows = c.fetchall()
    for row in rows:
        fd_load = json.loads(row[1])
        fd = np.array(fd_load)

        # Calculate Distance Metric and Compare for k similar images
        data[row[0]] = fd
        score = chi2_distance(fd1, data[row[0]])
        distance = euclidean0_1(fd1, data[row[0]])
        x[row[0]] = score
        y[row[0]]= distance
    save = sorted(x.items(), key=lambda y: y[1])
    save_eu = sorted(y.items(), key=lambda z: z[1])
    print("Chi Squared:")
    j=0
    for i in save:

        if j<k:
            print(i)
        else:
            break;
        j=j+1
    print("Eucledian:")
    j=0
    for i in save_eu:

        if j<k:
            print(i)
        else:
            break;
        j=j+1



if __name__== "__main__":
    name = input("Which Model: 1) LBP 2)HOG ")
    path = os.path.join(os.getcwd(), 'images', '2.jpg');
    if(name== '1'):
        lbpimage(path)
    elif(name== '2'):
        hogimage()
    else:
        print("Wrong option")