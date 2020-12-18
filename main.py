
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import Response
from flask import render_template

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

import os

import cv2
import numpy as np
import pickle

# importing the required module 
import matplotlib.pyplot as plt 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage, firestore
from firebase_admin import db

import requests

from datetime import datetime

firecreds = {
"type": "service_account",
"project_id": "hemarays",
"private_key_id": "c4072f415f668e28fae417e0e5c3f4bfb020b1c1",
"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCoNoYkIARKVey2\niihIOuNDDDiexlQ/8fkjafWbf8KjzWjMLgg6GZcXy94RdzqLwXywEioq8FJfKwfs\ns0Ct8MMaR6wSwy0XMTBorBAAUDQEfLA5Nc/GWsJYkI3Kr4oYE0Wt3wiMxB9FtlhX\nmzcV7Lx1WRs0isBUiCJuxRgA2WmQKg4L3kif7vkOE8EdPixJTx2ev9x1lroyLe0m\n4nbW7tFMb1aaMMhQ5mNE2t6BSC6SUKVPZ0/pNycfhsh0LPweyK5GP30DBBkf2Rav\n2ppYc8s6NhsVkTfg+bJONRXhY80f3YGyXmH+52EvlSFooRk+P/Gg1a4J1neOQ5rt\ndjree82/AgMBAAECggEAEs21hQhHMoAUa/tZsWlTykTtd2I4PMWx0fGgUPehLGpj\n0p86sDP4HeLeOhmX49OHOq9tI0umCZln01/eVRNa2+8zHw3OVo9bF/hT+ZT9m5rM\noDiRt1yh6QCPuR6SU0qkOWF7NTEfRc2yZmilacAC+SMy1VbFVS26m6NQoZesIz9B\np8vHdobdZAmBZXIkNgKVXR6FSTaIXs/WU0KGAHeSFfDH0Z+202ZkOEsiViv3vxn5\nzejp8gxr7bwIYF8seGHPSAJowyfom87f2MrZtLN7+QZcjKnN78nLFyMT8hOnx8Q+\nh7RhTZrrw6hcm196T+tcNMQtgxP6+HCx+E5AErsY0QKBgQDjbsSSPE+eeG0s9XlX\nk76dstTNl4KauqRxjLAc+GYR/N3NIt7pKc4Fh6AZBkFNFKYpjYBvwkSSjyMQnN6a\n+pYhsBPTG9a1njHRpj86/937xaOL/BSDAKk688sFtoN/QaDKCKF6RkwZHVkTohtm\nnKhPoOf9brB5D9MSOzseHSkciwKBgQC9V4L9Yn4o7roHBKGeimpuvU6QhOhjNh1T\nhKQ5efrs0zUVXi0qLG8cTM1f4zgnnwMjxbh5l7vtvFm4YtGHqk2JqFouorvCSNo6\n6le0EOiIx94Nj6fOeDDGtqkiXjAfEDTPSXhhL+XN4vxgZHdhuM59lWfYME6q0rx8\n64gLvPL2HQKBgCxsWWb68s5QVXrfo8jwad4hrSFPQ8p3RGGNimTOPBmtW6GS+xlt\n+fjoieP5bc3hh6c8JWcu+ffqj33SNkTtR1/jJawpluG4uaBqqZUbnz9rVkukfFku\nSt/h+Ljv8nVr2z07PFdG3dxV+C02j8WWOeX71vSQp1WuOpsoCJ8UMRCLAoGBAJ2G\nPRiJ5OQxGNvV4pCAH+RZ4w8hRCWmU+e0Jt0ausRlQ3ivjWvU4+vricIIzCNKi9Yr\nHTssHdHALfTVYfU4nqG0SrMZ+JO/ALCbXrQUjSGfBwLJTZbdL9djCHvrWKW/WfBK\n87gHnW0ZN1cKvreyhTi+IFMgfZJpGR/k5J6/aHORAoGAKF4ywMjTuBZu/t9uBoM8\nCgHW1wqfWdNEy8xwg/20Ef361sGabZMB7UMhhA0K/ZKTvZ2dJuRB6horlXHcnuUv\nKQBmVMcPoRZjoFqHFB7xX76mWYyubmiU97TDj0parasOlpYxS52kZt3ZGlcfkAvP\nyhsVa3sH9QlJ2kj009Iab50=\n-----END PRIVATE KEY-----\n",
"client_email": "firebase-adminsdk-huesy@hemarays.iam.gserviceaccount.com",
"client_id": "107803427388685264608",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-huesy%40hemarays.iam.gserviceaccount.com"
}


