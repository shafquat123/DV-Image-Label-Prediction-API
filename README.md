# DV-Image-Label-Prediction-API
This API was built to return 6 similar images to input image in conjunction with DV-SEINet-CACTACEAE-Dashboard project.

Prerequisites:
For Windows and macOS:
1) Python 3.x should be installed.
   a) To download Python 3.x, visit https://www.python.org/downloads/ and download the latest stable version for windows or macOS.

2) Google Chrome 81.x.x.x
   a) To download Google Chrome 81.x.x.x, visit https://www.google.com/chrome/

3) Install Flask.
	a) Open terminal.
	b) Run $ pip install Flask 

4) Install Pandas
	a) Open terminal
	b) Run $ pip install pandas

5) Install CORS
	a) Open terminal
	b) Run $ pip install flask-cors

6) Install skimage
	a) Open terminal
	b) Run $ pip install scikit-image

7) Install cv2
	a) Open terminal
	b) Run $ pip install opencv-pyt

8) Install numpy
	a) Open terminal
	b) Run $ pip install numpy

Installing:
1) Go to Google drive (https://drive.google.com/drive/u/1/folders/128q0V6S5msdIMM9ySAUQKLADAf1VsTk1) and download the images folder.

2) Add this images folder in the current directory (~/seinet_cactaceae_dashboard).

3) Go to Google drive (https://drive.google.com/drive/u/1/folders/1dZlOQZy-YOmViXPfsqH67-e5qkjAIBPO) and download the mwdbSql1.sqlite file.

4) Add this folder in the api folder in current directory. (~/seinet_cactaceae_dashboard/api).

5) Open terminal and change the directory to seinet_cactaceae_dashboard/api folder
	cd ~/seinet_cactaceae_dashboard/api

6) Run python ./api.py .

Data preprocessing:
All scripts related to data collection, cleaning, aggregation and preprocessing are available in the data_preprocessing folder.
The output files can also be found here.

Similarity matching:
Code for creating db and feature extraction is available in the similarity_matching folder.

Authors:
1) Dhriti Shah
2) Kasturi Adep
3) Omakar Sandeep Vedak
4) Shafquat Bakhtiyar
5) Shrimangal Sanjay Rewagad

Acknowledgments
http://swbiodiversity.org/seinet/ was used to get all data set.
