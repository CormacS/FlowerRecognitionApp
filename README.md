# FlowerRecognitionApp
This README file contains a project description, project structure and how to get the project running.

## Project Description
This app is a mobile application for IOS and Android that focuses on the identification of flowers.
The app uses a trained image classification model that takes in any image and returns a prediction along with a short description.

## Project Structure
Project is divided into 2 sections, frontend and backend.

### Frontend

FlowerRecognitionApp/src
This folder contains the main code that was used for creating the front end.
FlowerRecognitionApp/src/pages contains home.tsx which is what is actually displaed to the user.

#### Deployment
Clone the repo
Type ionic serve in the terminal

#### Deployment on Mobile
Make sure to have Android Studio or XCode installed.
Clone the repo
Type into Terminal:
- Ionic Build
- Ionic cap
- Ionic cap copy
- Ionic cap sync
Run on Android Studio

### Backend

#### Breakdown
api.py - contains all the content for the API and Backend
my_h5_model.h5 - This is the machine learning model
FlowerModel.ipynb - This is the file that actually created and trained the model
ngrox.exe - used to host your localhost publicly

#### Deployment (Locally)
Clone the repo
Go into the flask-api folder and do flask run

Now it should work locally

#### Deployment (Hosted)
- Clone the repo
- Go into the flask-api folder and do flask run, copy the localhost
- Run ngrox.exe
- In the ngrox terminal type ngrok http (You address here)
- Ngrox will now display the new link under Fowarding, copy one of them
- Open the file Home.tsx and go the line 42. This should be the line with fetch('/results').
- before the / paste in the new URL. Example: 'www.NewAddress.com/results'
- Now it should work from anywhere, just have to load it onto phone now. (steps above)

### Dataset
This is a link to the dataset used for training, can easily be switched out with any dataset you want.
https://www.kaggle.com/alxmamaev/flowers-recognition

### Code References
These are the resources I used below to learn and get it working. 

https://ionicframework.com/docs/react/your-first-app

Would recommend doing some extra research into the things done in this guide rather than just copy paste
https://www.tensorflow.org/tutorials/images/classification - Dataset was a funny coincidence