cred = credentials.Certificate(firecreds)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'hemarays.appspot.com',
    # 'databaseURL': 'https://nous-project.firebaseio.com/'
})

app = Flask(__name__)

@app.route('/')
def hello():


    arrR = np.empty(shape=150, dtype=float)
    arrG = np.empty(shape=150, dtype=float)
    arrB = np.empty(shape=150, dtype=float)

    bucket = storage.bucket()
    blob = bucket.blob("test.mp4")

    # blob.download_to_filename("test.mp4")
    vidcap = cv2.VideoCapture("demo.mp4")   

    def getFrame(sec, countArr):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)

        hasFrames,image = vidcap.read()
        
        if hasFrames:
            print(image.shape)

            R = np.mean(image[:, :, 2])
            arrR[countArr] = R

            G = np.mean(image[:, :, 1])
            arrG[countArr] = G
            
            B = np.mean(image[:, :, 0])
            arrB[countArr] = B
            

            # print("RGB", arrR, arrG, arrB)

            # print(image)

            # exit(1)

            # cv2.imwrite("image"+str(count)+".jpg", image)     # save frame as JPG file
        return hasFrames
    
    sec = 0
    frameRate = 1/30 #//it will capture image in each 0.5 second

    print(frameRate*1000)

    start_time = datetime.now()
    
    count=0
    
    # '''
    success = getFrame(sec, count)
    
    # print("count start", count)
    
    while success:
        count = count + 1

        # print("count mid", count)
        
        sec = sec + frameRate
        success = getFrame(sec, count)



        if count == 149:
            print("count", count)
            break
    # '''

    timeTaken = datetime.now() - start_time

    retResponse = str.encode(timeTaken.__str__())

    dictArr = {
        "R": arrR,
        "G": arrG,
        "B": arrB
    }

    with open('arr.pickle', 'wb') as handle:
        pickle.dump(dictArr, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('arr.pickle', 'rb') as handle:
        dataDict = pickle.load(handle)


    # print("RGB", dictArr)

    # print("count end", count)

    # with open('arr.pickle', 'wb') as handle:
    #     pickle.dump(dictArr, handle, protocol=pickle.HIGHEST_PROTOCOL)


    blob.make_private()
    # '''

    # line 1 points 
    framesIndex = np.arange(start=0, stop=len(dataDict['R']), step=1)

    # print(framesIndex)

    # return -1
 
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    axis.plot(framesIndex, dataDict['R'], label = "R Channel", color="red")
    
    axis.plot(framesIndex, dataDict['G'], label = "G Channel", color="green")
    
    axis.plot(framesIndex, dataDict['B'], label = "B Channel", color="blue")
    
    axis.set_xlabel('Frames')

    axis.set_ylabel('RGB Average')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # plotting the line 1 points  
    # plt.plot(framesIndex, dataDict['R'], label = "R Channel", color="red") 
    
    # plotting the line 2 points  
    # plt.plot(framesIndex, dataDict['G'], label = "G Channel", color="green") 
    
    # plotting the line 2 points  
    # plt.plot(framesIndex, dataDict['B'], label = "B Channel", color="blue") 
    
    # naming the x axis 
    # plt.xlabel('Frames') 
    # naming the y axis 
    # plt.ylabel('RGB Average') 
    # giving a title to my graph 
    # plt.title('ANAL') 
    
    # show a legend on the plot 
    # plt.legend()

    # plt.savefig('static\\images\\new_plot.png') 
    
    # '''

    # response = dictArr.__str__()
    # response += "\n"
    
    # response = str.encode(response)

    # return response

    return Response(output.getvalue(), mimetype='image/png')

    # return render_template('index.html', name = 'new_plot', url ='static\\images\\new_plot.png')


if __name__ == '__main__':
    app.run()