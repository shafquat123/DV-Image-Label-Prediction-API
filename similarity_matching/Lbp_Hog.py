import cv2
import glob
from skimage.transform import downscale_local_mean
from skimage.feature import hog
import sqlite3
import ntpath
import json
import numpy as np
from skimage import feature as ft
import skimage.feature
def hogimage():

    sqldbfile='mwdbSql1.sqlite'
    folderPath="C://Users//kastu//Downloads//DV//Project//images//*.*"
    #Connect Database
    conn = sqlite3.connect(sqldbfile)
    c = conn.cursor()
    #Delete previously stored data
    c.execute("DELETE FROM imageshog")
    conn.commit()
    #Store feature descriptors of each image in the folder
    for f in glob.glob(folderPath):
        img = cv2.imread(f)
        file_name=ntpath.basename(f)
        #print(file_name)
        #RGB to GRAY
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Downscale the image for simplicity
        downsample = downscale_local_mean(gray, (10, 10))
        #Calculate HOG Features
        fd, hog_image = hog(downsample, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(2, 2), visualize=True,multichannel=False)
        flist=np.asarray(fd).tolist()
        #Convert ndarray to json to store in sqlite database
        feature=json.dumps(flist)
        #Insert values to sqlite database
        try:
            c.execute("INSERT INTO imageshog VALUES (?,?);", (file_name,feature))
            conn.commit()
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format('name'))


def lbpimage():
    sqldbfile = 'mwdbSql1.sqlite'
    folderPath = "C://Users//kastu//Downloads//DV//Project//images//*.*"
    # Connect Database
    conn = sqlite3.connect(sqldbfile)
    c = conn.cursor()
    # Delete previously stored data
    c.execute("DELETE FROM imageslbp")
    conn.commit()
    # Store feature descriptors of each image in the folder
    for f in glob.glob(folderPath):
        img = cv2.imread(f)
        file_name=ntpath.basename(f)
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

        fd=np.asarray(hist).tolist()
        #Convert ndarray to Json representation to store in database
        feature = json.dumps(fd)

        # Insert values to sqlite database
        try:
            c.execute("INSERT INTO imageslbp VALUES (?,?);", (file_name,feature))
            conn.commit()
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format('name'))



if __name__== "__main__":
    name = input("Select a Model: 1) LBP 2)HOG ")
    if(name== '1'):
        lbpimage()
    elif(name== '2'):
        hogimage()
    else:
        print("Wrong option")