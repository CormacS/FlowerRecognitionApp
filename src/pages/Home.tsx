import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonButton,
  IonIcon,
  IonCard,
  IonFabButton,
  IonFab,
  IonPopover,
  IonCardContent
} from "@ionic/react";
import { camera, help } from "ionicons/icons";
import React from "react";

import { useState } from 'react';
import { CameraResultType} from "@capacitor/core";
import { useCamera } from "@ionic/react-hooks/camera";


const Home: React.FC = () => {

  const [placeholder, setPlaceholder] = useState('');
  const { photo, getPhoto } = useCamera();
  const [popoverState, setShowPopover] = useState({ showPopover: false, event: undefined });
  
  //Allows user to take a picture or choose from gallery
  const takePicture = async () => {
    getPhoto({
        quality: 100,
        allowEditing: false,
        resultType: CameraResultType.DataUrl,
        saveToGallery: true,
      });
  };


  //Post request
  function  submitPhoto(pho: string) {
    fetch('/results', {

      //type of data we're sending
      headers: {
        'Content-Type': 'application/json'
      },
      
      // Choosing the method
      method: 'POST',
      body: JSON.stringify({"Image":pho})

    }).then(function (response) {
      return response.text();
  }).then(function (text) {
  
      var parsedData = JSON.parse(text);
      
      //Replaces placeholder 
      setPlaceholder(parsedData.Prediction);
  });
  }

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Flower Recognition App</IonTitle>
          
          
          <IonPopover
                event={popoverState.event}
                isOpen={popoverState.showPopover}
                onDidDismiss={() => setShowPopover({ showPopover: false, event: undefined })}
          >
                <p>Open the Analyse tab.<br></br> Press the camera icon to select a photo.<br></br>Click Analyse to see what flower it is!</p>
          </IonPopover>
          
            <IonButton 
            //When button is clicked set showPopover to true
            slot="end" onClick={
              (e: any) => {
                e.persist();
                setShowPopover({ showPopover: true, event: e })
              }}
            >
              <IonIcon slot="icon-only" icon={help} />
            </IonButton>
        </IonToolbar>
      </IonHeader>

      <IonContent className="ion-padding">
        
        
      <IonCard>
        
          {photo ? (
            //Ionic Card that contains all the information about the flower (Photo and Text)
            <div className="ion-text-center">
              <IonCard>
                <img width="450" height="500" src={photo.dataUrl} />
              </IonCard>
              <IonButton shape="round" fill="outline" color="success" onClick={() => submitPhoto(JSON.stringify(photo.dataUrl))}>Analyze</IonButton>
            </div>
          ) : null}
          <IonCardContent>
            
            {placeholder}
          </IonCardContent>
        </IonCard>

      <br></br>
      <br></br>

      </IonContent>

        <IonFab vertical="bottom" horizontal="center" slot="fixed">
          
            <IonFabButton 
            //Calls takePicture to open up the camera
              onClick={() => takePicture()}>
              <IonIcon icon={camera}></IonIcon>
            </IonFabButton>
        </IonFab>
      
    </IonPage>
  );
};

export default Home;