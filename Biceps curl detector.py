#!pip install gTTS
import cv2
import mediapipe as mp
import numpy as np

import pyttsx3
cap = cv2.VideoCapture(0)


from gtts import gTTS
import os

counter = 0 
stage = None


up = "Go up"
down = "Go down"

voice = pyttsx3.init()


def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    return angle 



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
    

tts_up = gTTS(up)
tts_down = gTTS(down)


tts_up.save("up.mp3")
tts_down.save("down.mp3")


#os.system("start up.mp3")
#os.system("start down.mp3")

user = input("Which exercise?")
if user == "Biceps":
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
          

            results = pose.process(image)
        

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            

            try:
                landmarks = results.pose_landmarks.landmark
                
                #coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                #angle
                angle = calculate_angle(shoulder, elbow, wrist)
                
                #Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                #Curl counte
                if angle > 155:
                    stage = "down"
                    #os.system("start up.mp3")
                    voice.say("Go up up up")
                    voice.runAndWait()
                    exit()
                    
                if angle < 40 and stage =='down':
                    stage="up"
                    #os.system("start down.mp3")
                    voice.say("Go down")
                    voice.runAndWait()
                    counter +=1
                    print(counter)
                    exit()
                           
            except:
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               
            
            cv2.imshow('Mediapipe Feed', image)
    
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
        cap.release()
        cv2.destroyAllWindows()
else: print("Bro sorry")
