from flask import Flask, request, jsonify, abort
import cv2
from PIL import Image
import predictions as pred
import numpy as np
import base64  
import io
import pandas as pd

import json
app = Flask(__name__)

@app.route("/members")
def members():    
    return {"members": ["Member1","Member2","Member3"]}
   

@app.route("/ocrProcessing", methods=['POST'])
def ocrProcessing():
    print("Hello ocr Processing started.....")
    # if not request.json or 'img' not in request.json: 
    #     abort(400)
    if(request.method == "POST"):
        reqOfImage = request.get_data()
        #print(" request data ", reqOfImage)    
        req_data = json.loads(reqOfImage)     
        img_data = req_data['base64']  
        result = img_data.index('base64')
        byteIndex = result+6
        byte_data = img_data[byteIndex:]
        b = base64.b64decode(byte_data)
        #print(b)
        img = Image.open(io.BytesIO(b))
        img.save('savedImage.png')
        #img.show()
        
        
        img_results, entities = pred.getPredictions(img)   
        print(entities)
        print("image type 1 ", type(img))
        
        # img_pl2 = Image.open('flask-server\Invoice_1.jpeg')
        # img_results2, entities2 = pred.getPredictions(img_pl2)   
        # print(entities2)
        # print("image type 1 ", type(img_pl2))
        
        
        return entities



if __name__ == "__main__":
    app.run(debug=True)