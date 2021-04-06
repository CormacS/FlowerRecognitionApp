from flask import Flask, request
from flask_cors import CORS
from tensorflow import keras

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib


import base64
import json

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


#Sets up Flask and CORS
app = Flask(__name__)
CORS(app)

#Setting up API call to recieve the image
@app.route('/results',methods=['GET','POST'])
def results():
    #Take the dataurl from the json
    input = request.get_json()
    
    #Pass the dataurl to the function modelPredictions
    pred = modelPredictions(input)
    return {"Prediction":pred}


def modelPredictions(input):
    img_height = 180
    img_width = 180
    batch_size = 5
    data_dir = pathlib.Path("C:/Users/corma/Desktop/New folder/FYP/MobileAPP/flowerFireApp/flowerRecognitionApp/flask-api/flower_photos")

    #We do this so we can get the class names
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = train_ds.class_names

    #Load in the model
    reconstructed_model = keras.models.load_model("C:/Users/corma/Desktop/New folder/FYP/MobileAPP/flowerFireApp/flowerRecognitionApp/flask-api/my_h5_model.h5")


    #Split the dataurl so we remove the text before the comma
    input = json.dumps(input)
    input = input.split(",")

    #Decode the DataUrl and write it out as a PNG
    base64_img_bytes = input[1].encode('utf-8')
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)

    #Load the image
    img = keras.preprocessing.image.load_img(
        "C:/Users/corma/Desktop/New folder/FYP/MobileAPP/flowerFireApp/flowerRecognitionApp/flask-api/decoded_image.png", target_size=(img_height, img_width)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    #Use the model to make a prediction
    predictions = reconstructed_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    #Take the best score and store the flower name
    flower = class_names[np.argmax(score)]
    #Pass the flower name to the web scraping function
    scraped = webScraping(flower)

    #String that prints out flower name and description of flower
    output = ("{} ({:.2f}%) ".format(class_names[np.argmax(score)], 100 * np.max(score))+scraped)

    
    return(output)

def webScraping(flower):
    i = 1
    #Checks if the flower is Daisy as for the web scraping to work it needs its scientific name
    if(flower == "Daisy"):
        flower = "Bellis_perennis"

    
    URL = 'https://kids.kiddle.co/'+flower
    page = requests.get(URL)
    #Go to this URL and take the content from the page
    soup = BeautifulSoup(page.content, 'html.parser')

    #Find the first <p> tag and get the text
    results = soup.find_all('p')[0].get_text()

    #Check if the <p> tag actually contains a decent amount of text
    length = len(results)
    while(length < 10):
        results = soup.find_all('p')[i].get_text()
        length = len(results)
        i = i + 1

    return(results)